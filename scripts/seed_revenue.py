import os
import sys
import uuid

# Ensure project root in path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

from core.db_manager import get_connection

def seed_revenue():
    print("💰 Seeding Pulse AI Revenue Data...")
    conn = get_connection()
    cursor = conn.cursor()

    business_id = "senior_sales_demo"
    # Get a contact ID
    cursor.execute("SELECT id FROM contacts LIMIT 1")
    contact_id = cursor.fetchone()[0]

    # Insert mock transactions
    transactions = [
        (str(uuid.uuid4()), business_id, contact_id, 45000, "PAID", "ref_001"),
        (str(uuid.uuid4()), business_id, contact_id, 38000, "PAID", "ref_002"),
        (str(uuid.uuid4()), business_id, contact_id, 15000, "PENDING", "ref_003"),
        (str(uuid.uuid4()), business_id, contact_id, 45000, "PAID", "ref_004")
    ]
    
    cursor.executemany("INSERT OR IGNORE INTO transactions (id, business_id, contact_id, amount, status, reference) VALUES (?, ?, ?, ?, ?, ?)", transactions)
    
    conn.commit()
    conn.close()
    print("✅ Revenue data seeded successfully.")

if __name__ == "__main__":
    seed_revenue()
