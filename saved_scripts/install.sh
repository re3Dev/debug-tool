#!/bin/bash

chown root:root /home/pi/debug-tool/saved_scripts/install.sh

apt update && apt upgrade -y
apt install dnsmasq -y

# Install OliveTin and setup
dpkg -i /debug-tool/OliveTin_linux_arm64.deb
chmod +x /etc/OliveTin/olivetin_setup.sh
. /pi/saved_scripts/olivetin_setup.sh

chmod +x /pi/saved_scripts/ip_check.sh

# Setup Ethernet
chmod +x /pi/saved_scripts/eth_setup.sh
. /pi/saved_scripts/eth_setup.sh

# Setup static IP on boot
mv /home/pi/debug-tool/saved_scripts/system.service /etc/systemd/system
systemctl enable static-ip.service

reboot