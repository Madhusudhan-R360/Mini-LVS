# 🚀 Mini LVS (Live Voucher System)

## 📌 Overview

Mini LVS (Live Voucher System) is a production-style backend application built using **FastAPI**, **Celery**, **Redis**, and **MongoDB**.

The system simulates how voucher orders are processed in real-world reward and voucher platforms using asynchronous processing, message queues, background workers, caching, retries, and lifecycle tracking.

---

## 🏗️ System Architecture

```text
Client
   ↓
FastAPI
   ↓
Celery
   ↓
Redis (Broker Queue)
   ↓
Celery Worker
   ↓
MongoDB
````

### Extended Architecture

```text
                    Redis Cache
                        ↑
                        |
Client → FastAPI → MongoDB
              |
              ↓
            Celery
              ↓
          Redis Queue
              ↓
        Celery Worker
              ↓
          Vendor APIs
```

***

## ⚙️ Technology Stack

* **Backend Framework:** FastAPI
* **Task Queue:** Celery
* **Message Broker:** Redis
* **Cache Layer:** Redis
* **Database:** MongoDB
* **Database Driver:** PyMongo
* **Background Workers:** Celery Workers
* **Container Support:** Docker
* **Language:** Python 3.12

***

# ✅ Implemented Features

## 1. Order Creation

Endpoint:

```http
POST /orders
```

### Capabilities

* Creates a unique order ID
* Stores order in MongoDB
* Generates voucher processing task
* Pushes task to Celery queue

***

## 2. Order Retrieval

Endpoints:

```http
GET /orders
GET /orders/{order_id}
```

### Capabilities

* Fetch all orders
* Fetch a specific order
* Retrieve associated voucher data
* Utilizes Redis caching for faster access

***

## 3. Multi-Vendor Support

Implemented vendor routing based on product type.

Supported vendors:

* Amazon Voucher
* Flipkart Voucher

Example:

```text
amazon_voucher  → Amazon Vendor
flipkart_voucher → Flipkart Vendor
```

***

## 4. Asynchronous Processing

Order processing is completely asynchronous.

### Flow

```text
Client submits order
       ↓
API returns immediately
       ↓
Task added to Redis queue
       ↓
Worker processes task
       ↓
Database updated
```

### Benefits

* Faster API response
* Better scalability
* Improved user experience

***

## 5. Redis Queue Integration

Redis is used as Celery's message broker.

### Queue Flow

```text
FastAPI
   ↓
Redis Queue
   ↓
Celery Worker
```

### Advantages

* Decouples API and processing
* Enables worker scalability
* Supports asynchronous architecture

***

## 6. Queue Separation

Implemented dedicated queue:

```text
orders_queue
```

instead of relying only on the default Celery queue.

### Benefits

* Better workload isolation
* Easier scaling
* Foundation for priority-based processing

***

## 7. Celery Background Workers

Workers execute voucher processing outside the API request lifecycle.

Responsibilities:

* Process queued tasks
* Call vendors
* Handle retries
* Update order status
* Generate vouchers

***

## 8. Order Lifecycle Tracking

Implemented production-style order lifecycle.

### Status Flow

```text
CREATED
   ↓
QUEUED
   ↓
PROCESSING
   ↓
DELIVERED
```

or

```text
FAILED
```

### Status Meaning

| Status     | Description                    |
| ---------- | ------------------------------ |
| CREATED    | Order stored in database       |
| QUEUED     | Task submitted to Redis        |
| PROCESSING | Worker executing task          |
| DELIVERED  | Voucher successfully generated |
| FAILED     | Retries exhausted              |

***

## 9. Retry Mechanism

Implemented Celery native retries.

### Behavior

```text
Vendor Failure
      ↓
Retry
      ↓
Retry
      ↓
Retry
      ↓
Success / Failure
```

### Benefits

* Handles transient issues
* Improves reliability
* Reduces manual intervention

***

## 10. Exponential Backoff

Retry intervals increase progressively.

### Example

```text
Retry 1 → 2 sec
Retry 2 → 4 sec
Retry 3 → 8 sec
```

### Benefits

* Prevents vendor overload
* Improves success rate
* Production-style fault tolerance

***

## 11. Failure Handling

If all retries fail:

```text
Order Status → FAILED
```

### Benefits

* No stuck orders
* Accurate order tracking
* Better operational visibility

***

## 12. Redis Caching

Implemented Redis cache for:

```http
GET /orders/{order_id}
```

### Cache Workflow

```text
Request
   ↓
Redis Lookup
   ↓
Cache Hit  → Return immediately
Cache Miss → MongoDB Query
               ↓
           Store in Redis
               ↓
            Return
```

### Benefits

* Faster response time
* Reduced database load
* Improved scalability

***

## 13. Cache Hit / Cache Miss Logging

System logs:

```text
Cache HIT
Cache MISS
```

for easy performance tracking.

***

## 14. Structured Logging

Implemented centralized logging.

### Logged Events

* Order creation
* Worker processing
* Vendor success
* Vendor failure
* Retry attempts
* Final delivery
* Final failure

Example:

```text
Starting processing for order
Vendor failed
Retrying order
Order DELIVERED
```

***

## 15. MongoDB Integration

Uses real MongoDB database.

### Collections

```text
lvs_db
 ├── orders
 └── vouchers
```

### Stored Data

Orders:

```json
{
  "order_id": "...",
  "status": "DELIVERED"
}
```

Vouchers:

```json
{
  "order_id": "...",
  "voucher_code": "ABC123"
}
```

***

## 16. Idempotency Support

Implemented:

```text
idempotency_key
```

### Benefits

* Prevents duplicate order creation
* Safe retries
* Ensures consistency

***

# 🔄 End-to-End Workflow

```text
POST /orders
      ↓
Order Created
      ↓
Status = CREATED
      ↓
Task Sent to Redis
      ↓
Status = QUEUED
      ↓
Worker Picks Task
      ↓
Status = PROCESSING
      ↓
Vendor Processing
      ↓
SUCCESS → DELIVERED
      ↓
Voucher Stored

OR

FAILURE → Retry
      ↓
Retries Exhausted
      ↓
FAILED
```

***

# 📡 API Endpoints

## Create Order

```http
POST /orders
```

Example Request:

```json
{
  "client": "HDFC",
  "product": "amazon_voucher",
  "quantity": 2,
  "idempotency_key": "abc123"
}
```

***

## Get All Orders

```http
GET /orders
```

***

## Get Order By ID

```http
GET /orders/{order_id}
```

***

# 🧠 Key Concepts Demonstrated

## Asynchronous Processing

```text
Request → Queue → Worker → Result
```

***

## Producer-Consumer Model

```text
Producer → FastAPI
Broker   → Redis
Consumer → Celery Worker
```

***

## Eventual Consistency

```text
Order Created
    ↓
Background Processing
    ↓
Final State Available
```

***

## Queue-Based Architecture

```text
Task Producer
      ↓
Redis Queue
      ↓
Worker Consumer
```

***

## Distributed System Design

Independent components:

* API Layer
* Queue Layer
* Worker Layer
* Data Layer
* Cache Layer

***

## Fault Tolerance

Implemented:

* Retry handling
* Exponential backoff
* Failure state tracking

***

# 🛠️ Local Setup

## 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

***

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

***

## 3. Start Redis

```bash
redis-server
```

***

## 4. Start MongoDB

```bash
docker run -d -p 27017:27017 mongo
```

***

## 5. Start Celery Worker

```bash
python -m celery -A app.celery_worker worker -Q orders_queue --loglevel=info
```

***

## 6. Start FastAPI

```bash
uvicorn app.main:app --reload --port 8001
```

***

## 7. Access Swagger UI

```text
http://localhost:8001/docs
```

***

# 📊 Current Capabilities

✅ FastAPI APIs

✅ MongoDB Persistence

✅ Redis Queue

✅ Redis Cache

✅ Celery Workers

✅ Dedicated Order Queue

✅ Order Lifecycle Tracking

✅ Multi-Vendor Routing

✅ Retry Mechanism

✅ Exponential Backoff

✅ Failure Handling

✅ Structured Logging

✅ Idempotency

✅ Async Order Processing

***

# 🎯 Project Summary

Mini LVS demonstrates a production-style backend architecture using FastAPI, Redis, Celery, and MongoDB. The system supports asynchronous voucher fulfillment, order lifecycle management, retry handling with exponential backoff, Redis-based caching, dedicated task queues, structured logging, and idempotency, closely simulating how real-world voucher and rewards platforms process transactions at scale.

***

## 👨‍💻 Author

**Madhusudhan M**
