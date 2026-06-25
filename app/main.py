from fastapi import FastAPI
from app.routes import order_routes

app = FastAPI()

app.include_router(order_routes.router)

@app.get("/")
def home():
    return {"message": "Mini LVS is running "}