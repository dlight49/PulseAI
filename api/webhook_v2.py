import os
import sys
import json
import requests
import asyncio
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Ensure project root in path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

import core.db_manager as db
from core.ai_brain import get_ai_response

# Load config
load_dotenv(dotenv_path=os.path.join(project_root, "config", ".env"))

app = FastAPI(title="Pulse AI All-in-One Production")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN", "pulse_ai_secure_token")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
BUFFER_SECONDS = 10.0

# --- IN-MEMORY BUFFER ---
# For a single-instance Render deploy, this works perfectly.
# sender_id -> {"text": str, "last_updated": float, "phone_id": str}
message_buffer = {}

async def wait_and_process(sender: str):
    """
    The Human Buffer: Wait for the customer to finish typing multiple messages or edits.
    Enables multi-tenancy by resolving business-specific tokens from the database.
    """
    await asyncio.sleep(BUFFER_SECONDS)
    
    if sender not in message_buffer:
        return
        
    data = message_buffer.pop(sender)
    final_text = data['text']
    phone_id = data['phone_id']
    
    # Resolve Business dynamically from Database
    business = db.get_business_by_phone_id(phone_id)
    if not business:
        print(f"❌ Error: No business found for Phone ID {phone_id}")
        return
        
    # THE KILL SWITCH CHECK
    if not business.get('subscriptionActive', True):
        print(f"🚦 Message held: {business['name']} has paused their AI (Kill Switch Active).")
        return

    business_id = business['id']
    # Decrypt business-specific token
    encrypted_token = business.get('whatsappAccessToken')
    if not encrypted_token:
        print(f"❌ Error: No WhatsApp Token found for business {business['name']}")
        return
        
    try:
        whatsapp_token = db.decrypt_token(encrypted_token)
    except Exception as e:
        print(f"❌ Decryption Error for {business['name']}: {e}")
        return
    
    try:
        print(f"🧠 Pulse Brain: Processing for {sender} ({business['name']})...")
        reply = get_ai_response(final_text, sender, business_id)
        
        # Send Reply via Meta API using business-specific token
        url = f"https://graph.facebook.com/v18.0/{phone_id}/messages"
        headers = {
            "Authorization": f"Bearer {whatsapp_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": sender,
            "type": "text",
            "text": {"body": reply}
        }
        
        res = requests.post(url, json=payload, headers=headers)
        res.raise_for_status()
        print(f"✅ Reply delivered to {sender}")
    except Exception as e:
        print(f"❌ Worker Error: {e}")

# --- WEBHOOK ENDPOINTS ---

@app.get("/webhook")
async def verify(request: Request):
    params = request.query_params
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == VERIFY_TOKEN:
        try:
            return int(params.get("hub.challenge"))
        except:
            return params.get("hub.challenge")
    return "Forbidden", 403

@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    raw_body = await request.body()
    try:
        payload = json.loads(raw_body.decode('utf-8'))
    except Exception as e:
        print(f"❌ JSON Parse Error: {e}")
        print(f"📄 Raw Body: {raw_body.decode('utf-8', errors='replace')}")
        return {"status": "error", "message": "invalid json"}, 400
    
    if 'entry' in payload:
        for entry in payload['entry']:
            for change in entry['changes']:
                value = change.get('value', {})
                messages = value.get('messages', [])
                metadata = value.get('metadata', {})
                
                if messages:
                    message = messages[0]
                    sender = message.get('from')
                    phone_id = metadata.get('phone_number_id')
                    
                    msg_text = ""
                    if message.get('type') == 'text':
                        msg_text = message['text'].get('body', '')
                    
                    if msg_text:
                        print(f"📱 Received from {sender}. Buffering...")
                        
                        # Buffer Logic
                        if sender in message_buffer:
                            message_buffer[sender]['text'] += " " + msg_text
                        else:
                            message_buffer[sender] = {"text": msg_text, "phone_id": phone_id}
                            # Start the wait timer in background
                            background_tasks.add_task(wait_and_process, sender)
                            
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
