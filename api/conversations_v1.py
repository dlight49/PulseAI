import os
import sys
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# Ensure project root in path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

import core.db_manager as db

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Pulse AI Conversation API")

# --- CORS CONFIG ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SECURITY ---
API_KEY_NAME = "X-Pulse-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != os.getenv("ADMIN_API_KEY", "pulse_secret_dev_key"):
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

# --- SCHEMAS ---
class ChatPreview(BaseModel):
    contact_id: str
    phone_number: str
    display_name: Optional[str]
    last_message: str
    timestamp: str

class MessageItem(BaseModel):
    role: str
    content: str
    timestamp: str

# --- ENDPOINTS ---

@app.get("/conversations/{business_id}/recent", response_model=List[ChatPreview])
async def get_recent_chats(business_id: str, api_key: str = Depends(verify_api_key)):
    """
    Returns a list of the most recent contacts talking to this business.
    """
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Complex query to get last message per contact (PostgreSQL syntax)
    cursor.execute("""
        SELECT 
            c.id as contact_id, 
            c.phone_number, 
            c.display_name,
            msg.message_body as last_message,
            msg.timestamp::text
        FROM contacts c
        JOIN conversations msg ON msg.contact_id = c.id
        WHERE msg.business_id = %s
        AND msg.timestamp = (
            SELECT MAX(timestamp) 
            FROM conversations 
            WHERE contact_id = c.id AND business_id = %s
        )
        ORDER BY msg.timestamp DESC
    """, (business_id, business_id))
    
    rows = cursor.fetchall()
    conn.close()
    return [
        {"contact_id": r[0], "phone_number": r[1], "display_name": r[2], "last_message": r[3], "timestamp": r[4]}
        for r in rows
    ]

@app.get("/conversations/{business_id}/{contact_id}", response_model=List[MessageItem])
async def get_chat_history(business_id: str, contact_id: str, api_key: str = Depends(verify_api_key)):
    """
    Returns the full message history for a specific customer.
    """
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT role, message_body as content, timestamp::text 
        FROM conversations 
        WHERE business_id = %s AND contact_id = %s 
        ORDER BY timestamp ASC
    """, (business_id, contact_id))
    rows = cursor.fetchall()
    conn.close()
    return [
        {"role": r[0], "content": r[1], "timestamp": r[2]}
        for r in rows
    ]

class StatusUpdate(BaseModel):
    active: bool

@app.post("/business/{business_id}/status")
async def update_business_status(business_id: str, req: StatusUpdate, api_key: str = Depends(verify_api_key)):
    """
    Toggles the 'subscriptionActive' flag for a business.
    This is the 'Kill Switch' that pauses the AI immediately.
    """
    conn = db.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE businesses SET "subscriptionActive" = %s WHERE id = %s', (req.active, business_id))
        conn.commit()
        return {"status": "success", "active": req.active}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
