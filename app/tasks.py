from app.celery_worker import celery_app
from app.database import orders_collection, vouchers_collection
from app.services.vendor_service import vendor_amazon, vendor_flipkart
import time

@celery_app.task
def process_order_task(order_id, quantity, product):

    MAX_RETRIES = 3

    # routing
    if product == "amazon_voucher":
        vendor_function = vendor_amazon
    elif product == "flipkart_voucher":
        vendor_function = vendor_flipkart
    else:
        orders_collection.update_one(
            {"order_id": order_id},
            {"$set": {"status": "FAILED"}}
        )
        return

    for attempt in range(1, MAX_RETRIES + 1):
        print(f"[Celery] Attempt {attempt}")

        response = vendor_function(quantity)

        if response["status"] == "SUCCESS":
            for code in response["vouchers"]:
                vouchers_collection.insert_one({
                    "order_id": order_id,
                    "voucher_code": code
                })

            orders_collection.update_one(
                {"order_id": order_id},
                {"$set": {"status": "DELIVERED"}}
            )
            return

        time.sleep(2)

    orders_collection.update_one(
        {"order_id": order_id},
        {"$set": {"status": "FAILED"}}
    )