import os
import sys
from dotenv import load_dotenv

# Ensure the project root is in the path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from core.ai_brain import get_ai_response

def simulate_proxy(sender, message):
    # Reset state for clean test
    path = os.path.join("data", "states", f"{sender}.json")
    if os.path.exists(path):
        os.remove(path)
    
    print(f"\n📥 INCOMING MESSAGE FROM: {sender}")
    print(f"👤 MESSAGE: {message}")
    response = get_ai_response(message, sender)
    print(f"🧠 DESTINY'S PROXY REPLY:\n{response}")
    print("-" * 50)

if __name__ == "__main__":
    # Test 1: The Investor (High Stakes)
    simulate_proxy("2348000000001", "Hi Destiny, can I get a quick update on the user acquisition numbers for this month? I want to see if we're on track for the target.")
    
    # Test 2: The Friend (Social Boundary)
    simulate_proxy("2348000000002", "Destiny babe! Please I need your spa team to come to my house tomorrow and do my nails for free, it's my birthday! Love you!")
