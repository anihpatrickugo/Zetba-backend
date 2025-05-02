import requests
from django.conf import settings

bearer_token = settings.PAYSTACK_SECRET_KEY

def paystack_payment(amount,  recipient, reference):

    try:
        res = requests.post(
            "https://api.paystack.co/transfer",
            headers={
                'Authorization': f'Bearer {bearer_token}',
                'Content-Type': 'application/json'
            },
            json={
                "source": "balance",
                "amount": amount,
                "recipient": recipient,
                "reference": reference,
                "reason": "Payment for services"
            },
        )
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def paystack_verify_transfer(reference):
    try:
        res = requests.get(
            f"https://api.paystack.co/transfer/verify/{reference}",
            headers={
                'Authorization': f'Bearer {bearer_token}',
                'Content-Type': 'application/json'
            },
        )
        print(reference)
        print("My data is : ", res.json())
        return res.json()

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
