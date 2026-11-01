package ru.urovenzhizni.app;

import android.Manifest;
import android.app.Activity;
import android.content.ClipData;
import android.content.ActivityNotFoundException;
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
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;

import org.json.JSONObject;

import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

/** The whole game is the web page in assets/www. This screen shows it full-screen and gives it storage, files and reminders. */
public class MainActivity extends Activity {
    private static final int REQ_FILE = 1;
    private static final int REQ_EXPORT = 2;
    private static final int REQ_NOTIFY = 3;

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
        });

        // <input type="file">: photos for the life feed and the backup file to restore.
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
        web.loadUrl("file:///android_asset/www/index.html");
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == REQ_FILE) {
            // Several photos come back as ClipData, one photo as getData().
            Uri[] picked = null;
            if (resultCode == RESULT_OK && data != null) {
                ClipData clip = data.getClipData();
                if (clip != null && clip.getItemCount() > 0) {
                    picked = new Uri[clip.getItemCount()];
                    for (int i = 0; i < picked.length; i++) picked[i] = clip.getItemAt(i).getUri();
                } else if (data.getData() != null) {
                    picked = new Uri[]{data.getData()};
                }
            }
            if (fileCallback != null) fileCallback.onReceiveValue(picked);
            fileCallback = null;
        } else if (requestCode == REQ_EXPORT) {
            String json = pendingExport;
            pendingExport = null;
            Uri uri = data == null ? null : data.getData();
            if (resultCode != RESULT_OK || uri == null || json == null) {
                jsToast("КОПИЯ НЕ СОХРАНЕНА");
                return;
            }
            new Thread(() -> {
                boolean ok = false;
                try (OutputStream out = getContentResolver().openOutputStream(uri, "wt")) {
                    if (out != null) {
                        out.write(json.getBytes(StandardCharsets.UTF_8));
                        ok = true;
                    }
                } catch (Exception ignored) {}
                jsToast(ok ? "КОПИЯ СОХРАНЕНА" : "НЕ ПОЛУЧИЛОСЬ СОХРАНИТЬ КОПИЮ");
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

        @JavascriptInterface public boolean savePhoto(String id, String dataUrl) { return Store.write(Store.photoFile(MainActivity.this, id), dataUrl); }
        @JavascriptInterface public String loadPhoto(String id) { return Store.read(Store.photoFile(MainActivity.this, id)); }
        @JavascriptInterface public void deletePhoto(String id) { Store.photoFile(MainActivity.this, id).delete(); }

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

        @JavascriptInterface public void exportBackup(String fileName, String json) {
            runOnUiThread(() -> {
                pendingExport = json;
                Intent i = new Intent(Intent.ACTION_CREATE_DOCUMENT)
                        .addCategory(Intent.CATEGORY_OPENABLE)
                        .setType("application/json")
                        .putExtra(Intent.EXTRA_TITLE, fileName);
                try {
                    startActivityForResult(i, REQ_EXPORT);
                } catch (ActivityNotFoundException e) {
                    pendingExport = null;
                    jsToast("НЕТ ПРИЛОЖЕНИЯ ДЛЯ СОХРАНЕНИЯ ФАЙЛОВ");
                }
            });
        }
    }
}
