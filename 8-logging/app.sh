#!/bin/bash

LOG_FILE="/home/ubuntu/logging-app/application.log"

echo "Starting centralized logging demo application..."
echo "Logs will be written to: $LOG_FILE"

while true
do
    echo "$(date '+%Y-%m-%d %H:%M:%S') INFO Application started successfully" >> "$LOG_FILE"

    sleep 5

    echo "$(date '+%Y-%m-%d %H:%M:%S') INFO User request processed successfully" >> "$LOG_FILE"

    sleep 5

    echo "$(date '+%Y-%m-%d %H:%M:%S') WARNING High response time detected" >> "$LOG_FILE"

    sleep 5

    echo "$(date '+%Y-%m-%d %H:%M:%S') ERROR Database connection failed" >> "$LOG_FILE"

    sleep 5

    echo "$(date '+%Y-%m-%d %H:%M:%S') INFO Database connection restored" >> "$LOG_FILE"

    sleep 5
done