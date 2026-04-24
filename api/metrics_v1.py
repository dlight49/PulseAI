import os
import sys
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from typing import List, Optional
from pydantic import BaseModel
from decimal import Decimal

# Ensure project root in path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

import core.db_manager as db

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Pulse AI Metrics & Revenue API")

# --- CORS CONFIG ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, we'll restrict this to pulse-ai.app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SECURITY ---
API_KEY_NAME = "X-Pulse-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def verify_api_key(api_key: str = Security(api_key_header)):
    # In production, we'd check this against the 'businesses' table in the DB
    if api_key != os.getenv("ADMIN_API_KEY", "pulse_secret_dev_key"):
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

# --- SCHEMAS ---
class BusinessSummary(BaseModel):
    business_name: str
    total_revenue: Decimal
    deals_closed: int
    pending_revenue: Decimal
    active_conversations: int

class TransactionItem(BaseModel):
    id: str
    amount: Decimal
    status: str
    reference: str
    created_at: str

# --- ENDPOINTS ---

@app.get("/metrics/{business_id}/summary", response_model=BusinessSummary)
async def get_business_summary(business_id: str, api_key: str = Depends(verify_api_key)):
    """
    Returns the high-level ROI stats for a business owner.
    """
    business = db.get_business(business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
        
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # 1. Calculate Revenue (With COALESCE to handle NULL/None)
    cursor.execute("""
        SELECT 
            COALESCE(SUM(CASE WHEN status = 'PAID' THEN amount ELSE 0 END), 0) as revenue,
            COALESCE(SUM(CASE WHEN status = 'PENDING' THEN amount ELSE 0 END), 0) as pending,
            COUNT(CASE WHEN status = 'PAID' THEN 1 END) as closed_deals
        FROM transactions 
        WHERE business_id = %s
    """, (business_id,))
    res = cursor.fetchone()
    
    # 2. Get Conversation Count
    cursor.execute("SELECT COUNT(DISTINCT contact_id) FROM conversations WHERE business_id = %s", (business_id,))
    conv_count = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "business_name": business['name'],
        "total_revenue": Decimal(str(res[0] or 0)),
        "pending_revenue": Decimal(str(res[1] or 0)),
        "deals_closed": res[2] or 0,
        "active_conversations": conv_count
    }

@app.get("/metrics/{business_id}/transactions", response_model=List[TransactionItem])
async def get_transactions(business_id: str, api_key: str = Depends(verify_api_key)):
    """
    Returns a detailed list of all sales attempts made by the AI.
    """
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, amount, status, reference, created_at FROM transactions WHERE business_id = %s ORDER BY created_at DESC", (business_id,))
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {"id": r[0], "amount": Decimal(str(r[1])), "status": r[2], "reference": r[3], "created_at": str(r[4])} 
        for r in rows
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
