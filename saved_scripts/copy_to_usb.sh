#!/bin/bash

LOG_SOURCE="/home/pi/saved_logs"
USB_DEVICE="/dev/sda1"  # Use the correct partition (usually sda1)
MOUNT_POINT="/media/pi/usb"
DISK="/dev/sda" 
USB_LOG_FOLDER="$MOUNT_POINT/saved_logs"

# Create mount point
mkdir -p "$MOUNT_POINT"

# Mount the USB read-write
if ! mount | grep -q "$MOUNT_POINT"; then
    sudo mount -o rw "$USB_DEVICE" "$MOUNT_POINT"
else
    sudo mount -o remount,rw "$MOUNT_POINT"
fi

# Check if writable
if [ ! -w "$MOUNT_POINT" ]; then
    echo "Error: USB is mounted read-only or has issues. Cannot copy logs."
    exit 1
fi

mkdir -p "$USB_LOG_FOLDER"

# Copy logs into the folder
cp -v "$LOG_SOURCE"/* "$USB_LOG_FOLDER"/

if [ $? -eq 0 ]; then
    echo "Logs copied successfully to $USB_LOG_FOLDER"
else
    echo "Failed to copy logs"
    exit 1
fi

# Wait a second before unmounting
sleep 2

echo "Unmounting USB..."
sudo umount "$MOUNT_POINT"

# Safely ejects the USB
if [ $? -eq 0 ]; then
    echo "USB unmounted. Powering off..."
    sudo udisksctl power-off -b "$DISK"
    echo "USB safe to remove!"
else
    echo "Failed to unmount USB. Please check it manually."
    exit 1
fi