import requests
import random
import time

BASE_URL = "http://localhost:8000"

ENDPOINTS = [
    "/users",
    "/users/1",
    "/products",
    "/products/10",
    "/orders",
    "/orders/1",
    "/status",
    "/health",
    "/inventory",
    "/metrics"
]

METHODS = {
    "GET": lambda url: requests.get(url),
    "POST": lambda url: requests.post(url, json={"product_id": 10, "quantity": 1})
}

def simulate_traffic(iterations=50):
    for _ in range(iterations):
        endpoint = random.choice(ENDPOINTS)
        method = "POST" if "/orders" in endpoint and random.random() > 0.5 else "GET"
        url = BASE_URL + endpoint

        try:
            response = METHODS[method](url)
            print(f"{method} {url} -> {response.status_code}")
        except Exception as e:
            print(f"Error accessing {url}: {e}")

        time.sleep(random.uniform(0.3, 1.0))

if __name__ == "__main__":
    simulate_traffic()
