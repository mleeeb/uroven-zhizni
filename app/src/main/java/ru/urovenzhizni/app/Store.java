package ru.urovenzhizni.app;

import android.content.Context;
import android.util.Base64;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;

/**
 * Files in the app's private storage. Every write goes to a temp file first, so a crash never leaves half a file.
 * Photos are JPEG files in photos/<id>.jpg. Older versions kept them as base64 text in photos/<id>.txt;
 * those are converted the first time they are needed.
 */
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

    static String safeId(String id) {
        String safe = id == null ? "" : id.replaceAll("[^A-Za-z0-9_-]", "");
        return safe.isEmpty() ? "x" : safe;
    }

    static File photoFile(Context c, String id) {
        return new File(photosDir(c), safeId(id) + ".jpg");
    }

    private static File legacyPhotoFile(Context c, String id) {
        return new File(photosDir(c), safeId(id) + ".txt");
    }

    /** The JPEG of a photo; converts an old text file on the way. The file may not exist. */
    static File photo(Context c, String id) {
        File f = photoFile(c, id);
        if (f.exists()) return f;
        File old = legacyPhotoFile(c, id);
        if (old.exists()) {
            byte[] bytes = decodeDataUrl(read(old));
            if (bytes != null && writeBytes(f, bytes)) old.delete();
        }
        return f;
    }

    static void migratePhotos(Context c) {
        File[] files = photosDir(c).listFiles();
        if (files == null) return;
        for (File f : files) {
            String n = f.getName();
            if (n.endsWith(".txt")) photo(c, n.substring(0, n.length() - 4));
        }
    }

    static byte[] decodeDataUrl(String s) {
        if (s == null || s.isEmpty()) return null;
        int comma = s.indexOf(',');
        try {
            return Base64.decode(comma >= 0 ? s.substring(comma + 1) : s, Base64.DEFAULT);
        } catch (IllegalArgumentException e) {
            return null;
        }
    }

    static boolean savePhoto(Context c, String id, String dataUrl) {
        byte[] bytes = decodeDataUrl(dataUrl);
        if (bytes == null || bytes.length == 0) return false;
        boolean ok = writeBytes(photoFile(c, id), bytes);
        if (ok) legacyPhotoFile(c, id).delete();
        return ok;
    }

    static void deletePhoto(Context c, String id) {
        photoFile(c, id).delete();
        legacyPhotoFile(c, id).delete();
    }

    static String read(File f) {
        if (!f.exists()) return null;
        try (InputStream in = new FileInputStream(f)) {
            return readText(in);
        } catch (Exception e) {
            return null;
        }
    }

    static String readText(InputStream in) throws java.io.IOException {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        byte[] buf = new byte[64 * 1024];
        int n;
        while ((n = in.read(buf)) > 0) out.write(buf, 0, n);
        return out.toString(StandardCharsets.UTF_8.name());
    }

    static boolean writeBytes(File f, byte[] data) {
        File tmp = new File(f.getParentFile(), f.getName() + ".tmp");
        try (FileOutputStream out = new FileOutputStream(tmp)) {
            out.write(data);
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

    static boolean write(File f, String data) {
        return writeBytes(f, (data == null ? "" : data).getBytes(StandardCharsets.UTF_8));
    }

    static String read(Context c, String name) {
        return read(new File(c.getFilesDir(), name));
    }

    static boolean write(Context c, String name, String data) {
        return write(new File(c.getFilesDir(), name), data);
    }

    static void clearDir(File dir) {
        File[] files = dir.listFiles();
        if (files != null) for (File f : files) f.delete();
    }

    static void clearAll(Context c) {
        new File(c.getFilesDir(), CORE).delete();
        new File(c.getFilesDir(), EVENTS).delete();
        new File(c.getFilesDir(), REMINDERS).delete();
        clearDir(photosDir(c));
    }
}
