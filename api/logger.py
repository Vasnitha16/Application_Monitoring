
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


# from kafka import KafkaProducer
# import logging
# import json

# producer = KafkaProducer(
#     bootstrap_servers='localhost:9092',
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )

# def get_logger(name: str):
#     logger = logging.getLogger(name)
#     logger.setLevel(logging.INFO)

#     if not logger.handlers:
#         ch = logging.StreamHandler()
#         formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
#         ch.setFormatter(formatter)
#         logger.addHandler(ch)

#     def kafka_handler(log_data):
#         producer.send("logs", log_data)

#     logger.kafka = kafka_handler  # attach custom method

#     return logger


from kafka import KafkaProducer
import logging
import json

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # enable all log levels

    if not logger.handlers:
        ch = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        ch.setLevel(logging.DEBUG)
        logger.addHandler(ch)

    # Custom method to send to topic based on level
    def kafka_handler(log_data: dict, level: str = "INFO"):
        topic = f"{level.lower()}-logs"
        producer.send(topic, log_data)

    logger.kafka = kafka_handler  # attach method to logger object

    return logger
