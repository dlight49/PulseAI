import os
import requests
import json
from dotenv import load_dotenv
from google import genai

# Path safety
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
load_dotenv(dotenv_path=os.path.join(project_root, "config", ".env"))

# Pulse AI: Deep Study Engine
# This script "visits" the prospect's site and extracts their DNA.

def deep_study(prospect_url):
    print(f"🕵️  Deep Studying: {prospect_url}...")
    
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not tavily_api_key or not gemini_api_key:
        return "Missing API keys for deep study."

    # Step 1: Extract content using Tavily
    url = "https://api.tavily.com/extract"
    payload = {
        "api_key": tavily_api_key,
        "urls": [prospect_url]
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        raw_content = data.get("results", [{}])[0].get("raw_content", "")
        
        if not raw_content:
            return "Could not extract content from the website."
            
        print(f"📄 Extracted {len(raw_content)} characters. Analyzing with Gemini...")

        # Step 2: Use Gemini to summarize USPs and Pain Points
        client = genai.Client(api_key=gemini_api_key)
        
        analysis_prompt = f"""
        Analyze the following raw website content of a business. 
        Extract the following:
        1. Their Core Services/Products.
        2. Their Tone of Voice (e.g., Luxury, Bold, Friendly).
        3. A "Pulse Gap": One specific thing they are missing (e.g., slow response time, no clear booking system, outdated pitch).
        
        Content:
        {raw_content[:15000]}  # Limiting to 15k chars for token efficiency
        """
        
        analysis = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=analysis_prompt
        )
        
        return analysis.text
        
    except Exception as e:
        return f"Error during deep study: {e}"

if __name__ == "__main__":
    # Test with a sample URL
    test_url = "https://www.interswitchgroup.com/" # Sample Nigerian Tech Company
    result = deep_study(test_url)
    print("\n🔍 --- DEEP STUDY REPORT ---")
    print(result)
