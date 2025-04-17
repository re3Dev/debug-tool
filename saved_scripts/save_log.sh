#!/bin/bash

SOURCE="pi@192.168.4.2:/home/pi/printer_data/logs/klippy.log"
DEST_DIR="/home/pi/saved_logs"
LOG_TIME=$(date +"%T")
KLIPPY_LOG_FILE="klippy_${LOG_TIME}.log"
DMESG_LOG_FILE="dmesg_${LOG_TIME}.log"
KLIPPY_DEST="$DEST_DIR/$KLIPPY_LOG_FILE"
DMESG_DEST="$DEST_DIR/$DMESG_LOG_FILE"
JSON_FILE="/etc/OliveTin/entities/logs.json"

#klippy.log: password A
sshpass -p "raspberry" scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$SOURCE" "$KLIPPY_DEST"

if [ $? -ne 0 ]; then
    # klippy.log: password B
    sshpass -p "Smcc13JLJpA22Jp" scp -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$SOURCE" "$KLIPPY_DEST"

    if [ $? -ne 0 ]; then
        echo "Failed to copy klippy log from printer."
        exit 1
    fi
fi

#dmseg.log: password A
sshpass -p "raspberry" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null pi@192.168.4.2 "dmesg" > "$DMESG_DEST"

if [ $? -ne 0 ]; then
    # dmesg.log: password B
    sshpass -p "Smcc13JLJpA22Jp" ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null pi@192.168.4.2 "dmesg" > "$DMESG_DEST"

    if [ $? -ne 0 ]; then
        echo "Failed to capture dmesg log from printer."
        exit 1
    fi
fi

if [ ! -f "$JSON_FILE" ]; then
    touch "$JSON_FILE"
fi

echo "{\"Name\":\"$KLIPPY_LOG_FILE\"}" >> "$JSON_FILE"
echo "{\"Name\":\"$DMESG_LOG_FILE\"}" >> "$JSON_FILE"