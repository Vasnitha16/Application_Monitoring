
# import logging

# def get_logger(name: str):
#     logger = logging.getLogger(name)
#     logger.setLevel(logging.INFO)

#     if not logger.handlers:
#         ch = logging.StreamHandler()
#         formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
#         ch.setFormatter(formatter)
#         logger.addHandler(ch)

#     return logger


from kafka import KafkaProducer
import logging
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        ch = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    def kafka_handler(log_data):
        producer.send("logs", log_data)

    logger.kafka = kafka_handler  # attach custom method

    return logger
