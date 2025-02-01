# Description: This script is used to run the main.py script and log the output to a file.
#              This script is to be called by the cron job scheduler.


#!/bin/bash

# Define log file location (fixed name)
LOG_DIR="$(pwd)/cronjob_logs"
LOG_FILE="$LOG_DIR/cron_job.log"

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

#  Appends logs to the file.
echo "New log entry" >> "$LOG_FILE"

# Log start time
echo "=====================================================================" >> "$LOG_FILE"
echo "Cron job started at $(date)" >> "$LOG_FILE"
echo "=====================================================================" >> "$LOG_FILE"

# Execute your command/script and log both stdout and stderr
python3 ./main.py >> "$LOG_FILE" 2>&1

# Log end time
echo "=====================================================================" >> "$LOG_FILE"
echo "Cron job ended at $(date)" >> "$LOG_FILE"
echo "=====================================================================" >> "$LOG_FILE"
echo -e "\n" >> "$LOG_FILE"
echo -e "\n" >> "$LOG_FILE"


