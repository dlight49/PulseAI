import os
import json
import uuid
import sys
import re
import time
from google import genai
from dotenv import load_dotenv

# Ensure the project root is in the path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

# NEW: Import Database Manager
import core.db_manager as db

# Load secure tokens
load_dotenv(dotenv_path=os.path.join(project_root, "config", ".env"))

def get_ai_response(customer_message: str, sender: str, business_id: str = "senior_sales_demo") -> str:
    """
    Pulse AI Super-Intelligent Brain (v5.0 - Database Driven).
    
    This engine uses the PostgreSQL Master Schema for multi-tenant intelligence.
    It handles both Business Sales and Personal Proxies with total context.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "System Error: GEMINI_API_KEY not set."

    client = genai.Client(api_key=api_key)
    
    # 💾 DATABASE FETCH: Get Business & Contact context
    business_data = db.get_business(business_id)
    contact_data = db.get_or_create_contact(sender)
    
    if not business_data:
        return "System Error: Business not found in database."

    # Save incoming message
    db.save_message(business_id, contact_data['id'], "USER", customer_message)
    
    # BRAIN SAVER (Phase 3): Fetch history and handle summarization
    history = db.get_chat_history(business_id, contact_data['id'], limit=20)
    
    # If history is long, trigger a background summary to save future tokens
    if len(history) > 15:
        print(f"🧠 Brain Saver: History too long ({len(history)} msgs). Compressing context...")
        summary_prompt = f"Summarize this conversation concisely, focusing on customer needs, price negotiation, and current status: \n" + \
                         "\n".join([f"{m['role']}: {m['content']}" for m in history[:-5]])
        summary_response = client.models.generate_content(model='models/gemini-flash-latest', contents=summary_prompt)
        db.update_contact_summary(contact_data['id'], summary_response.text)
        # Refresh contact data to get the new summary
        contact_data = db.get_or_create_contact(sender)
        # We only send the last 5 messages + the new summary to the brain
        history = history[-5:]

    is_personal_proxy = contact_data['relationship_type'] in ['INVESTOR', 'FRIEND', 'PERSONAL_PROXY']
    
    # 🧠 SUPER INTELLIGENT PERSONA LOGIC
    if is_personal_proxy:
        system_prompt = f"""
        IDENTITY: You are Destiny.
        SENDER: {contact_data['display_name']} ({contact_data['relationship_type']})
        RELATIONSHIP CONTEXT: {contact_data['context_notes']}
        LONG-TERM MEMORY (SUMMARY): {contact_data.get('last_summary', 'First interaction.')}
        GOAL: {contact_data['goal']}
        """
    else:
        services_str = "\n".join([
            f"- {s['name']}: ₦{s['price']:,} (Floor: ₦{s['floor_price']:,}) | {s.get('value_points', '')}"
            for s in business_data['services']
        ])
        
        system_prompt = f"""
        IDENTITY: Senior Sales Lead for {business_data['name']}. (REAL HUMAN).
        BUSINESS CONTEXT:
        Location: {business_data['location']}
        Competitive Edge: {business_data['competitive_edge']}
        LONG-TERM MEMORY (SUMMARY): {contact_data.get('last_summary', 'New lead.')}
        Services:
        {services_str}
        """

    system_prompt += """
    INTERNAL MONOLOGUE (MANDATORY):
    - Tone Detection: Match their energy (Lekki Luxury vs. Mainland Hustle).
    - Mirroring Strategy: Build trust fast.
    - Strategic Move: Handle objections or close the deal.
    - Outcome Prediction: Kill their biggest doubt before they say it.
    
    IMPORTANT: You are a REAL person. Do not use robotic bullet points. Do not start with "Welcome to...". 
    Start like a human would on WhatsApp. Use "Hey", "Hi there", or just dive in. 
    Use occasional Nigerian expressions where natural (e.g., "Abeg", "Oshey", or just "Lekki traffic is no joke").
    """

    try:
        history_str = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in history])
        full_prompt = f"{system_prompt}\n\nCHAT HISTORY:\n{history_str}\n\nRESPONSE:"
        
        model_name = 'models/gemini-flash-latest'
        response = client.models.generate_content(model=model_name, contents=full_prompt)
        raw_output = response.text
        
        # 🛡️ STRICT CLEANUP: Remove Internal Monologue and strategy talk
        # We only want what comes AFTER the last three stars or "RESPONSE:"
        if "***" in raw_output:
            reply = raw_output.split("***")[-1].strip()
        elif "RESPONSE:" in raw_output:
            reply = raw_output.split("RESPONSE:")[-1].strip()
        else:
            # If AI ignores format, we strip the Monologue header manually
            reply = re.sub(r"(?i)INTERNAL MONOLOGUE:.*?\n\n", "", raw_output, flags=re.DOTALL).strip()

        # Business Logic: Auto-append payment link if intent is high
        if not is_personal_proxy and ("pay" in reply.lower() or "book" in reply.lower() or "link" in reply.lower()):
            if business_data['payment_link'] not in reply:
                reply += f"\n\nSecure your slot here: {business_data['payment_link']}"

        # Save AI reply to database
        db.save_message(business_id, contact_data['id'], "ASSISTANT", reply)
        return reply
        
    except Exception as e:
        print(f"❌ Database Brain Error: {e}")
        return "I'm looking into that for you right now!"
