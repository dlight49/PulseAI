import os
import json
import requests
import sys
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv

# --- PATH SAFETY ---
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

load_dotenv(dotenv_path=os.path.join(project_root, "config", ".env"))

HOST_NAME = "0.0.0.0"
SERVER_PORT = 5000

# Meta Cloud API Details
WHATSAPP_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN", "pulse_ai_secure_token")

# --- MESSAGE BUFFERING SYSTEM ---
# This keeps track of pending responses to allow for edits/multi-messages
# Format: { sender_id: {"timer": TimerObject, "text": "current text", "is_edit": False} }
message_buffer = {}
buffer_lock = threading.Lock()
RESPONSE_DELAY = 10.0 # Seconds to wait for customer to finish typing/editing

def send_whatsapp_message(to, text):
    """Sends a message via the Meta WhatsApp Cloud API."""
    if not WHATSAPP_TOKEN or not PHONE_NUMBER_ID:
        print("❌ Error: WHATSAPP_TOKEN or PHONE_NUMBER_ID not set!")
        return False

    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print(f"✅ Reply sent to {to}")
        return True
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False

def process_buffered_message(sender, business_id):
    """Wait period over. Actually call the AI brain and reply."""
    with buffer_lock:
        if sender not in message_buffer:
            return
        data = message_buffer.pop(sender)
        final_text = data['text']
        was_edited = data.get('is_edit', False)

    from core.ai_brain import get_ai_response
    
    # If it was an edit, we tell the brain so it can acknowledge it
    if was_edited:
        final_text = f"[CUSTOMER_EDITED_MESSAGE]: {final_text}"
        
    print(f"🧠 Brain activated for {sender} after buffer period...")
    ai_reply = get_ai_response(final_text, sender, business_id)
    
    if ai_reply == "[OWNER_APPROVAL_REQUIRED]":
        print(f"🚦 Message held for Owner Approval ({sender})")
    else:
        send_whatsapp_message(sender, ai_reply)

class WhatsAppWebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Verification handshake
        if self.path.startswith('/webhook'):
            from urllib.parse import urlparse, parse_qs
            query_components = parse_qs(urlparse(self.path).query)
            if query_components.get('hub.mode', [''])[0] == 'subscribe' and \
               query_components.get('hub.verify_token', [''])[0] == VERIFY_TOKEN:
                challenge = query_components.get('hub.challenge', [''])[0]
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(bytes(challenge, "utf-8"))
            else:
                self.send_response(403)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/webhook':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                if 'entry' in data and data['entry']:
                    changes = data['entry'][0].get('changes', [])
                    if changes and 'value' in changes[0]:
                        messages = changes[0]['value'].get('messages', [])
                        if messages:
                            msg = messages[0]
                            sender = msg.get('from')
                            
                            # Handle different message types (text vs edited)
                            msg_text = ""
                            is_edit = False
                            
                            if msg.get('type') == 'text':
                                msg_text = msg['text'].get('body', '')
                            elif msg.get('context', {}).get('referred_product'): # Example of other metadata
                                pass
                            
                            # Check for Edit (Meta sends 'context' with 'id' of original for edits)
                            if 'context' in msg and 'id' in msg['context']:
                                is_edit = True
                                print(f"📝 DETECTED EDIT from {sender}: {msg_text}")
                            
                            if not msg_text:
                                self.send_response(200)
                                self.end_headers()
                                return

                            print(f"\n📱 Received from {sender}: '{msg_text}' (Waiting {RESPONSE_DELAY}s for edits/more text...)")
                            
                            # --- BUFFER LOGIC ---
                            with buffer_lock:
                                # If a timer already exists, cancel it and restart
                                if sender in message_buffer:
                                    message_buffer[sender]['timer'].cancel()
                                    # If it's a new message, append to old text; if it's an edit, replace it.
                                    if is_edit:
                                        new_text = msg_text
                                    else:
                                        new_text = message_buffer[sender]['text'] + " " + msg_text
                                else:
                                    new_text = msg_text

                                # Set up new timer
                                business_id = "sample_product"
                                timer = threading.Timer(RESPONSE_DELAY, process_buffered_message, args=[sender, business_id])
                                message_buffer[sender] = {"timer": timer, "text": new_text, "is_edit": is_edit}
                                timer.start()
                            # --------------------
                
            except Exception as e:
                print(f"❌ Webhook POST Error: {e}")

            self.send_response(200)
            self.end_headers()

def run_server():
    print(f"Checking .env keys...")
    print(f"TOKEN: {'Set' if WHATSAPP_TOKEN else 'MISSING'}")
    print(f"ID: {'Set' if PHONE_NUMBER_ID else 'MISSING'}")

    webServer = HTTPServer((HOST_NAME, SERVER_PORT), WhatsAppWebhookHandler)
    print(f"📱 Pulse AI Webhook (Human Buffer) started at http://{HOST_NAME}:{SERVER_PORT}")
    print(f"Buffer period: {RESPONSE_DELAY} seconds.")
    
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()

if __name__ == "__main__":
    run_server()
