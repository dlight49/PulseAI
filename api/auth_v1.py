import os
import sys
import uuid
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Ensure project root in path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

import core.db_manager as db

app = FastAPI(title="Pulse AI Auth & Onboarding API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SignupRequest(BaseModel):
    business_name: str
    owner_email: str

@app.post("/onboard/signup")
async def signup_business(req: SignupRequest):
    """
    Creates a new business entry in the Master SQL Database.
    This is Step 1 of the scaling roadmap.
    """
    business_id = str(uuid.uuid4())
    conn = db.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO businesses (id, name, persona_prompt, competitive_edge)
            VALUES (?, ?, ?, ?)
        ''', (
            business_id, 
            req.business_name,
            "You are a Senior Sales Lead. Professional and persuasive.",
            "Quality service guaranteed."
        ))
        conn.commit()
        return {"status": "success", "business_id": business_id}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.post("/onboard/connect-whatsapp/{business_id}")
async def save_whatsapp_token(business_id: str, token: str, phone_id: str):
    """
    Saves the Meta Access Token after the handshake is complete.
    This makes the AI live for that specific business.
    """
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE businesses 
        SET whatsapp_access_token = ?, whatsapp_phone_id = ?
        WHERE id = ?
    ''', (token, phone_id, business_id))
    conn.commit()
    conn.close()
    return {"status": "connected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
