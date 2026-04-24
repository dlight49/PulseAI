import os
from google import genai
from dotenv import load_dotenv

# Load secure tokens
load_dotenv(dotenv_path=r"C:\Users\Omola\PulseAI\config\.env")

# Pulse AI: Pitch Generator
# This script uses Gemini to write unique, 3-paragraph pitches for prospects.

def generate_pitch(prospect_data):
    print(f"✍️  Generating personalized pitch for {prospect_data['name']}...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY is not set in config/.env")
        return None

    client = genai.Client(api_key=api_key)
    
    # Using Gemini 1.5 Pro (The Master Brain) as specified in Phase 1
    model_id = 'gemini-1.5-pro'
    
    prompt = f"""
    You are Pulse AI, the world-class inbound sales agent for my company.
    Write a unique, highly personalized 3-paragraph outreach pitch for the following prospect.
    Do NOT use templates. Speak directly to their specific business.
    
    Prospect Details:
    - Business Name: {prospect_data.get('name')}
    - Niche: {prospect_data.get('niche', 'Unknown')}
    - Context: We help businesses automate their lead generation and sales using AI.
    
    Requirements:
    1. Hook them based on their business name/niche.
    2. Explain the value of AI automation simply (No tech jargon).
    3. End with a soft, low-friction Call to Action (e.g., a quick 5-min chat).
    """
    
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=prompt
        )
        print("\n✨ [PULSE AI] Pitch Generated Successfully:\n")
        print("--------------------------------------------------")
        print(response.text)
        print("--------------------------------------------------")
        return response.text
    except Exception as e:
        print(f"❌ Error generating pitch: {e}")
        return None

if __name__ == "__main__":
    # Testing with a real-world scenario
    test_prospect = {
        "name": "Lagos Tech Real Estate",
        "niche": "High-end real estate agency"
    }
    generate_pitch(test_prospect)
