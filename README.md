# Application Monitoring System

This project is a **distributed application monitoring system** designed to simulate API traffic, log requests, and monitor them using **Kafka**, **MySQL**, and **Grafana**. It provides a complete pipeline for generating, processing, storing, and visualizing logs, enabling real-time monitoring and analysis of API performance and errors.

---

## Features

- **FastAPI Application**:
  - Simulates API endpoints for users, products, orders, and more.
  - Logs request data (e.g., endpoint, method, status code, response time).
  - Middleware sends logs to Kafka for processing.

- **Kafka Integration**:
  - Acts as a message broker for logs.
  - Categorizes logs into `info-logs`, `error-logs`, and `debug-logs` topics.
  - Kafka producer generates synthetic logs, and Kafka consumer processes them.

- **MySQL Database**:
  - Stores logs in a structured format for querying and analysis.
  - Schema includes fields like `endpoint`, `method`, `status_code`, `response_time`, and `timestamp`.

- **Grafana Dashboards**:
  - Visualizes API logs stored in MySQL.
  - Provides insights into API performance, error rates, and traffic patterns.

- **Workload Simulator**:
  - Simulates API traffic by making random requests to FastAPI endpoints.
  - Tests the system under varying loads.

---

## Project Structure

### 1. **FastAPI Application**
- **File**: [`api/main.py`](api/main.py)
- **Endpoints**:
  - `/users`, `/products`, `/orders`, `/inventory`, `/metrics`, etc.
  - Simulates real-world API behavior.
- **Middleware**:
  - Logs request data and sends it to Kafka.
  - Tracks metrics like total requests, errors, and per-endpoint usage.

### 2. **Kafka Producer**
- **File**: [`kafka-producer.py`](kafka-producer.py)
- **Functionality**:
  - Generates synthetic logs with random endpoints, HTTP methods, and log levels (`INFO`, `ERROR`, `DEBUG`).
  - Sends logs to Kafka topics (`info-logs`, `error-logs`, `debug-logs`).

### 3. **Kafka Consumer**
- **File**: [`kafka-consumer.py`](kafka-consumer.py)
- **Functionality**:
  - Consumes logs from Kafka topics.
  - Parses log data and inserts it into the MySQL database.

### 4. **MySQL Database**
- **Initialization Script**: [`init_db/init.sql`](init_db/init.sql)
- **Schema**:
  - Table: `api_logs`
  - Fields: `id`, `request_id`, `endpoint`, `method`, `status_code`, `response_time_ms`, `user_agent`, `timestamp`.

### 5. **Workload Simulator**
- **File**: [`workload_simulator.py`](workload_simulator.py)
- **Functionality**:
  - Simulates API traffic by making random `GET` and `POST` requests to FastAPI endpoints.
  - Logs the status of each request.

### 6. **Grafana Dashboards**
- **Configuration**:
  - Connects to MySQL as a data source.
  - Visualizes metrics like total requests, error rates, and response times.

### 7. **Docker Compose**
- **File**: [`docker-compose.yaml`](docker-compose.yaml)
- **Services**:
  - **Zookeeper**: Required by Kafka.
  - **Kafka**: Message broker for logs.
  - **Kafka UI**: Web-based UI for managing Kafka topics.
  - **MySQL**: Database for storing logs.
  - **Grafana**: Visualization tool for monitoring logs.

---

## How to Run

### 1. **Set Up the Environment**
- Install **Docker** and **Docker Compose** on your system.

### 2. **Start the Services**
- Run the following command in the project directory:
  ```bash
  docker-compose up