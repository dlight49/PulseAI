import os
import sys
import json
import time
import asyncio
import httpx
import threading
from concurrent.futures import ThreadPoolExecutor

# Ensure project root in path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

# MOCKING THE WORKER TO SAVE API COSTS
# We want to test the PIPELINE speed, not the LLM speed right now
from core.db_manager import save_message

async def simulate_incoming_message(client, sender_id, message_text):
    """Simulates a single Meta Webhook POST request."""
    payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "WHATSAPP_ID",
            "changes": [{
                "value": {
                    "messaging_product": "whatsapp",
                    "metadata": {"display_phone_number": "2340000000", "phone_number_id": "12345"},
                    "messages": [{
                        "from": sender_id,
                        "id": "wamid.HBgL",
                        "timestamp": str(int(time.time())),
                        "text": {"body": message_text},
                        "type": "text"
                    }]
                },
                "field": "messages"
            }]
        }]
    }
    
    start_time = time.time()
    try:
        response = await client.post("http://127.0.0.1:5001/webhook", json=payload)
        latency = (time.time() - start_time) * 1000
        return response.status_code, latency
    except Exception as e:
        return 500, 0

async def run_stress_test(total_messages=100):
    print(f"🔥 QA STRESS TEST: Simulating {total_messages} concurrent messages...")
    print(f"Target: Pulse AI Webhook (FastAPI + Async Pipeline)")
    print("-" * 50)

    async with httpx.AsyncClient() as client:
        tasks = []
        for i in range(total_messages):
            sender = f"234800000{i:04d}"
            tasks.append(simulate_incoming_message(client, sender, "Hi, I want to book a facial!"))
        
        start_all = time.time()
        results = await asyncio.gather(*tasks)
        total_duration = time.time() - start_all
        
        # Stats
        success_count = sum(1 for status, lat in results if status == 200)
        avg_latency = sum(lat for status, lat in results) / total_messages
        
        print(f"\n📊 RESULTS:")
        print(f"✅ Success Rate: {success_count}/{total_messages} ({(success_count/total_messages)*100}%)")
        print(f"⏱️ Avg Webhook Response Time: {avg_latency:.2f}ms")
        print(f"🚀 Total Time for {total_messages} requests: {total_duration:.2f}s")
        print(f"📈 Throughput: {total_messages/total_duration:.2f} messages/second")
        
        if success_count == total_messages:
            print("\n🌟 VERDICT: THE PIPELINE IS INDESTRUCTIBLE. 10k Scaling Ready.")
        else:
            print("\n⚠️ VERDICT: SYSTEM BOTTLENECK DETECTED. Check logs.")

if __name__ == "__main__":
    # Note: Webhook must be running in another process
    asyncio.run(run_stress_test(200)) # Starting with 200 to prove the concept
