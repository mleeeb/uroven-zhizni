package ru.urovenzhizni.app;

import android.Manifest;
import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.ClipData;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Insets;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.view.WindowInsets;
import android.webkit.JavascriptInterface;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;

import org.json.JSONObject;

import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * The whole game is the web page in assets/www. This screen shows it full-screen and gives it storage, photos,
 * backups and reminders. Photos are served to the page from files at https://uroven.local/photo/<id>.jpg.
 */
public class MainActivity extends Activity {
    private static final int REQ_FILE = 1;
    private static final int REQ_EXPORT = 2;
    private static final int REQ_NOTIFY = 3;
    private static final int REQ_RESTORE = 4;
    static final String PHOTO_HOST = "uroven.local";

    private WebView web;
    private ValueCallback<Uri[]> fileCallback;
    private String pendingExport;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        FrameLayout root = new FrameLayout(this);
        root.setBackgroundColor(0xFF151833);
        web = new WebView(this);
        web.setBackgroundColor(0xFF1B1E3A);
        root.addView(web, new FrameLayout.LayoutParams(FrameLayout.LayoutParams.MATCH_PARENT, FrameLayout.LayoutParams.MATCH_PARENT));
        setContentView(root);

        // Android 11+: draw edge to edge and keep the page clear of the status bar, navigation bar and keyboard.
        if (Build.VERSION.SDK_INT >= 30) {
            getWindow().setDecorFitsSystemWindows(false);
            root.setOnApplyWindowInsetsListener((View v, WindowInsets insets) -> {
                Insets bars = insets.getInsets(WindowInsets.Type.systemBars() | WindowInsets.Type.displayCutout());
                Insets ime = insets.getInsets(WindowInsets.Type.ime());
                v.setPadding(bars.left, bars.top, bars.right, Math.max(bars.bottom, ime.bottom));
                return WindowInsets.CONSUMED;
            });
        }

        WebSettings ws = web.getSettings();
        ws.setJavaScriptEnabled(true);
        ws.setDomStorageEnabled(true);
        ws.setTextZoom(100);
        ws.setAllowContentAccess(true);
        ws.setMediaPlaybackRequiresUserGesture(true);

        web.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri u = request.getUrl();
                String scheme = u.getScheme();
                if ("http".equals(scheme) || "https".equals(scheme)) {
                    try { startActivity(new Intent(Intent.ACTION_VIEW, u)); } catch (ActivityNotFoundException ignored) {}
                    return true;
                }
                return false;
            }

            /** Photos are read straight from files, so the page never has to carry them as text. */
            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                Uri u = request.getUrl();
                if (!PHOTO_HOST.equals(u.getHost())) return null;
                Map<String, String> headers = new HashMap<>();
                headers.put("Cache-Control", "no-store");
                headers.put("Access-Control-Allow-Origin", "*");
                List<String> seg = u.getPathSegments();
                if (seg.size() == 2 && "photo".equals(seg.get(0))) {
                    String name = seg.get(1);
                    String id = name.endsWith(".jpg") ? name.substring(0, name.length() - 4) : name;
                    File f = Store.photo(MainActivity.this, id);
                    try {
                        if (f.exists()) return new WebResourceResponse("image/jpeg", null, 200, "OK", headers, new FileInputStream(f));
                    } catch (Exception ignored) {}
                }
                return new WebResourceResponse("text/plain", null, 404, "Not Found", headers, new ByteArrayInputStream(new byte[0]));
            }
        });

        // <input type="file">: photos for the life feed. Several photos come back as ClipData, one as getData().
        web.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> callback, FileChooserParams params) {
                if (fileCallback != null) fileCallback.onReceiveValue(null);
                fileCallback = callback;
                Intent pick = params.createIntent();
                if (params.getMode() == FileChooserParams.MODE_OPEN_MULTIPLE) pick.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
                try {
                    startActivityForResult(pick, REQ_FILE);
                } catch (ActivityNotFoundException e) {
                    fileCallback = null;
                    return false;
                }
                return true;
            }
        });

        web.addJavascriptInterface(new Bridge(), "Native");
        Reminders.ensureChannel(this);
        new Thread(() -> Store.migratePhotos(this)).start();
        web.loadUrl("file:///android_asset/www/index.html");
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        Uri uri = data == null ? null : data.getData();
        if (requestCode == REQ_FILE) {
            Uri[] picked = null;
            if (resultCode == RESULT_OK && data != null) {
                ClipData clip = data.getClipData();
                if (clip != null && clip.getItemCount() > 0) {
                    picked = new Uri[clip.getItemCount()];
                    for (int i = 0; i < picked.length; i++) picked[i] = clip.getItemAt(i).getUri();
                } else if (uri != null) {
                    picked = new Uri[]{uri};
                }
            }
            if (fileCallback != null) fileCallback.onReceiveValue(picked);
            fileCallback = null;
        } else if (requestCode == REQ_EXPORT) {
            String json = pendingExport;
            pendingExport = null;
            if (resultCode != RESULT_OK || uri == null || json == null) {
                jsToast("КОПИЯ НЕ СОХРАНЕНА");
                return;
            }
            new Thread(() -> jsToast(Backup.writeZip(this, uri, json) ? "КОПИЯ СОХРАНЕНА" : "НЕ ПОЛУЧИЛОСЬ СОХРАНИТЬ КОПИЮ")).start();
        } else if (requestCode == REQ_RESTORE) {
            if (resultCode != RESULT_OK || uri == null) return;
            new Thread(() -> {
                Backup.Result r = Backup.read(this, uri);
                if (r.json == null) {
                    Backup.discard(this);
                    jsToast("НЕ ПОЛУЧИЛОСЬ ПРОЧИТАТЬ ФАЙЛ");
                    return;
                }
                String js = "window.__onRestoreFile&&window.__onRestoreFile(" + JSONObject.quote(r.json) + "," + r.zip + ")";
                web.post(() -> web.evaluateJavascript(js, null));
            }).start();
        }
    }

    @Override
    @SuppressWarnings("deprecation")
    public void onBackPressed() {
        web.evaluateJavascript("(window.__onBack&&window.__onBack())?'1':'0'", value -> {
            if (!"\"1\"".equals(value)) finish();
        });
    }

    @Override
    protected void onResume() {
        super.onResume();
        web.onResume();
    }

    @Override
    protected void onPause() {
        web.onPause();
        super.onPause();
    }

    private void jsToast(String message) {
        web.post(() -> web.evaluateJavascript("window.__nativeToast&&window.__nativeToast(" + JSONObject.quote(message) + ")", null));
    }

    /** Called from the page as window.Native.*. Runs on a background thread. */
    private class Bridge {
        @JavascriptInterface public String loadCore() { return Store.read(MainActivity.this, Store.CORE); }
        @JavascriptInterface public boolean saveCore(String json) { return Store.write(MainActivity.this, Store.CORE, json); }
        @JavascriptInterface public String loadEvents() { return Store.read(MainActivity.this, Store.EVENTS); }
        @JavascriptInterface public boolean saveEvents(String json) { return Store.write(MainActivity.this, Store.EVENTS, json); }

        /** The page sends a new photo once (after shrinking it); it is stored as a JPEG file. */
        @JavascriptInterface public boolean savePhoto(String id, String dataUrl) { return Store.savePhoto(MainActivity.this, id, dataUrl); }
        @JavascriptInterface public void deletePhoto(String id) { Store.deletePhoto(MainActivity.this, id); }
        @JavascriptInterface public String photoBase() { return "https://" + PHOTO_HOST + "/photo/"; }

        @JavascriptInterface public void clearAll() {
            Store.clearAll(MainActivity.this);
            Reminders.schedule(MainActivity.this);
        }

        @JavascriptInterface public void setReminders(String json) {
            Store.write(MainActivity.this, Store.REMINDERS, json);
            Reminders.schedule(MainActivity.this);
        }

        @JavascriptInterface public void requestNotifications() {
            if (Build.VERSION.SDK_INT < 33) return;
            if (checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) == PackageManager.PERMISSION_GRANTED) return;
            runOnUiThread(() -> requestPermissions(new String[]{Manifest.permission.POST_NOTIFICATIONS}, REQ_NOTIFY));
        }

        /** Asks where to save, then writes a ZIP: data.json plus every photo file. */
        @JavascriptInterface public void exportBackupZip(String fileName, String dataJson) {
            runOnUiThread(() -> {
                pendingExport = dataJson;
                Intent i = new Intent(Intent.ACTION_CREATE_DOCUMENT)
                        .addCategory(Intent.CATEGORY_OPENABLE)
                        .setType("application/zip")
                        .putExtra(Intent.EXTRA_TITLE, fileName);
                try {
                    startActivityForResult(i, REQ_EXPORT);
                } catch (ActivityNotFoundException e) {
                    pendingExport = null;
                    jsToast("НЕТ ПРИЛОЖЕНИЯ ДЛЯ СОХРАНЕНИЯ ФАЙЛОВ");
                }
            });
        }

        /** Lets the user pick a backup (ZIP or an older JSON). The page gets window.__onRestoreFile(json, isZip). */
        @JavascriptInterface public void pickRestore() {
            runOnUiThread(() -> {
                Intent i = new Intent(Intent.ACTION_OPEN_DOCUMENT)
                        .addCategory(Intent.CATEGORY_OPENABLE)
                        .setType("*/*")
                        .putExtra(Intent.EXTRA_MIME_TYPES, new String[]{"application/zip", "application/x-zip-compressed", "application/json", "application/octet-stream", "text/plain"});
                try {
                    startActivityForResult(i, REQ_RESTORE);
                } catch (ActivityNotFoundException e) {
                    jsToast("НЕТ ПРИЛОЖЕНИЯ ДЛЯ ВЫБОРА ФАЙЛОВ");
                }
            });
        }

        /** After the user confirmed: the staged photos from the ZIP take the place of the current ones. */
        @JavascriptInterface public boolean commitRestore() { return Backup.commit(MainActivity.this); }
        @JavascriptInterface public void discardRestore() { Backup.discard(MainActivity.this); }
    }
}
