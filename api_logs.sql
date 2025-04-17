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

SELECT 
    endpoint, 
    COUNT(*) AS request_count
FROM 
    api_logs
GROUP BY 
    endpoint
ORDER BY 
    request_count DESC;



SELECT 
    DATE_FORMAT(timestamp, '%Y-%m-%d %H:00:00') AS hour_slot,
    AVG(response_time_ms) AS avg_response_time
FROM 
    api_logs
GROUP BY 
    hour_slot
ORDER BY 
    hour_slot;



SELECT 
    endpoint, 
    status_code, 
    COUNT(*) AS error_count
FROM 
    api_logs
WHERE 
    status_code >= 400
GROUP BY 
    endpoint, status_code
ORDER BY 
    error_count DESC;


truncate table api_logs;
select * from api_logs;