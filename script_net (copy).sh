#!/bin/bash

INPUT_FILE='/home/sghandi/Téléchargements/wemon-main/parameter_file1.txt'
PYTHON_SCRIPT1='/home/sghandi/Téléchargements/wemon-main/network2.py'
PYTHON_SCRIPT2='/home/sghandi/Téléchargements/wemon-main/automation.py'
DIRECTORY_PATH='/home/sghandi/Téléchargements/wemon-main/'  

# Check if the input file exists
if [[ ! -f $INPUT_FILE ]]; then
    echo "Error: File $INPUT_FILE does not exist."
    exit 1
fi

# Read each line from the input file
while IFS= read -r line
do
    echo "Starting Mininet setup with parameters: $line"
    sudo python3 $PYTHON_SCRIPT1 $line &
    sleep 10
    MININET_PID=$!
    echo "Mininet started with PID: $MININET_PID"

    # Run the second Python script
    python3 $PYTHON_SCRIPT2 '/home/sghandi/Téléchargements/wemon-main/urls/urls.txt'
    echo "Script 2 completed. Stopping Mininet setup..."
    
    # Kill the Mininet process
    sudo kill $MININET_PID
    wait $MININET_PID  # Ensure the process has finished cleanup

    # Clear Mininet to ensure no residual data
    sudo mn -c
    echo "########### Network cleared."
done < "$INPUT_FILE"

