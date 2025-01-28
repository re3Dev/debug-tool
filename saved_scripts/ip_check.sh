#!/bin/bash

chown root:root /home/pi/saved_scripts/ip_check

nmcli connection modify "Wired connection 1" ipv4.addresses 192.168.4.1/24 ipv4.method manual
nmcli connection down "Wired connection 1"
nmcli connection up "Wired connection 1"