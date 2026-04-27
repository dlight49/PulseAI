import os
from google import genai
from dotenv import load_dotenv

# Load secure tokens
load_dotenv(dotenv_path=r"C:\Users\Omola\PulseAI\config\.env")

# Pulse AI: Pitch Generator
# This script uses Gemini to write unique, 3-paragraph pitches for prospects.

def generate_pitch(prospect_data, deep_study_data=None):
    print(f"✍️  Generating hyper-personalized pitch for {prospect_data['name']}...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY is not set in config/.env")
        return None

    client = genai.Client(api_key=api_key)
    
    # Using Gemini 1.5 Pro (The Master Brain)
    model_id = 'gemini-1.5-pro'
    
    context_data = f"""
    Prospect Details:
    - Business Name: {prospect_data.get('name')}
    - Niche: {prospect_data.get('niche', 'Unknown')}
    - URL: {prospect_data.get('url', 'N/A')}
    """

    if deep_study_data:
        context_data += f"\nDeep Study Analysis:\n{deep_study_data}"

    prompt = f"""
    You are Pulse AI, an elite Sales Executive. 
    Your goal is to write a 3-paragraph outreach pitch that feels like it was written after 2 hours of research.
    
    {context_data}
    
    Pulse AI Value Proposition: We deploy autonomous sales agents that handle WhatsApp/Instagram leads, book appointments, and close sales 24/7 using the business's own brand voice.

    Requirements:
    1. The Hook: Reference a specific detail from their business or the "Pulse Gap" identified in the study.
    2. The Solution: Explain how Pulse AI specifically solves their unique problem (e.g., if they have a complex booking flow, mention our auto-booking integration).
    3. The Close: A bold, high-confidence but low-friction invite to a 5-minute "Growth Audit".
    
    Tone: Professional, Nigerian-business savvy (persuasive but respectful), and technologically elite.
    """
    
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=prompt
        )
        print("\n✨ [PULSE AI] Hyper-Personalized Pitch Generated:\n")
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
