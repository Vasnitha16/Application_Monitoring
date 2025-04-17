from kafka import KafkaProducer
import json
import time
import uuid
import random

# Connect to Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Define sample logs
sample_logs = {
    "INFO": "User successfully logged in.",
    "ERROR": "Failed to connect to database.",
    "DEBUG": "Auth token verified from cache."
}

log_levels = ["INFO", "ERROR", "DEBUG"]

def create_log(level):
    return {
        "log_id": str(uuid.uuid4()),
        "level": level,
        "message": sample_logs[level],
        "endpoint": "/example-endpoint",
        "method": "GET",
        "status_code": 200 if level == "INFO" else 500,
        "response_time_ms": round(random.uniform(0.5, 5.0), 2),
        "user_agent": "log-producer-client/1.0",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

try:
    print("🚀 Kafka log producer started. Press Ctrl+C to stop.")
    while True:
        level = random.choice(log_levels)
        topic = f"{level.lower()}-logs"
        log_entry = create_log(level)

        producer.send(topic, log_entry)
        print(f"[{level}] Log sent to `{topic}`: {log_entry}")
        time.sleep(1)

except KeyboardInterrupt:
    print("\n🛑 Producer stopped.")
finally:
    producer.close()
