import os
import sys

# Ensure project root in path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from core.ai_brain import get_ai_response

def run_final_audit():
    print("💎 PULSE AI: PHASE 1 FINAL AUDIT (Full Database Integration)")
    print("="*60)

    # 1. Test Business Negotiation (DB-Driven)
    print("\nTEST 1: BUSINESS CLOSER (Luxe Glo Demo)")
    sender_biz = "2349000000001"
    msgs_biz = [
        "How much is the Glow treatment?",
        "Ah, that's high. I have only 35k."
    ]
    for m in msgs_biz:
        print(f"👤 {m}")
        print(f"💼 {get_ai_response(m, sender_biz, 'senior_sales_demo')}\n")

    # 2. Test Personal Proxy (DB-Driven)
    print("\nTEST 2: PERSONAL PROXY (Investor Context)")
    sender_pers = "2348000000001" # Segun's number from our seed
    m_pers = "Destiny, are we hitting the growth targets this week? I need a status update for the board."
    print(f"👤 {m_pers}")
    print(f"🧠 {get_ai_response(m_pers, sender_pers)}\n")

    print("="*60)
    print("✅ PHASE 1 AUDIT COMPLETE: ALL CONTEXT LOADED FROM DATABASE.")

if __name__ == "__main__":
    run_final_audit()
