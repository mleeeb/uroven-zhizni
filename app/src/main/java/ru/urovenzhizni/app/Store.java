package ru.urovenzhizni.app;

import android.content.Context;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;

/** Files in the app's private storage. Every write goes to a temp file first, so a crash never leaves half a file. */
final class Store {
    static final String CORE = "core.json";
    static final String EVENTS = "events.json";
    static final String REMINDERS = "reminders.json";

    private Store() {}

    static File photosDir(Context c) {
        File d = new File(c.getFilesDir(), "photos");
        if (!d.exists()) d.mkdirs();
        return d;
    }

    static File photoFile(Context c, String id) {
        String safe = id == null ? "" : id.replaceAll("[^A-Za-z0-9_-]", "");
        if (safe.isEmpty()) safe = "x";
        return new File(photosDir(c), safe + ".txt");
    }

    static String read(File f) {
        if (!f.exists()) return null;
        try (InputStream in = new FileInputStream(f)) {
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            byte[] buf = new byte[64 * 1024];
            int n;
            while ((n = in.read(buf)) > 0) out.write(buf, 0, n);
            return out.toString(StandardCharsets.UTF_8.name());
        } catch (Exception e) {
            return null;
        }
    }

    static boolean write(File f, String data) {
        File tmp = new File(f.getParentFile(), f.getName() + ".tmp");
        try (FileOutputStream out = new FileOutputStream(tmp)) {
            out.write((data == null ? "" : data).getBytes(StandardCharsets.UTF_8));
            out.getFD().sync();
        } catch (Exception e) {
            tmp.delete();
            return false;
        }
        if (f.exists() && !f.delete()) {
            tmp.delete();
            return false;
        }
        return tmp.renameTo(f);
    }

    static String read(Context c, String name) {
        return read(new File(c.getFilesDir(), name));
    }

    static boolean write(Context c, String name, String data) {
        return write(new File(c.getFilesDir(), name), data);
    }

    static void clearAll(Context c) {
        new File(c.getFilesDir(), CORE).delete();
        new File(c.getFilesDir(), EVENTS).delete();
        new File(c.getFilesDir(), REMINDERS).delete();
        File[] photos = photosDir(c).listFiles();
        if (photos != null) for (File p : photos) p.delete();
    }
}
