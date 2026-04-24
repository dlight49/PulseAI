import os
import sys
import json
import uuid

# Ensure project root in path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from core.db_manager import get_connection

def seed():
    print("🌱 Seeding Pulse AI Database...")
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Seed Business
    business_id = "senior_sales_demo"
    cursor.execute("DELETE FROM businesses WHERE id = ?", (business_id,))
    cursor.execute('''
    INSERT INTO businesses (id, name, type, location, persona_prompt, competitive_edge, objection_playbook, payment_link)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        business_id, 
        "Luxe Glo Beauty & Spa", 
        "service", 
        "Lekki Phase 1, Lagos",
        "You are the Senior Sales Lead. Professional, persuasive, human, and direct. You are a CLOSER.",
        "We use only imported organic oils from France. Our treatments are 90 mins.",
        json.dumps({
            "too_expensive": "Acknowledge the cost, then pivot to the 90-min duration and premium materials.",
            "too_far": "Remind them we offer a premium Home Service."
        }),
        "https://paystack.com/pay/luxeglo-deposit"
    ))

    # 2. Seed Services
    cursor.execute("DELETE FROM services WHERE business_id = ?", (business_id,))
    services = [
        (str(uuid.uuid4()), business_id, "Full Body Glow Treatment", 45000, 38000, "Instant glow, Natural organic oils"),
        (str(uuid.uuid4()), business_id, "Express Hydrating Facial", 25000, 20000, "Deep hydration, No downtime"),
        (str(uuid.uuid4()), business_id, "Executive Mani-Pedi Combo", 15000, 12000, "Premium gel, Paraffin wax")
    ]
    cursor.executemany("INSERT INTO services VALUES (?, ?, ?, ?, ?, ?)", services)

    # 3. Seed Contacts (Personal Proxy)
    contacts = [
        ("2348000000001", "Segun (Lead Investor)", "INVESTOR", "Values speed and transparency.", "Keep updated on growth."),
        ("2348000000002", "Bolanle (Friend)", "FRIEND", "Very close friend.", "Maintain boundaries.")
    ]
    for phone, name, rel, context, goal in contacts:
        cursor.execute("DELETE FROM contacts WHERE phone_number = ?", (phone,))
        cursor.execute("INSERT INTO contacts (id, phone_number, display_name, relationship_type, context_notes, goal) VALUES (?, ?, ?, ?, ?, ?)",
                       (str(uuid.uuid4()), phone, name, rel, context, goal))

    conn.commit()
    conn.close()
    print("✅ Seeding complete.")

if __name__ == "__main__":
    seed()
