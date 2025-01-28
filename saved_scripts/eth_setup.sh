#!/bin/bash

chown root:root /home/pi/debug-tool/saved_scripts/eth_setup

# Enable and start systemd-networkd
systemctl enable systemd-networkd
systemctl restart systemd-networkd

# Add DHCP configuration for eth0
bash -c 'cat <<EOL >> /etc/dnsmasq.conf
# DHCP Configuration for Ethernet interface (eth0)
interface=eth0
bind-dynamic
dhcp-range=192.168.4.2,192.168.4.2,255.255.255.0,24h
EOL'

# Restart dhcpcd and dnsmasq
systemctl restart dhcpcd

systemctl start dnsmasq
systemctl enable dnsmasq

# Add static IP configuration for eth0
bash -c 'cat <<EOL >> /etc/systemd/network/10-eth0.network
[Match]
Name=eth0

[Network]
Address=192.168.4.1/24
EOL'

echo "Setup complete. DHCP configuration added and dnsmasq restarted."