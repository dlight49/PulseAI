import os
import sys
from dotenv import load_dotenv

# Ensure the project root is in the path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from core.ai_brain import get_ai_response, load_state, save_state

def simulate_chat(messages):
    sender = "2348149084806" # Test number
    business_id = "senior_sales_demo"
    
    # Reset state for clean test
    path = os.path.join("data", "states", f"{sender}.json")
    if os.path.exists(path):
        os.remove(path)
    
    print(f"🚀 STARTING SALES SIMULATION: {business_id}\n" + "="*50)
    
    for msg in messages:
        print(f"\n👤 CUSTOMER: {msg}")
        response = get_ai_response(msg, sender, business_id)
        print(f"💼 EXECUTIVE: {response}")
        print("-" * 30)

if __name__ == "__main__":
    # Test Scenarios
    test_msgs = [
        "Hi, how much is your Full Body Glow Treatment?",
        "That's a bit expensive for me. Can you do 35k?",
        "Okay, 38k is fair. How do I book it?"
    ]
    
    simulate_chat(test_msgs)
