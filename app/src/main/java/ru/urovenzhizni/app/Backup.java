package ru.urovenzhizni.app;

import android.content.Context;
import android.net.Uri;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;
import java.util.zip.ZipOutputStream;

/**
 * Backup is a ZIP: data.json with everything except photos, and photos/<id>.jpg.
 * Files are streamed one by one, so even hundreds of photos never sit in memory together.
 * Restoring unpacks photos into a staging folder first; they replace the current ones only after the user confirms.
 */
final class Backup {
    static final class Result {
        String json;
        boolean zip;
    }

    private Backup() {}

    private static File stageDir(Context c) {
        File d = new File(c.getFilesDir(), "restore_tmp");
        if (!d.exists()) d.mkdirs();
        return d;
    }

    private static void copy(InputStream in, OutputStream out) throws java.io.IOException {
        byte[] buf = new byte[64 * 1024];
        int n;
        while ((n = in.read(buf)) > 0) out.write(buf, 0, n);
    }

    static boolean writeZip(Context c, Uri uri, String dataJson) {
        try (OutputStream raw = c.getContentResolver().openOutputStream(uri, "wt");
             ZipOutputStream zip = new ZipOutputStream(new BufferedOutputStream(raw))) {
            zip.putNextEntry(new ZipEntry("data.json"));
            zip.write(dataJson.getBytes(StandardCharsets.UTF_8));
            zip.closeEntry();
            Store.migratePhotos(c);
            File[] files = Store.photosDir(c).listFiles();
            if (files != null) {
                for (File f : files) {
                    if (!f.getName().endsWith(".jpg")) continue;
                    zip.putNextEntry(new ZipEntry("photos/" + f.getName()));
                    try (InputStream in = new FileInputStream(f)) {
                        copy(in, zip);
                    }
                    zip.closeEntry();
                }
            }
            zip.finish();
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    /** Reads a ZIP backup (photos go to the staging folder) or an older JSON backup (photos are inside it). */
    static Result read(Context c, Uri uri) {
        File stage = stageDir(c);
        Store.clearDir(stage);
        Result r = new Result();
        try (InputStream raw = c.getContentResolver().openInputStream(uri)) {
            BufferedInputStream in = new BufferedInputStream(raw);
            in.mark(4);
            int b0 = in.read(), b1 = in.read();
            in.reset();
            if (b0 == 'P' && b1 == 'K') {
                r.zip = true;
                ZipInputStream zip = new ZipInputStream(in);
                ZipEntry e;
                while ((e = zip.getNextEntry()) != null) {
                    if (e.isDirectory()) continue;
                    String name = e.getName();
                    if ("data.json".equals(name)) {
                        r.json = Store.readText(zip);
                    } else if (name.startsWith("photos/") && name.endsWith(".jpg")) {
                        String id = Store.safeId(name.substring(7, name.length() - 4));
                        try (OutputStream out = new FileOutputStream(new File(stage, id + ".jpg"))) {
                            copy(zip, out);
                        }
                    }
                }
            } else {
                r.json = Store.readText(in);
            }
        } catch (Exception ex) {
            r.json = null;
        }
        return r;
    }

    /** Moves the staged photos into place. Call after Store.clearAll. */
    static boolean commit(Context c) {
        File[] files = stageDir(c).listFiles();
        boolean ok = true;
        if (files != null) {
            File dir = Store.photosDir(c);
            for (File f : files) ok &= f.renameTo(new File(dir, f.getName()));
        }
        return ok;
    }

    static void discard(Context c) {
        Store.clearDir(stageDir(c));
    }
}
