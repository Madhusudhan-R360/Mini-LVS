from app.celery_worker import celery_app
from app.database import orders_collection, vouchers_collection
from app.services.vendor_service import vendor_amazon, vendor_flipkart
from app.logger import logger


@celery_app.task(bind=True, max_retries=3)
def process_order_task(self, order_id, quantity, product):

    logger.info(f"Starting processing for order {order_id}")

    # ✅ Vendor selection
    if product == "amazon_voucher":
        vendor_function = vendor_amazon
    elif product == "flipkart_voucher":
        vendor_function = vendor_flipkart
    else:
        logger.error(f"Unknown product {product}")

        orders_collection.update_one(
            {"order_id": order_id},
            {"$set": {"status": "FAILED"}}
        )
        return

    try:
        response = vendor_function(quantity)

        if response["status"] == "SUCCESS":

            logger.info(f"Vendor success for order {order_id}")

            for code in response["vouchers"]:
                vouchers_collection.insert_one({
                    "order_id": order_id,
                    "voucher_code": code
                })

            orders_collection.update_one(
                {"order_id": order_id},
                {"$set": {"status": "DELIVERED"}}
            )

            logger.info(f"Order {order_id} DELIVERED")
            return

        else:
            logger.error(f"Vendor failed for order {order_id}")
            raise Exception("Vendor failed")

    except Exception as e:

    # ✅ Check if max retries exceeded
        if self.request.retries >= self.max_retries:
            logger.error(f"Order {order_id} FAILED after retries")

            orders_collection.update_one(
            {"order_id": order_id},
            {"$set": {"status": "FAILED"}}
        )
            return

        delay = 2 ** self.request.retries

        logger.error(f"Retrying order {order_id} in {delay} seconds")

        raise self.retry(
        exc=e,
        countdown=delay
    )
