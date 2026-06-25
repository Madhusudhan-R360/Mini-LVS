
# 🚀 Mini LVS (Live Voucher System)

## 📌 Overview
This project is a **mini Live Voucher System (LVS)** built using **FastAPI** and **MongoDB (mongomock)**.

It simulates how an ERP system processes **E‑voucher orders**, integrates with external vendors, and delivers vouchers to customers.

---

## 🧠 System Flow

```

ERP (API Request) → LVS → Vendor → LVS → Database → ERP (Status Check)

```

---

## ⚙️ Features

### ✅ Order Management
- Create voucher orders via API
- Generates unique `order_id`
- Stores order details in database

### ✅ Vendor Integration (Simulation)
- Simulates external vendor APIs
- Generates voucher codes dynamically
- Supports multiple vendors (Amazon, Flipkart)

### ✅ Asynchronous Processing
- Uses FastAPI BackgroundTasks
- Order processing happens in background
- API responds immediately

### ✅ Retry Mechanism
- Retries vendor call up to 3 times
- Handles temporary failures
- Improves reliability

### ✅ Idempotency
- Prevents duplicate order processing
- Uses `idempotency_key`
- Same request → same response

### ✅ Multi-Vendor Routing
- Routes requests based on product type:
  - `amazon_voucher` → Amazon Vendor
  - `flipkart_voucher` → Flipkart Vendor

### ✅ Order Tracking
- Fetch order details using:
```

GET /orders/{order\_id}

```
- Returns:
- Order status
- Voucher codes (if available)

---

## 📡 API Endpoints

### 🔹 Create Order
```

POST /orders

````

**Request Body:**
```json
{
  "client": "HDFC",
  "product": "amazon_voucher",
  "quantity": 2,
  "idempotency_key": "test123"
}
````

***

### 🔹 Get Order Status

```
GET /orders/{order_id}
```

***

## 🗄️ Tech Stack

* **Backend:** FastAPI
* **Database:** MongoDB (mongomock for local testing)
* **Containerization:** Docker
* **Language:** Python 3.12

***

## 🐳 Docker Setup

### Build Image

```bash
docker build -t mini-lvs .
```

### Run Container

```bash
docker run -p 8000:8000 mini-lvs
```

### Access API Docs

```
http://localhost:8000/docs
```

***

## 🛠️ Local Setup

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Server

```bash
uvicorn app.main:app --reload --port 8001
```

***

## 🧠 Key Concepts Learned

* API design with FastAPI
* Asynchronous processing
* Retry mechanisms
* Idempotency in backend systems
* Vendor abstraction and routing
* NoSQL data modeling
* Docker containerization

***

## ✅ Project Capability

This system can:

* Accept voucher orders
* Process orders asynchronously
* Integrate with multiple vendors
* Handle vendor failures with retry logic
* Prevent duplicate requests
* Provide order status and voucher tracking

***

## 📌 Summary

This project simulates a **production-like LVS backend system**, covering real-world concepts such as async workflows, vendor integration, retry handling, and scalable API design.

***

## 👨‍💻 Author

Madhusudhan M

---
