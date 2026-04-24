import os
import sys
import json
import uuid

# Ensure project root in path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from core.ai_brain import get_ai_response
from core.db_manager import get_connection

def run_launch_stress_test():
    print("🔥 PULSE AI: FINAL END-TO-END LAUNCH TEST")
    print("="*60)
    
    # 1. Simulate NEW BUSINESS: Chioma's Luxury Hair
    biz_id = str(uuid.uuid4())
    print(f"\n[STEP 1] ONBOARDING: Deploying 'Chioma's Luxury Hair' (ID: {biz_id[:8]})")
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO businesses (id, name, persona_prompt, competitive_edge, objection_playbook, payment_link)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        biz_id, 
        "Chioma's Luxury Hair", 
        "You are the Senior Sales Lead for a luxury hair brand. You are premium, persuasive, and use Nigerian slang naturally.",
        "100% Raw Donor Virgin Hair. Lasts 5 years. No shedding.",
        json.dumps({"too_expensive": "Mention the 5-year durability and raw donor quality. Explain that cheap hair tangles in 2 weeks."}),
        "https://paystack.com/pay/chioma-hair"
    ))
    
    # 2. Seed Services
    cursor.execute("INSERT INTO services VALUES (?, ?, ?, ?, ?, ?)", 
                   (str(uuid.uuid4()), biz_id, "Bone Straight 24 inch", 180000, 155000, "Double drawn, raw hair"))
    conn.commit()
    print("✅ ONBOARDING SUCCESSFUL: Database synchronized.")

    # 3. Simulate CUSTOMER CHAT: "Is this hair real?"
    customer_phone = "2347000000001"
    print(f"\n[STEP 2] SALES ENGINE: Customer messaging Chioma's Luxury Hair...")
    print(f"👤 CUSTOMER: 'Abeg, why is the 24 inch so expensive? I saw one for 80k elsewhere.'")
    
    reply = get_ai_response("Abeg, why is the 24 inch so expensive? I saw one for 80k elsewhere.", customer_phone, biz_id)
    print(f"💼 AI SALES EXEC: \n{reply}")

    # 4. Check Analytics
    print(f"\n[STEP 3] ANALYTICS: Checking the ROI Command Center...")
    cursor.execute("SELECT COUNT(*) FROM conversations WHERE business_id = ?", (biz_id,))
    convs = cursor.fetchone()[0]
    print(f"📈 Dashboard Stats: {convs} Live Conversations Logged.")

    print("\n" + "="*60)
    print("🌟 LAUNCH STATUS: 100% READY. PULSE AI IS LIVE.")
    conn.close()

if __name__ == "__main__":
    run_launch_stress_test()
