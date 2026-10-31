package ru.urovenzhizni.app;

import android.Manifest;
import android.app.AlarmManager;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Build;

import org.json.JSONArray;
import org.json.JSONObject;

import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;

/**
 * One alarm a day at the time the user picked. When it fires we decide what to say:
 * deadlines in 3 days, tomorrow or today, and an evening "write down your day" if nothing was written today.
 */
final class Reminders {
    static final String CHANNEL = "reminders";
    private static final int NOTIFY_ID = 1;

    private Reminders() {}

    static void ensureChannel(Context c) {
        NotificationManager nm = c.getSystemService(NotificationManager.class);
        if (nm == null || nm.getNotificationChannel(CHANNEL) != null) return;
        NotificationChannel ch = new NotificationChannel(CHANNEL, c.getString(R.string.channel_name), NotificationManager.IMPORTANCE_DEFAULT);
        ch.setDescription(c.getString(R.string.channel_desc));
        nm.createNotificationChannel(ch);
    }

    private static JSONObject settings(Context c) {
        try {
            String s = Store.read(c, Store.REMINDERS);
            return s == null || s.isEmpty() ? null : new JSONObject(s);
        } catch (Exception e) {
            return null;
        }
    }

    private static PendingIntent alarmIntent(Context c) {
        Intent i = new Intent(c, ReminderReceiver.class);
        return PendingIntent.getBroadcast(c, 0, i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
    }

    /** Sets the next alarm, or cancels it when every reminder is off. */
    static void schedule(Context c) {
        AlarmManager am = c.getSystemService(AlarmManager.class);
        if (am == null) return;
        PendingIntent pi = alarmIntent(c);
        JSONObject s = settings(c);
        if (s == null || !(s.optBoolean("daily") || s.optBoolean("deadlines"))) {
            am.cancel(pi);
            return;
        }
        int hour = 21, minute = 0;
        try {
            String[] t = s.optString("time", "21:00").split(":");
            hour = Integer.parseInt(t[0]);
            minute = Integer.parseInt(t[1]);
        } catch (Exception ignored) {}
        Calendar next = Calendar.getInstance();
        next.set(Calendar.HOUR_OF_DAY, hour);
        next.set(Calendar.MINUTE, minute);
        next.set(Calendar.SECOND, 0);
        next.set(Calendar.MILLISECOND, 0);
        if (next.getTimeInMillis() <= System.currentTimeMillis() + 30_000) next.add(Calendar.DAY_OF_MONTH, 1);
        am.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, next.getTimeInMillis(), pi);
    }

    static void fire(Context c) {
        JSONObject s = settings(c);
        if (s == null) return;
        if (Build.VERSION.SDK_INT >= 33
                && c.checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) return;

        LocalDate today = LocalDate.now();
        List<String> lines = new ArrayList<>();
        if (s.optBoolean("deadlines")) {
            JSONArray qs = s.optJSONArray("quests");
            if (qs != null) {
                for (int i = 0; i < qs.length(); i++) {
                    JSONObject q = qs.optJSONObject(i);
                    if (q == null) continue;
                    try {
                        long d = ChronoUnit.DAYS.between(today, LocalDate.parse(q.optString("due")));
                        String title = "«" + q.optString("title") + "»";
                        if (d == 0) lines.add("Сегодня срок задания " + title);
                        else if (d == 1) lines.add("Завтра срок задания " + title);
                        else if (d == 3) lines.add("Через 3 дня срок задания " + title);
                    } catch (Exception ignored) {}
                }
            }
        }
        boolean wroteToday = today.toString().equals(s.optString("lastEntry"));
        if (s.optBoolean("daily") && !wroteToday) lines.add("Как прошёл день? Запиши его в ленту жизни.");
        if (lines.isEmpty()) return;

        ensureChannel(c);
        String title = lines.get(0).startsWith("Как прошёл") ? c.getString(R.string.app_name) : "Задания ждут";
        StringBuilder all = new StringBuilder();
        for (String l : lines) {
            if (all.length() > 0) all.append('\n');
            all.append(l);
        }
        Intent open = new Intent(c, MainActivity.class).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP);
        PendingIntent tap = PendingIntent.getActivity(c, 1, open, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        Notification n = new Notification.Builder(c, CHANNEL)
                .setSmallIcon(R.drawable.ic_notification)
                .setColor(0xFFF2CC8F)
                .setContentTitle(title)
                .setContentText(lines.get(0))
                .setStyle(new Notification.BigTextStyle().bigText(all.toString()))
                .setContentIntent(tap)
                .setAutoCancel(true)
                .build();
        NotificationManager nm = c.getSystemService(NotificationManager.class);
        if (nm != null) nm.notify(NOTIFY_ID, n);
    }
}
