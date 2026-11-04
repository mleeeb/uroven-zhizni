package ru.urovenzhizni.app;

import android.Manifest;
import android.app.AlarmManager;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.os.Build;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

/**
 * The page decides what to remind and when; it sends a list of items {at (ms), title, text}.
 * Here we keep one alarm for the nearest item. When it fires we show everything that is due and set the next one.
 */
final class Reminders {
    static final String CHANNEL = "reminders";
    private static final long DAY = 24L * 60 * 60 * 1000;

    private Reminders() {}

    static void ensureChannel(Context c) {
        NotificationManager nm = c.getSystemService(NotificationManager.class);
        if (nm == null || nm.getNotificationChannel(CHANNEL) != null) return;
        NotificationChannel ch = new NotificationChannel(CHANNEL, c.getString(R.string.channel_name), NotificationManager.IMPORTANCE_DEFAULT);
        ch.setDescription(c.getString(R.string.channel_desc));
        nm.createNotificationChannel(ch);
    }

    private static JSONArray items(Context c) {
        try {
            String s = Store.read(c, Store.REMINDERS);
            if (s == null || s.isEmpty()) return null;
            return new JSONObject(s).optJSONArray("items");
        } catch (Exception e) {
            return null;
        }
    }

    private static SharedPreferences prefs(Context c) {
        return c.getSharedPreferences("reminders", Context.MODE_PRIVATE);
    }

    private static PendingIntent alarmIntent(Context c) {
        Intent i = new Intent(c, ReminderReceiver.class);
        return PendingIntent.getBroadcast(c, 0, i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
    }

    static void schedule(Context c) {
        AlarmManager am = c.getSystemService(AlarmManager.class);
        if (am == null) return;
        PendingIntent pi = alarmIntent(c);
        long now = System.currentTimeMillis(), next = Long.MAX_VALUE;
        JSONArray a = items(c);
        if (a != null) {
            for (int i = 0; i < a.length(); i++) {
                JSONObject o = a.optJSONObject(i);
                if (o == null) continue;
                long at = o.optLong("at");
                if (at > now && at < next) next = at;
            }
        }
        if (next == Long.MAX_VALUE) {
            am.cancel(pi);
            return;
        }
        am.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, next, pi);
    }

    static void fire(Context c) {
        long now = System.currentTimeMillis();
        SharedPreferences p = prefs(c);
        long from = Math.max(p.getLong("last", 0), now - DAY);
        long to = now + 60_000;
        p.edit().putLong("last", to).apply();

        List<JSONObject> due = new ArrayList<>();
        JSONArray a = items(c);
        if (a != null) {
            for (int i = 0; i < a.length(); i++) {
                JSONObject o = a.optJSONObject(i);
                if (o == null) continue;
                long at = o.optLong("at");
                if (at > from && at <= to) due.add(o);
            }
        }
        if (due.isEmpty()) return;
        if (Build.VERSION.SDK_INT >= 33
                && c.checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) return;

        ensureChannel(c);
        String title = due.size() == 1 ? due.get(0).optString("title", c.getString(R.string.app_name)) : c.getString(R.string.app_name);
        StringBuilder all = new StringBuilder();
        for (JSONObject o : due) {
            if (all.length() > 0) all.append('\n');
            all.append(o.optString("text"));
        }
        Intent open = new Intent(c, MainActivity.class).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP);
        PendingIntent tap = PendingIntent.getActivity(c, 1, open, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        Notification n = new Notification.Builder(c, CHANNEL)
                .setSmallIcon(R.drawable.ic_notification)
                .setColor(0xFFF2CC8F)
                .setContentTitle(title)
                .setContentText(due.get(0).optString("text"))
                .setStyle(new Notification.BigTextStyle().bigText(all.toString()))
                .setContentIntent(tap)
                .setAutoCancel(true)
                .build();
        NotificationManager nm = c.getSystemService(NotificationManager.class);
        if (nm != null) nm.notify((int) ((now / 60_000) % Integer.MAX_VALUE), n);
    }
}
