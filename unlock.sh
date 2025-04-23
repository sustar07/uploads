#!/bin/bash

# Wake up device
adb shell input keyevent POWER
sleep 1

# Swipe up to unlock
adb shell input swipe 500 1800 500 800
sleep 1

# Enter PIN 0808
adb shell input tap 563 1850  # 0
sleep 0.2
adb shell input tap 563 1680  # 8
sleep 0.2
adb shell input tap 563 1850  # 0
sleep 0.2
adb shell input tap 563 1680  # 8
sleep 0.2

# Confirm (if needed, replace with your Enter button coordinates)
# adb shell input tap x y

