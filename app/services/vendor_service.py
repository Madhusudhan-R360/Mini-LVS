import random
import string

def vendor_amazon(quantity: int):
    success = random.choice([True, True, False])

    if not success:
        return {"status": "FAILED", "vouchers": []}

    vouchers = [
        "AM-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        for _ in range(quantity)
    ]

    return {"status": "SUCCESS", "vouchers": vouchers}


def vendor_flipkart(quantity: int):
    success = random.choice([True, True, False])

    if not success:
        return {"status": "FAILED", "vouchers": []}

    vouchers = [
        "FK-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        for _ in range(quantity)
    ]

    return {"status": "SUCCESS", "vouchers": vouchers}


def vendor_default(quantity: int):
    return {
        "status": "FAILED",
        "message": "Unknown product"
    }
