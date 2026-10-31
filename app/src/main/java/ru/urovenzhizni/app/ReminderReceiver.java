package ru.urovenzhizni.app;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

public class ReminderReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        try {
            Reminders.fire(context);
        } finally {
            Reminders.schedule(context);
        }
    }
}
