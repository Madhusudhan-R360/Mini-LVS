🚀 Mini LVS (Live Voucher System)## 

📌 Overview : This project is a **mini Live Voucher System (LVS)** built using **FastAPI**, **Redis**, **Celery**, and **MongoDB**.It simulates how an ERP system processes voucher orders asynchronously using a **queue-based architecture**.

---## 🧠 System Architecture
Client
↓
FastAPI (API layer)
↓
Celery (Task Producer)
↓
Redis (Message Queue / Broker)
↓
Celery Worker (Task Executor)
↓
MongoDB (Persistent Storage)

---

## ⚙️ Features

### ✅ Order Management
- Create voucher orders via API
- Generates unique `order_id`
- Stores order with initial status `IN_PROGRESS`

---

### ✅ Asynchronous Processing
- Uses **Celery** for background task execution
- API responds immediately without waiting
- Order processing happens via worker

---

### ✅ Redis Queue Integration
- Redis acts as message broker
- Tasks are queued and processed asynchronously
- Supports scalable worker-based processing

---

### ✅ Celery Worker System
- Separate worker process executes background tasks
- Handles vendor integration and voucher generation
- Supports retry logic for failures

---

### ✅ MongoDB Integration
- Stores:
  - Orders
  - Voucher codes
  - Order status
- Shared across FastAPI and Celery worker

---

### ✅ Retry Mechanism
- Retries vendor calls up to 3 times
- Handles temporary failures gracefully

---

### ✅ Idempotency
- Prevents duplicate order creation
- Uses `idempotency_key` to ensure safe retries

---

### ✅ Multi-Vendor Routing
- Supports multiple vendors:
  - Amazon
  - Flipkart
- Routes request based on product type

---

### ✅ Order Tracking API
- Fetch order and voucher details:

GET /orders/{order_id}

---

## 📡 API Endpoints

### 🔹 Create Order

POST /orders

**Request Body:**
```json
{
  "client": "HDFC",
  "product": "amazon_voucher",
  "quantity": 2,
  "idempotency_key": "test123"
}


🔹 Get Order Status
GET /orders/{order_id}


🔹 Get All Orders
GET /orders


🔁 Workflow

Client sends order request
FastAPI creates order (IN_PROGRESS)
Celery sends task to Redis queue
Worker picks task from Redis
Worker processes order (vendor call)
MongoDB updated (DELIVERED / FAILED)
Client fetches result via GET API


⚡ Tech Stack

Backend: FastAPI
Queue / Broker: Redis
Task Worker: Celery
Database: MongoDB
Containerization: Docker
Language: Python 3.12


🧠 Key Concepts Demonstrated

Asynchronous processing
Queue-based architecture
Producer-Consumer model
Eventual consistency
Retry mechanisms
Idempotency
Distributed systems design


🛠️ Local Setup
1. Activate Virtual Environment
Shellpython3 -m venv venvsource venv/bin/activate``Show more lines

2. Install Dependencies
Shellpip install -r requirements.txtShow more lines

3. Start Redis
Shellredis-serverShow more lines

4. Start MongoDB (Docker)
Shelldocker run -d -p 27017:27017 mongoShow more lines

5. Start Celery Worker
Shellpython -m celery -A app.celery_worker worker --loglevel=info``Show more lines

6. Start FastAPI
Shelluvicorn app.main:app --reload --port 8001Show more lines

7. Access API
http://localhost:8001/docs


✅ Final Capability
This system can:
✅ Handle asynchronous order processing
✅ Process tasks via Redis queue
✅ Execute background jobs using Celery
✅ Store and retrieve data from MongoDB
✅ Handle retries and failures
✅ Scale using worker-based architecture

📌 Summary
This project demonstrates a production-style backend system using:

FastAPI for APIs
Redis for queueing
Celery for background processing
MongoDB for persistent storage


👨‍💻 Author
Madhusudhan M
