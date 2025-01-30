MAC_ADDRESS="DC:2C:26:15:FB:E0"

# Start bluetoothctl and send commands
bluetoothctl <<EOF
power on
agent on
connect $MAC_ADDRESS
exit
EOF

sleep 10

# Check if connection was successful
if bluetoothctl info "$MAC_ADDRESS" | grep -q "Connected: yes"; then
    echo "Successfully connected to $MAC_ADDRESS"
else
    echo "Retrying connection..."
    bluetoothctl <<EOF
    connect $MAC_ADDRESS
    exit
EOF
fi
