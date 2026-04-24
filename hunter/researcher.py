import os
import requests
from dotenv import load_dotenv

# Load secure tokens
load_dotenv(dotenv_path=r"C:\Users\Omola\PulseAI\config\.env")

# Pulse AI: Autonomous Researcher
# This script finds prospects based on a niche using the Tavily Search API.

def find_prospects(niche, location):
    print(f"🔍 Searching for '{niche}' in {location}...")
    
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        print("❌ Error: TAVILY_API_KEY is not set in config/.env")
        print("💡 Hint: Get a free API key at https://tavily.com and add it to your .env file.")
        return []

    query = f"{niche} in {location}"
    
    url = "https://api.tavily.com/search"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "api_key": tavily_api_key,
        "query": query,
        "search_depth": "basic",
        "include_answer": False,
        "include_images": False,
        "include_raw_content": False,
        "max_results": 5
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        prospects = []
        for result in data.get("results", []):
            prospect = {
                "name": result.get("title", "Unknown Business"),
                "niche": niche,
                "url": result.get("url", ""),
                "description": result.get("content", "")
            }
            prospects.append(prospect)
            
        print(f"✅ Found {len(prospects)} prospects!")
        for p in prospects:
            print(f"- {p['name']} ({p['url']})")
            
        return prospects
        
    except Exception as e:
        print(f"❌ Error during search: {e}")
        return []

if __name__ == "__main__":
    # Test the researcher
    found_prospects = find_prospects("High-end real estate agency", "Lagos Nigeria")
    
    # Connect to pitch generator to test the full "Hunter" flow
    if found_prospects:
        try:
            from pitch_generator import generate_pitch
            print("\n🚀 Passing first prospect to Pitch Generator...\n")
            # Enhance the prospect data for the pitch generator
            first_prospect = found_prospects[0]
            # Add description context to niche so the pitch is more personalized
            first_prospect['niche'] = f"{first_prospect['niche']} - Context: {first_prospect['description'][:100]}..."
            generate_pitch(first_prospect)
        except ImportError:
            print("❌ Could not import pitch_generator.py")
