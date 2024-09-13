#!/bin/bash


PYTHON_SCRIPT1='/home/sghandi/Téléchargements/wemon-main/mynetwork.py'
PYTHON_SCRIPT2='/home/sghandi/Téléchargements/wemon-main/automation.py'
DIRECTORY_PATH='/home/sghandi/Téléchargements/wemon-main/'  




sudo python3 $PYTHON_SCRIPT1 

touch /tmp/script1_done
while [ ! -f /tmp/script1_done ]; do
sleep 1
done
rm /tmp/script1_done
gnome-terminal --wait -- /bin/bash -c "cd '$DIRECTORY_PATH' && python3 $PYTHON_SCRIPT2 '/home/sghandi/Téléchargements/wemon-main/urls/urls.txt'; exec bash"
sleep 2
sudo mn -c
echo "########### i cleared network "
done < "$INPUT_FILE"
