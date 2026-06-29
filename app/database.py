from pymongo import MongoClient

# ✅ Connect to real MongoDB (running in Docker)
client = MongoClient("mongodb://localhost:27017")

# ✅ Database
db = client["lvs_db"]

# ✅ Collections
orders_collection = db["orders"]
vouchers_collection = db["vouchers"]
