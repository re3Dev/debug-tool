#!/bin/bash

# Set variables
PASSWORD="raspberry"
SOURCE="pi@192.168.4.2:/home/pi/printer_data/logs/klippy.log"
DEST_DIR="/home/pi/saved_logs"
LOG_FILE_NAME="klippy_$(date +"%T").log"
DEST_FILE="$DEST_DIR/$LOG_FILE_NAME"
JSON_FILE="/etc/OliveTin/entities/logs.json"

# Copy the file using sshpass and scp
sshpass -p "$PASSWORD" scp -o StrictHostKeyChecking=no "$SOURCE" "$DEST_FILE"

# Check if the SCP command was successful
if [ $? -eq 0 ]; then
    echo "Success!"

    # Ensure the JSON file exists, initialize if not
    if [ ! -f "$JSON_FILE" ]; then
        touch "$JSON_FILE"
    fi

    # Append the new log file name in JSON format manually
    echo "{\"Name\":\"$LOG_FILE_NAME\"}" >> "$JSON_FILE"


else
    echo "Failed!"
fi
