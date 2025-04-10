#!/bin/bash

SOURCE="pi@192.168.4.2:/home/pi/printer_data/logs/klippy.log"
DEST_DIR="/home/pi/saved_logs"
LOG_FILE_NAME="klippy_$(date +"%T").log"
DEST_FILE="$DEST_DIR/$LOG_FILE_NAME"
JSON_FILE="/etc/OliveTin/entities/logs.json"

# Try with password A
sshpass -p "raspberry" scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$SOURCE" "$DEST_FILE"

if [ $? -eq 0 ]; then
    echo "Success"
else
    # Try with password B
    sshpass -p "Smcc13JLJpA22Jp" scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$SOURCE" "$DEST_FILE"
    
    if [ $? -eq 0 ]; then
        echo "Success"
    else
        echo "Failed to copy log from printer."
        exit 1
    fi
fi

if [ ! -f "$JSON_FILE" ]; then
    touch "$JSON_FILE"
fi

echo "{\"Name\":\"$LOG_FILE_NAME\"}" >> "$JSON_FILE"