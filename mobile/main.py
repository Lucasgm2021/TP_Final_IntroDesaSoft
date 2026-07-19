from kivy.app import App
from kivy.utils import platform
from kivy.uix.widget import Widget

if platform == 'android':
    from android.run_on_ui_thread import run_on_ui_thread
    from jnius import autoclass
else:
    # Dummy decorator so the app doesn't crash if you run it on your PC
    def run_on_ui_thread(func):
        return func

class WebViewApp(App):
    def build(self):
        if platform == 'android':
            # Schedule the WebView creation on the correct thread
            self.create_webview_on_ui()
            
            # Kivy always requires a root widget returned from build().
            # Since the WebView will cover the screen, we return a blank Widget.
            return Widget()
        else:
            # Fallback text if you run it on your desktop computer during testing
            from kivy.uix.label import Label
            return Label(text="Android WebView only works when compiled into an APK!")

    @run_on_ui_thread
    def create_webview_on_ui(self):
        # This function runs completely on the native Android UI thread
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        
        activity = PythonActivity.mActivity
        
        # Safe to initialize now that we are on the UI thread
        self.webview = WebView(activity)
        self.webview.getSettings().setJavaScriptEnabled(True)
        self.webview.setWebViewClient(WebViewClient())
        
        # Point it to your existing frontend URL
        self.webview.loadUrl('https://tp-final-introdesasoft-1.onrender.com/puerto-hermoso/')
        
        # Set the mobile screen content to be this web view
        activity.setContentView(self.webview)

    def on_pause(self):
        return True

if __name__ == '__main__':
    WebViewApp().run()