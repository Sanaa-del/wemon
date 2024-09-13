#!/bin/bash

INPUT_FILE='/home/sghandi/Téléchargements/wemon-main/parameter_file.txt'
PYTHON_SCRIPT1='/home/sghandi/Téléchargements/wemon-main/network2.py'
PYTHON_SCRIPT2='/home/sghandi/Téléchargements/wemon-main/automation.py'
DIRECTORY_PATH='/home/sghandi/Téléchargements/wemon-main/'  
FLAG_FILE='/tmp/mininet_done.flag'
TIMEOUT=300  # Timeout in seconds for waiting for the flag file
START_LINE=1811  # The line number to start from

if [[ ! -f $INPUT_FILE ]]; then
    echo "Error: File $INPUT_FILE does not exist."
    exit 1
fi

# Skip the first START_LINE-1 lines and start reading from the START_LINE
tail -n +$START_LINE "$INPUT_FILE" | while IFS= read -r line
do
    echo "Starting Mininet setup with parameters: $line"
    line_number=$(echo "$line" | awk '{print $1}')
    # Remove any existing flag file
    sudo rm -f $FLAG_FILE
    
    sudo python3 $PYTHON_SCRIPT1 $line &
    
    MININET_PID=$!
    echo "Mininet started with PID: $MININET_PID"
    
    # Wait for the flag file to be created by PYTHON_SCRIPT1
    while [[ ! -f $FLAG_FILE ]]; do
        sleep 1
    done
    
    # Start the second Python script after the flag file is created
    echo "Flag detected. Running Script 2..."
    python3 $PYTHON_SCRIPT2 '/home/sghandi/Téléchargements/fixed_urls.txt' '/home/sghandi/Téléchargements/cluster0_urls.txt' '/home/sghandi/Téléchargements/cluster1_urls.txt' '/home/sghandi/Téléchargements/cluster2_urls.txt' '/home/sghandi/Téléchargements/cluster3_urls.txt' $line_number
    echo "Script 2 completed. Stopping Mininet setup..."
    sudo kill $MININET_PID
    wait $MININET_PID  # Ensure the process has finished cleanup
    sudo mn -c
    echo "########### Network cleared."
done


