from kivy.app import App
from kivy.uix.webview import WebView
from kivy.clock import Clock
import subprocess, os, threading, time
from pathlib import Path

HOME = Path(os.environ.get("HOME","/data/data/com.termux/files/home"))

def start_aether():
    time.sleep(3)
    subprocess.Popen([
        "python", str(HOME/"aether"/"aether_stream.py")
    ])

class AetherApp(App):
    def build(self):
        threading.Thread(target=start_aether, daemon=True).start()
        Clock.schedule_once(self.load_web, 5)
        self.web = WebView(url="http://localhost:5000")
        return self.web

    def load_web(self, dt):
        self.web.url = "http://localhost:5000"

if __name__ == "__main__":
    AetherApp().run()
