import os
from google import genai
from dotenv import load_dotenv

# Load secure tokens
load_dotenv(dotenv_path=r"C:\Users\Omola\PulseAI\config\.env")

def list_compatible_models():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY is not set in config/.env")
        return

    client = genai.Client(api_key=api_key)
    
    print("🛰️  Scanning for available Pulse AI Brain models...")
    print("--------------------------------------------------")
    
    try:
        # Use simple iteration for the modern client
        for model in client.models.list():
            print(f"✅ Model ID: {model.name}")
            print(f"   Name: {model.display_name}")
            print("---")
    except Exception as e:
        print(f"❌ Error listing models: {e}")
    
    print("--------------------------------------------------")

if __name__ == "__main__":
    list_compatible_models()
