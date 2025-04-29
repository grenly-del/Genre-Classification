import subprocess
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FlaskReloader(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py"):  # Deteksi perubahan file Python
            print(f"Change detected in {event.src_path}. Restarting Flask...")
            subprocess.run([sys.executable, 'app.py'])  # Menjalankan kembali app.py

if __name__ == "__main__":
    event_handler = FlaskReloader()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)  # Monitor direktori saat ini
    observer.start()
    
    try:
        while True:
            time.sleep(1)  # Tunggu perubahan file
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
