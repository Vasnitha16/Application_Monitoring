CREATE DATABASE IF NOT EXISTS monitoring;

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

SELECT endpoint, COUNT(*) AS request_count
FROM api_logs
GROUP BY endpoint
ORDER BY request_count DESC;
