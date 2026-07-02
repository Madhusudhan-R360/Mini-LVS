from pymongo import MongoClient
import redis
# ✅ Connect to real MongoDB (running in Docker)
client = MongoClient("mongodb://localhost:27017")

# ✅ Database
db = client["lvs_db"]

# ✅ Collections
orders_collection = db["orders"]
vouchers_collection = db["vouchers"]

# Redis cache connection
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=1,
    decode_responses=True
)
