import os
import sys
import json
import requests
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

# --- CONSOLIDATED WORKER (No Redis Needed) ---
async def process_message_directly(sender: str, message_text: str, business_id: str, phone_number_id: str):
    """
    Handles the AI reasoning and WhatsApp reply within the same process.
    Perfect for Render's Free Tier.
    """
    try:
        print(f"🧠 Production Brain: Thinking for {sender}...")
        reply = get_ai_response(message_text, sender, business_id)
        
        url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {WHATSAPP_TOKEN}",
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
        print(f"✅ Production: Reply sent to {sender}")
    except Exception as e:
        print(f"❌ Production Worker Error: {e}")

# --- WEBHOOK ENDPOINTS ---

@app.get("/webhook")
async def verify(request: Request):
    params = request.query_params
    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == VERIFY_TOKEN:
        return int(params.get("hub.challenge"))
    return "Forbidden", 403

@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Receives message and immediately triggers internal background task.
    """
    payload = await request.json()
    
    if 'entry' in payload:
        for entry in payload['entry']:
            for change in entry['changes']:
                value = change.get('value', {})
                messages = value.get('messages', [])
                metadata = value.get('metadata', {})
                
                if messages:
                    message = messages[0]
                    sender = message.get('from')
                    phone_number_id = metadata.get('phone_number_id')
                    business_id = "senior_sales_demo" 
                    
                    msg_text = message['text'].get('body', '') if message.get('type') == 'text' else ""
                    
                    if msg_text:
                        print(f"📱 Webhook: Received from {sender}. Triggering internal worker...")
                        # Run in FastAPI background task (No separate worker needed!)
                        background_tasks.add_task(process_message_directly, sender, msg_text, business_id, phone_number_id)
                            
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    # Use $PORT provided by Render
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
