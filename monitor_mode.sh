#!/bin/bash

# Check if wlan1 exists
if ! iwconfig wlx001ea6ff9116 > /dev/null 2>&1; then
    echo "Error: wlan1 interface not found!"
    exit 1
fi

echo "[+] Setting wlan1 down..."
sudo ip link set wlx001ea6ff9116 down

echo "[+] Enabling monitor mode..."
sudo iw dev wlx001ea6ff9116 set type monitor

echo "[+] Setting wlan1 up..."
sudo ip link set wlx001ea6ff9116 up

echo "[+] Verifying mode..."
iwconfig wlx001ea6ff9116 | grep "Mode"

echo "[+] Done! wlan1 is now in monitor mode."

