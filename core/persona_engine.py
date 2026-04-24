import os
import sys
import json

# Ensure project root in path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

import core.db_manager as db

def load_business_data(business_id="senior_sales_demo"):
    """
    DEPRECATED: Old JSON-based loading. 
    Now calls the Database Manager directly.
    """
    return db.get_business(business_id)

def get_business_prompt_context(business_data):
    """
    Formats database-sourced business data into a context string for the AI.
    This provides the 'Super Intelligence' for the Senior Sales Executive.
    """
    if not business_data:
        return "System Error: Business data missing."
        
    context = f"""
    Business Name: {business_data['name']}
    Type: {business_data['type']}
    Location: {business_data['location']}
    Competitive Edge: {business_data['competitive_edge']}
    Objection Playbook: {json.dumps(business_data.get('objection_playbook', {}))}
    """
    
    context += "\nServices & Pricing (Target vs Floor):\n"
    for service in business_data.get('services', []):
        context += f"- {service['name']}: ₦{service['price']:,} (Floor: ₦{service['floor_price']:,})\n"
        context += f"  Value Points: {service.get('value_points', 'N/A')}\n"
        
    return context

if __name__ == "__main__":
    # Test DB-driven context generation
    data = load_business_data("senior_sales_demo")
    if data:
        print("✅ Database-Driven Context Loaded:")
        print(get_business_prompt_context(data))
