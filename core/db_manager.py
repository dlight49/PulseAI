import os
import json
import uuid
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from dotenv import load_dotenv

# Path safety
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
load_dotenv(dotenv_path=os.path.join(project_root, "config", ".env"))

# PRODUCTION DATABASE URL (Neon)
DB_URL = os.getenv("DATABASE_URL")

def get_connection():
    """Returns a connection to the Production PostgreSQL database."""
    if not DB_URL:
        raise Exception("❌ PRODUCTION ERROR: DATABASE_URL not set in .env")
    
    conn = psycopg2.connect(DB_URL, sslmode='require')
    return conn

def get_business(business_id):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM businesses WHERE id = %s", (business_id,))
        business = cursor.fetchone()
        
        if not business:
            return None
            
        # Fetch services
        cursor.execute("SELECT * FROM services WHERE business_id = %s", (business_id,))
        services = cursor.fetchall()
        business['services'] = services
        
        # Objection playbook is already a dict in PG (JSONB)
        return dict(business)
    finally:
        conn.close()

def get_or_create_contact(phone_number):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM contacts WHERE phone_number = %s", (phone_number,))
        row = cursor.fetchone()
        
        if not row:
            contact_id = str(uuid.uuid4())
            cursor.execute("INSERT INTO contacts (id, phone_number, relationship_type) VALUES (%s, %s, 'LEAD')", (contact_id, phone_number))
            conn.commit()
            cursor.execute("SELECT * FROM contacts WHERE id = %s", (contact_id,))
            row = cursor.fetchone()
            
        return dict(row)
    finally:
        conn.close()

def save_message(business_id, contact_id, role, content):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        msg_id = str(uuid.uuid4())
        cursor.execute("INSERT INTO conversations (id, business_id, contact_id, role, message_body) VALUES (%s, %s, %s, %s, %s)", 
                       (msg_id, business_id, contact_id, role, content))
        conn.commit()
    finally:
        conn.close()

def get_chat_history(business_id, contact_id, limit=10):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT role, message_body as content FROM conversations WHERE business_id = %s AND contact_id = %s ORDER BY timestamp DESC LIMIT %s", 
                       (business_id, contact_id, limit))
        rows = cursor.fetchall()
        return [dict(r) for r in reversed(rows)]
    finally:
        conn.close()

def update_contact_summary(contact_id, summary):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE contacts SET last_summary = %s, summary_updated_at = %s WHERE id = %s", 
                       (summary, datetime.now(), contact_id))
        conn.commit()
    finally:
        conn.close()
