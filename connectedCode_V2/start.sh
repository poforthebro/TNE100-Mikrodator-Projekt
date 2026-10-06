#!/bin/bash

# 1. Check if pigpiod is already running. 
# If it is NOT running, start it. 
# This prevents the "Can't lock" error if it's already active.
if ! pgrep -x "pigpiod" > /dev/null; then
    sudo pigpiod &
    # Wait 2 seconds to give it a moment to initialize
    sleep 2
fi

# 2. Launch the terminal window.
# IMPORTANT: Run this script WITHOUT 'sudo'.
source ~/myenv/bin/activate
python3 main.py
