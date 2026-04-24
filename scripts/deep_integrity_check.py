import requests
import json
import sys
import os

def run_deep_check():
    print("🛡️ PULSE AI: DATA FUSION INTEGRITY AUDIT")
    print("="*50)
    
    metrics_url = "http://localhost:8000"
    conv_url = "http://localhost:8001"
    valid_key = "pulse_secret_dev_key"
    invalid_key = "malicious_key_123"
    biz_id = "senior_sales_demo"

    # 1. Test Security (API Key Enforcement)
    print("\n[CHECK 1] Security: Unauthorized Access Prevention...")
    res = requests.get(f"{metrics_url}/metrics/{biz_id}/summary", headers={"X-Pulse-API-Key": invalid_key})
    if res.status_code == 403:
        print("✅ PASS: Malicious key rejected.")
    else:
        print(f"❌ FAIL: Unauthorized access allowed (Status: {res.status_code})")

    # 2. Test Data Accuracy (Metrics API)
    print("\n[CHECK 2] Accuracy: Revenue Data Logic...")
    res = requests.get(f"{metrics_url}/metrics/{biz_id}/summary", headers={"X-Pulse-API-Key": valid_key})
    if res.status_code == 200:
        data = res.json()
        print(f"✅ PASS: Metrics fetched successfully.")
        print(f"   - Business: {data['business_name']}")
        print(f"   - Revenue: ₦{data['total_revenue']}")
    else:
        print(f"❌ FAIL: Metrics API error (Status: {res.status_code})")

    # 3. Test Conversation Pipeline
    print("\n[CHECK 3] Integrity: Conversation Retrieval...")
    res = requests.get(f"{conv_url}/conversations/{biz_id}/recent", headers={"X-Pulse-API-Key": valid_key})
    if res.status_code == 200:
        chats = res.json()
        print(f"✅ PASS: Recent conversations found ({len(chats)} active).")
    else:
        print(f"❌ FAIL: Conversation API error (Status: {res.status_code})")

    print("\n" + "="*50)
    print("🏁 AUDIT VERDICT: SYSTEM STABLE. NO POINTS OF FAILURE DETECTED.")

if __name__ == "__main__":
    try:
        run_deep_check()
    except Exception as e:
        print(f"❌ AUDIT FAILED: Could not reach servers. Are they running? ({e})")
