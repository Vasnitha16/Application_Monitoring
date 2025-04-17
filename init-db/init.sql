USE monitoring;

CREATE TABLE IF NOT EXISTS api_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    request_id VARCHAR(255),
    endpoint VARCHAR(255),
    method VARCHAR(10),
    status_code INT,
    response_time_ms FLOAT,
    user_agent TEXT,
    timestamp DATETIME
);
