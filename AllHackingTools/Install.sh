#!/bin/bash
g="\033[1;32m"
r="\033[1;31m"
b="\033[1;34m"
w="\033[0m"
red='\e[1;31m'
default='\e[0m'
yellow='\e[0;33m'
orange='\e[38;5;166m'
green='\033[92m'

clear
sleep 1.5
echo -e "$default"

echo 2002 | sudo -S apt update
echo 2002 | sudo -S apt upgrade -y
echo 2002 | sudo -S apt install -y python3 python3-pip git wget curl php toilet figlet zip lolcat pv zsh neofetch ruby jq apache2 openssh-client w3m

pip3 install --break-system-packages requests colorama rich paramiko future flask flask_socketio flask_cors passlib progressbar2 smtplib

cd "$HOME/AllHackingTools"
python3 src/InstallMenu.py
