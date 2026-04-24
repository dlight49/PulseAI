import os
import sys
from dotenv import load_dotenv

# Ensure the project root is in the path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from core.ai_brain import get_ai_response

def simulate_ultimate_test(message):
    sender = "2349000000001" # New random customer
    business_id = "senior_sales_demo"
    
    # Reset state
    path = os.path.join("data", "states", f"{sender}.json")
    if os.path.exists(path):
        os.remove(path)
    
    print(f"🔥 ULTIMATE HUMAN-PASSING TEST: {business_id}")
    print(f"👤 CUSTOMER: {message}")
    response = get_ai_response(message, sender, business_id)
    print(f"🧠 SUPER INTELLIGENT REPLY:\n{response}")
    print("-" * 50)

if __name__ == "__main__":
    simulate_ultimate_test("How much for the glow treatment? 45k is too much abeg. My sister did her own for 25k last week.")
