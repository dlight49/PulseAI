import os
import sys
import time
import json
from unittest.mock import MagicMock

# Path safety
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

# Mock core.db_manager BEFORE importing ai_brain
import core.db_manager as db
db.get_business = MagicMock(return_value={
    "id": "senior_sales_demo",
    "name": "Luxe Glo Beauty & Spa",
    "location": "Lekki Phase 1, Lagos",
    "competitive_edge": "We use only imported organic oils from France. Our treatments are 90 mins.",
    "payment_link": "https://paystack.com/pay/luxeglo-deposit",
    "services": [
        {"name": "Full Body Glow Treatment", "price": 45000, "floor_price": 38000, "value_points": "90 mins, French Oils"},
        {"name": "Express Hydrating Facial", "price": 25000, "floor_price": 20000, "value_points": "Deep hydration"}
    ]
})
db.get_or_create_contact = MagicMock(return_value={
    "id": "test_contact_uuid",
    "phone_number": "2348149084806",
    "display_name": "Prospective Client",
    "relationship_type": "LEAD",
    "context_notes": "Interested in premium spa services.",
    "last_summary": "First interaction."
})
db.save_message = MagicMock()
db.get_chat_history = MagicMock(return_value=[])

from core.ai_brain import get_ai_response

def test_prototype():
    print("🔥 PULSE AI: WHATSAPP MVP SIMULATOR")
    print("="*50)
    
    # Simulate the "Human Buffer" (Multi-part message)
    print("\n[STEP 1] Simulating Human Buffer...")
    print("📱 User is typing: 'Hi, I want to ask about the glow treatment...'")
    time.sleep(1)
    print("📱 User is typing: 'And is it possible to get a discount?'")
    
    combined_message = "Hi, I want to ask about the glow treatment... And is it possible to get a discount?"
    print(f"\n[STEP 2] Buffer Closed. Final Text: '{combined_message}'")
    
    print("\n[STEP 3] Triggering Master Brain...")
    print("🧠 Thinking...")
    
    # We use a real call to Gemini here (requires GEMINI_API_KEY in .env)
    try:
        reply = get_ai_response(combined_message, "2348149084806", "senior_sales_demo")
        
        print("\n" + "="*50)
        print("💬 PULSE AI RESPONSE:")
        print("-" * 50)
        print(reply)
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ Error during AI generation: {e}")
        print("💡 Check if your GEMINI_API_KEY is correct in config/.env")

if __name__ == "__main__":
    test_prototype()
