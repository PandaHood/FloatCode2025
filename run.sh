#!/bin/bash

# Run the first Python script
echo "Running first_script.py..."
python3 info.py

# Run the second Python script
echo "Running second_script.py..."
screen -dmS mysession python3 /path/to/script.py