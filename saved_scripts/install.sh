#!/bin/bash

chown root:root /pi/debug-tool/saved_scripts/install.sh

apt update
apt install dnsmasq -y

chmod +x /pi/saved_scripts/ip_check.sh
chmod +x /pi/saved_scripts/eth_setup.sh
chmod +x /etc/OliveTin/olivetin_setup.sh

./pi/saved_scripts/ip_check.sh
./pi/saved_scripts/eth_setup.sh
