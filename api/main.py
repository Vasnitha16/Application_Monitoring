# from fastapi import FastAPI, Request, HTTPException, Path
# from api.logger import get_logger
# import time
# import random
# import uuid

# app = FastAPI()
# logger = get_logger("api")

# # Sample data
# fake_users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
# fake_products = [{"id": 10, "name": "Widget"}, {"id": 11, "name": "Gadget"}]
# fake_orders = []
# fake_inventory = {"Widget": 12, "Gadget": 7}
# metrics = {"requests": 0, "errors": 0, "per_endpoint": {}}


# @app.middleware("http")
# async def log_request_data(request: Request, call_next):
#     request_id = str(uuid.uuid4())
#     start_time = time.time()
#     response = await call_next(request)
#     duration = round((time.time() - start_time) * 1000, 2)

#     endpoint = request.url.path
#     status_code = response.status_code

#     # Metrics tracking
#     metrics["requests"] += 1
#     if status_code >= 400:
#         metrics["errors"] += 1
#     metrics["per_endpoint"].setdefault(endpoint, 0)
#     metrics["per_endpoint"][endpoint] += 1

#     # Log to console or push to Kafka
#     log = {
#         "request_id": request_id,
#         "endpoint": endpoint,
#         "method": request.method,
#         "status_code": status_code,
#         "response_time_ms": duration,
#         "user_agent": request.headers.get("user-agent"),
#         "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
#     }
#     # Log to console
#     logger.info(f"LOG | {log}")

#     # Send to Kafka
#     logger.kafka(log)



# @app.get("/status")
# async def get_status():
#     return {"message": "API is live"}


# @app.get("/health")
# async def health_check():
#     return {"status": "healthy"}


# @app.get("/users")
# async def get_users():
#     return fake_users


# @app.get("/users/{user_id}")
# async def get_user(user_id: int):
#     user = next((u for u in fake_users if u["id"] == user_id), None)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


# @app.post("/login")
# async def login():
#     return {"token": "fake-jwt-token", "user_id": random.choice(fake_users)["id"]}


# @app.get("/products")
# async def get_products():
#     return fake_products


# @app.get("/products/{product_id}")
# async def get_product(product_id: int):
#     product = next((p for p in fake_products if p["id"] == product_id), None)
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not found")
#     return product


# @app.post("/orders")
# async def create_order(order: dict):
#     order_id = len(fake_orders) + 1
#     fake_orders.append({"id": order_id, **order})
#     return {"message": "Order placed", "order_id": order_id}


# @app.get("/orders/{order_id}")
# async def get_order(order_id: int = Path(..., gt=0)):
#     order = next((o for o in fake_orders if o["id"] == order_id), None)
#     if not order:
#         raise HTTPException(status_code=404, detail="Order not found")
#     return order


# @app.get("/inventory")
# async def get_inventory():
#     return fake_inventory


# @app.get("/metrics")
# async def get_metrics():
#     return metrics



from fastapi import FastAPI, Request, HTTPException, Path
from fastapi.responses import JSONResponse
from api.logger import get_logger
import time
import random
import uuid

app = FastAPI()
logger = get_logger("api")

# Sample data
fake_users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
fake_products = [{"id": 10, "name": "Widget"}, {"id": 11, "name": "Gadget"}]
fake_orders = []
fake_inventory = {"Widget": 12, "Gadget": 7}
metrics = {"requests": 0, "errors": 0, "per_endpoint": {}}


@app.middleware("http")
async def log_request_data(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}")
        metrics["errors"] += 1
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
    
    duration = round((time.time() - start_time) * 1000, 2)
    endpoint = request.url.path
    status_code = response.status_code

    metrics["requests"] += 1
    if status_code >= 400:
        metrics["errors"] += 1
    metrics["per_endpoint"].setdefault(endpoint, 0)
    metrics["per_endpoint"][endpoint] += 1

    log = {
        "request_id": request_id,
        "endpoint": endpoint,
        "method": request.method,
        "status_code": status_code,
        "response_time_ms": duration,
        "user_agent": request.headers.get("user-agent"),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    logger.info(f"LOG | {log}")
    logger.kafka(log)
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."}
    )


@app.get("/status")
async def get_status():
    return {"message": "API is live"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/users")
async def get_users():
    return fake_users


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = next((u for u in fake_users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/login")
async def login():
    return {"token": "fake-jwt-token", "user_id": random.choice(fake_users)["id"]}


@app.get("/products")
async def get_products():
    return fake_products


@app.get("/products/{product_id}")
async def get_product(product_id: int):
    product = next((p for p in fake_products if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/orders")
async def create_order(order: dict):
    order_id = len(fake_orders) + 1
    fake_orders.append({"id": order_id, **order})
    return {"message": "Order placed", "order_id": order_id}


@app.get("/orders")
async def list_orders():
    return fake_orders


@app.get("/orders/{order_id}")
async def get_order(order_id: int = Path(..., gt=0)):
    order = next((o for o in fake_orders if o["id"] == order_id), None)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.get("/inventory")
async def get_inventory():
    return fake_inventory


@app.get("/metrics")
async def get_metrics():
    total_requests = metrics["requests"]
    total_errors = metrics["errors"]
    error_rate = round((total_errors / total_requests) * 100, 2) if total_requests else 0.0

    per_endpoint_breakdown = [
        {"endpoint": ep, "hits": count, "percent": round((count / total_requests) * 100, 2)}
        for ep, count in metrics["per_endpoint"].items()
    ]

    return {
        "total_requests": total_requests,
        "total_errors": total_errors,
        "error_rate_percent": error_rate,
        "per_endpoint_usage": per_endpoint_breakdown
    }
