import mongomock

# Create a mock MongoDB client
client = mongomock.MongoClient()

# Create database
db = client["lvs_db"]

# Collections
orders_collection = db["orders"]
vouchers_collection = db["vouchers"]
