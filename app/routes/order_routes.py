from fastapi import APIRouter, BackgroundTasks
from app.models.model import OrderRequest
from app.database import orders_collection, vouchers_collection
from app.services.vendor_service import vendor_amazon, vendor_flipkart, vendor_default
from datetime import datetime
import time
import uuid
from app.tasks import process_order_task

router = APIRouter()

def process_order_background(order_id: str, quantity: int):

    # Get product type
    order = orders_collection.find_one({"order_id": order_id})
    product = order.get("product")

    # 🔀 Vendor routing
    if product == "amazon_voucher":
        vendor_function = vendor_amazon
    elif product == "flipkart_voucher":
        vendor_function = vendor_flipkart
    else:
        vendor_function = vendor_default

    MAX_RETRIES = 3
    attempt = 0

    while attempt < MAX_RETRIES:
        attempt += 1
        print(f"Attempt {attempt} for order {order_id}")

        vendor_response = vendor_function(quantity)

        if vendor_response["status"] == "SUCCESS":

            for code in vendor_response["vouchers"]:
                vouchers_collection.insert_one({
                    "order_id": order_id,
                    "voucher_code": code,
                    "status": "ASSIGNED"
                })

            orders_collection.update_one(
                {"order_id": order_id},
                {"$set": {"status": "DELIVERED"}}
            )

            return

        import time
        time.sleep(2)

    orders_collection.update_one(
        {"order_id": order_id},
        {"$set": {"status": "FAILED"}}
    )

@router.post("/orders")
def create_order(order: OrderRequest, background_tasks: BackgroundTasks):

    # ✅ Check if idempotency_key already exists
    existing_order = orders_collection.find_one(
        {"idempotency_key": order.idempotency_key},
        {"_id": 0}
    )

    if existing_order:
        return {
            "message": "Duplicate request - returning existing order",
            "order_id": existing_order["order_id"],
            "status": existing_order["status"]
        }

    # ✅ Create new order
    order_id = str(uuid.uuid4())

    order_data = {
        "order_id": order_id,
        "client": order.client,
        "product": order.product,
        "quantity": order.quantity,
        "status": "IN_PROGRESS",
        "idempotency_key": order.idempotency_key,
        "created_at": datetime.utcnow()
    }

    orders_collection.insert_one(order_data)

    process_order_task.delay(
        order_id,
        order.quantity,
        order.product
    )

    return {
        "message": "Order created successfully",
        "order_id": order_id,
        "status": "IN_PROGRESS"
    }

@router.get("/orders/{order_id}")
def get_order(order_id: str):
    # Find order
    order = orders_collection.find_one({"order_id": order_id}, {"_id": 0})

    if not order:
        return {
            "message": "Order not found"
        }

    # Find vouchers for this order
    vouchers = list(vouchers_collection.find(
        {"order_id": order_id},
        {"_id": 0, "voucher_code": 1}
    ))

    # Extract only voucher codes
    voucher_codes = [v["voucher_code"] for v in vouchers]

    return {
        "order": order,
        "vouchers": voucher_codes
    }

@router.get("/orders")
def get_all_orders():
    orders = list(orders_collection.find({}, {"_id": 0}))
    
    return {
        "total_orders": len(orders),
        "orders": orders
    }