import time
import requests
import subprocess
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# The folder we are watching
WATCH_FOLDER = r"C:\Users\Omola\automation"
# The n8n Webhook URL
N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/automation-pulse"
# Path to our WhatsApp Robot
WHATSAPP_ROBOT = r"C:\Users\Omola\PulseAI\core\robots\whatsapp_pulse.py"

class PulseHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            filename = os.path.basename(event.src_path)
            print(f"🚀 New file detected: {filename}")
            
            # Check for the "Unthinkable" WhatsApp format: Contact_Message.txt
            if "_" in filename and filename.endswith(".txt"):
                print("📱 WhatsApp Trigger detected!")
                parts = filename.replace(".txt", "").split("_")
                contact = parts[0]
                message = parts[1]
                
                print(f"🤖 Shadow Robot is taking over to message {contact}...")
                subprocess.run(["python", WHATSAPP_ROBOT, contact, message])
            
            # Also send to n8n for our global logs
            try:
                requests.post(N8N_WEBHOOK_URL, json={
                    "event": "file_created",
                    "filename": filename,
                    "timestamp": time.time()
                })
            except:
                pass

if __name__ == "__main__":
    event_handler = PulseHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    
    print(f"🛡️  Global Empire Pulse is LIVE. Watching: {WATCH_FOLDER}")
    print("--------------------------------------------------")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
