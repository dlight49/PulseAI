import os
import requests
from dotenv import load_dotenv

# Load secure tokens
load_dotenv(dotenv_path=r"C:\Users\Omola\PulseAI\config\.env")

PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")

def create_payment_link(amount, email, reference, metadata=None):
    """
    Creates a Paystack payment page link.
    Amount should be in Naira (converted to Kobo for Paystack).
    """
    if not PAYSTACK_SECRET_KEY:
        print("⚠️  Warning: PAYSTACK_SECRET_KEY not set. Returning a mock link.")
        return f"https://checkout.paystack.com/mock-link-{reference}"

    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    
    # Paystack expects amount in kobo
    payload = {
        "amount": int(amount) * 100,
        "email": email,
        "reference": reference,
        "metadata": metadata or {}
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['data']['authorization_url']
    except Exception as e:
        print(f"❌ Error creating Paystack link: {e}")
        return f"https://paystack.com/pay/error-{reference}"

if __name__ == "__main__":
    # Test link generation
    print(create_payment_link(15000, "customer@example.com", "test_ref_123"))
