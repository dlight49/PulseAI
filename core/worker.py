import os
import sys
import json
import uuid
import requests
from celery import Celery
from dotenv import load_dotenv

# Ensure project root in path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from core.ai_brain import get_ai_response

load_dotenv(dotenv_path=os.path.join(project_root, "config", ".env"))

# --- CELERY CONFIG (The Redis Broker) ---
# This is the "Delivery Van" that moves messages from Webhook to Brain
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("pulse_ai_workers", broker=REDIS_URL)

WHATSAPP_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")

@celery_app.task(name="process_whatsapp_message")
def process_whatsapp_message(sender: str, message_text: str, business_id: str, phone_number_id: str):
    """
    This is the Worker Task. 
    It runs in a separate process/container.
    If the Webhook crashes, this worker keeps going.
    """
    print(f"📦 Worker: Processing queued message for {sender}...")
    
    # 1. Get the High-Level AI Reply
    reply = get_ai_response(message_text, sender, business_id)
    
    # 2. Send back to WhatsApp
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
    
    try:
        res = requests.post(url, json=payload, headers=headers)
        res.raise_for_status()
        print(f"✅ Worker: Reply sent successfully to {sender}")
    except Exception as e:
        print(f"❌ Worker Error: Failed to send reply: {e}")

if __name__ == "__main__":
    # To run: celery -A core.worker worker --loglevel=info
    celery_app.start()
