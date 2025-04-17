# # from kafka import KafkaConsumer
# # import json

# # # Set up the Kafka consumer
# # consumer = KafkaConsumer(
# #     'logs',
# #     bootstrap_servers='localhost:9092',
# #     auto_offset_reset='latest',       # start from latest message
# #     enable_auto_commit=True,
# #     group_id='log-monitor-group',
# #     value_deserializer=lambda x: json.loads(x.decode('utf-8'))
# # )

# # print("📡 Kafka Consumer started. Listening to 'logs' topic...\n")

# # try:
# #     for message in consumer:
# #         log = message.value
# #         print(f"[{log['timestamp']}] {log['method']} {log['endpoint']} → {log['status_code']} "
# #               f"({log['response_time_ms']}ms) | Agent: {log['user_agent']}")
# # except KeyboardInterrupt:
# #     print("\n🛑 Consumer stopped.")
# # finally:
# #     consumer.close()


# from kafka import KafkaConsumer
# import mysql.connector
# import json
# from datetime import datetime

# # MySQL connection config
# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="root",
#     database="monitoring"
# )
# cursor = db.cursor()

# # Kafka Consumer config
# consumer = KafkaConsumer(
#     'logs',
#     bootstrap_servers='localhost:9092',
#     auto_offset_reset='latest',
#     enable_auto_commit=True,
#     group_id='log-monitor-group',
#     value_deserializer=lambda m: json.loads(m.decode('utf-8'))
# )

# print("✅ Kafka consumer started. Listening for logs...\n")

# try:
#     for msg in consumer:
#         log = msg.value

#         # Parse values
#         request_id = log.get('request_id')
#         endpoint = log.get('endpoint')
#         method = log.get('method')
#         status_code = log.get('status_code')
#         response_time_ms = log.get('response_time_ms')
#         user_agent = log.get('user_agent')
#         timestamp = datetime.strptime(log.get('timestamp'), "%Y-%m-%d %H:%M:%S")

#         # Insert into MySQL
#         cursor.execute("""
#             INSERT INTO api_logs (request_id, endpoint, method, status_code, response_time_ms, user_agent, timestamp)
#             VALUES (%s, %s, %s, %s, %s, %s, %s)
#         """, (request_id, endpoint, method, status_code, response_time_ms, user_agent, timestamp))
#         db.commit()

#         print(f"[DB ✅] Stored log: {method} {endpoint} → {status_code}")

# except KeyboardInterrupt:
#     print("\n🛑 Stopped by user.")

# finally:
#     consumer.close()
#     cursor.close()
#     db.close()



from kafka import KafkaConsumer
import mysql.connector
import json
from datetime import datetime

# ✅ MySQL connection config
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",  # Update if different
    database="monitoring"
)
cursor = db.cursor()

# ✅ Kafka Consumer - Listen to multiple log topics
consumer = KafkaConsumer(
    'info-logs', 'error-logs', 'debug-logs',  # Add more topics if needed
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='log-monitor-group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("✅ Kafka consumer started. Listening to info-logs, error-logs, and debug-logs...\n")

try:
    for msg in consumer:
        log = msg.value

        # Extract values
        request_id = log.get('request_id')
        endpoint = log.get('endpoint')
        method = log.get('method')
        status_code = log.get('status_code')
        response_time_ms = log.get('response_time_ms')
        user_agent = log.get('user_agent')
        timestamp_str = log.get('timestamp')
        level = log.get('level', msg.topic.replace("-logs", "").upper())

        # Parse timestamp
        try:
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print(f"❌ Timestamp parse error: {e}")
            continue

        # Insert into MySQL
        cursor.execute("""
            INSERT INTO api_logs (request_id, endpoint, method, status_code, response_time_ms, user_agent, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (request_id, endpoint, method, status_code, response_time_ms, user_agent, timestamp))
        db.commit()

        print(f"[{level}] DB ✅ Stored: {method} {endpoint} → {status_code} | {timestamp_str}")

except KeyboardInterrupt:
    print("\n🛑 Stopped by user.")

finally:
    consumer.close()
    cursor.close()
    db.close()
