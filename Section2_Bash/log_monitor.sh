#!/bin/bash

############################################################
# Log Monitoring Script
# Monitors a log file for "ERROR" and "CRITICAL" messages
# Triggers an alert if >10 errors occur in 5 minutes
# Handles log rotation and missing file scenarios gracefully
#
# Usage:
#   ./log_monitor.sh /path/to/logfile.log
############################################################

LOG_FILE="$1"
ERROR_THRESHOLD=10
TIME_WINDOW=300  # 5 minutes in seconds

# Check if file path is given
if [[ -z "$LOG_FILE" ]]; then
  echo "Usage: $0 /path/to/logfile.log"
  exit 1
fi

# Create temp file to store timestamps
TMP_FILE=$(mktemp)

# Function to clean up on exit
cleanup() {
  rm -f "$TMP_FILE"
  echo "Exiting..."
  exit 0
}

trap cleanup SIGINT SIGTERM

echo "Monitoring $LOG_FILE for ERROR or CRITICAL messages..."

# Tail the file, handling log rotation with --follow=name
tail --follow=name --retry "$LOG_FILE" 2>/dev/null | while read -r line; do
  # Check for matching error patterns
  if [[ "$line" =~ ERROR|CRITICAL ]]; then
    current_time=$(date +%s)
    echo "$current_time" >> "$TMP_FILE"

    # Remove timestamps older than 5 minutes
    awk -v now="$current_time" -v window="$TIME_WINDOW" '$1 >= now - window' "$TMP_FILE" > "${TMP_FILE}.tmp"
    mv "${TMP_FILE}.tmp" "$TMP_FILE"

    # Count recent errors
    count=$(wc -l < "$TMP_FILE")
    if (( count > ERROR_THRESHOLD )); then
      echo "⚠️ ALERT: $count errors in the last 5 minutes"
    fi
  fi
done
