#!/bin/bash  

#tmux new-session -d -s dataserial 'python3 /home/arno/Ender-X-3000/Datacom/SerialCommunication.py'
#tmux new-session -d -s dataapp 'python3 /home/arno/Ender-X-3000/Datacom/App.py'
python3 /home/arno/Ender-X-3000/www/backend/app.py

#trap "tmux kill-session -t dataserial; tmux kill-session -t dataapp; tmux kill-session -t backend; exit" HUP INT TERM

#while :; do sleep 5; done;

exit 0