import os
import sys
import json
import hmac
import hashlib
from fastapi import FastAPI, Request, Response, HTTPException, BackgroundTasks
from pydantic import BaseModel
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

app = FastAPI(title="Pulse AI Enterprise Webhook")

VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN", "pulse_ai_secure_token")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")

# Fallback to background tasks if Celery/Redis is not available for testing
USE_CELERY = os.getenv("USE_CELERY", "False").lower() == "true"

@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):
    """
    High-speed receiver. 
    It identifies the business and pushes the message to a Task Queue.
    """
    payload = await request.json()
    
    try:
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
                            if USE_CELERY:
                                # Production: Push to Redis
                                from core.worker import process_whatsapp_message
                                process_whatsapp_message.delay(sender, msg_text, business_id, phone_number_id)
                            else:
                                # Development/Mock: Use FastAPI Background Tasks
                                from api.webhook_v2 import process_message_task_mock
                                background_tasks.add_task(process_message_task_mock, sender, msg_text, business_id, phone_number_id)
                            
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

async def process_message_task_mock(sender: str, message_text: str, business_id: str, phone_number_id: str):
    """Mock worker for local testing."""
    # We just log it for the stress test
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)
