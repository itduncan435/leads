red='\e[1;31m'
default='\e[0m'
yellow='\e[0;33m'
orange='\e[38;5;166m'
green='\033[92m'

clear
sleep 1
echo -e "$yellow  ___                 __         .__  .__                 "
echo -e "$yellow |   | ____   _______/  |______  |  | |  |   ___________  "    
echo -e "$yellow |   |/    \ /  ___/\   __\__  \ |  | |  | _/ __ \_  __ \ "    
echo -e "$yellow |   |   |  \___  \  |  |  / __ \|  |_|  |_\  ___/|  | \/ "    
echo -e "$yellow |___|___|  /____  > |__| (____  /____/____/\___  >__|    "
echo -e "$yellow          \/     \/            \/               \/        "
echo ""
echo -e "$orange [>] $yellow Tool Name: AllHackingTools "
echo -e "$orange [>] $yellow Developer: Misha Korzhik " 

which git > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e "$green[+]-[Git].............................[ SUCCESFUL ]"
sleep 1.5
else
echo -e "$red[-]-[Git]..........................[ FAILED ]"
sleep 1.5
echo -e "$yellow[!][Installing Module Git...]"
echo 2002 | sudo -S apt install -y git 
fi

which python3 > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e "$green[+]-[Python]..........................[ SUCCESFUL ]"
sleep 1.5
else
echo -e "$red[-]-[Python].......................[ FAILED ]"
sleep 1.5
echo -e "$yellow[!][Installing Module Python...]"
echo 2002 | sudo -S apt install -y python3 python3-pip
fi

which cowsay > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e "$green[+]-[Cowsay]..........................[ SUCCESFUL ]"
sleep 1.5
else
echo -e "$red[-]-[Cowsay].......................[ FAILED ]"
sleep 1.5
echo -e "$yellow[!][Installing Module Cowsay...]"
echo 2002 | sudo -S apt install -y cowsay
fi

which wget > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e "$green[+]-[Wget]............................[ SUCCESFUL ]"
sleep 1.5
else
echo -e "$red[-]-[Wget].........................[ FAILED ]"
sleep 1.5
echo -e "$yellow[!][Installing Module Wget...]"
echo 2002 | sudo -S apt install -y wget
fi

which ruby > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e "$green[+]-[Ruby]............................[ SUCCESFUL ]"
sleep 1.5
else
echo -e "$red[-]-[Ruby].........................[ FAILED ]"
sleep 1.5
echo -e "$yellow[!][Installing Module Ruby...]"
echo 2002 | sudo -S apt install -y ruby 
fi

which toilet > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e "$green[+]-[Toilet]..........................[ SUCCESFUL ]"
sleep 1.5
else
echo -e "$red[-]-[Toilet].......................[ FAILED ]"
sleep 1.5
echo -e "$yellow[!][Installing Module Toilet...]"
echo 2002 | sudo -S apt install -y toilet 
fi

which figlet > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e "$green[+]-[Figlet]..........................[ SUCCESFUL ]"
sleep 1.5
else
echo -e "$red[-]-[Figlet].......................[ FAILED ]"
sleep 1.5
echo -e "$yellow[!][Installing Module Figlet...]"
echo 2002 | sudo -S apt install -y figlet 
fi

which lolcat > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e "$green[+]-[Lolcat]..........................[ SUCCESFUL ]"
sleep 1.5
else
echo -e "$red[-]-[Lolcat].......................[ FAILED ]"
sleep 1.5
echo -e "$yellow[!][Installing Module Lolcat...]"
gem install lolcat
fi

which neofetch > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e "$green[+]-[Neofetch]........................[ SUCCESFUL ]"
sleep 1.5
else
echo -e "$red[-]-[Neofetch].....................[ FAILED ]"
sleep 1.5
echo -e "$yellow[!][Installing Module Neofetch...]"
echo 2002 | sudo -S apt install -y neofetch
fi

which php > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e "$green[+]-[PHP].............................[ SUCCESFUL ]"
sleep 1.5
else
echo -e "$red[-]-[PHP]..........................[ FAILED ]"
sleep 1.5
echo -e "$yellow[!][Installing Module PHP...]"
echo 2002 | sudo -S apt install -y php
fi

which clang > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e "$green[+]-[Clang]...........................[ SUCCESFUL ]"
sleep 1.5
else
echo -e "$red[-]-[Clang]........................[ FAILED ]"
sleep 1.5
echo -e "$yellow[!][Installing Module Clang...]"
echo 2002 | sudo -S apt install -y clang
fi

which zip > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e "$green[+]-[Zip].............................[ SUCCESFUL ]"
sleep 1.5
else
echo -e "$red[-]-[Zip]..........................[ FAILED ]"
sleep 1.5
echo -e "$yellow[!][Installing Module Zip...]"
echo 2002 | sudo -S apt install -y zip
fi

which pip3 > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e "$green[+]-[PIP].............................[ SUCCESFUL ]"
sleep 1.5
else
echo -e "$red[-]-[PIP]..........................[ FAILED ]"
sleep 1.5
echo -e "$yellow[!][Installing Module pip...]"
echo 2002 | sudo -S apt install -y python3-pip
fi

which zsh > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e "$green[+]-[zsh].............................[ SUCCESFUL ]"
sleep 1.5
else
echo -e "$red[-]-[zsh]..........................[ FAILED ]"
sleep 1.5
echo -e "$yellow[!][Installing Module zsh...]"
echo 2002 | sudo -S apt install -y zsh 
fi

which pv > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e "$green[+]-[pv]..............................[ SUCCESFUL ]"
sleep 1.5
else
echo -e "$red[-]-[pv]...........................[ FAILED ]"
sleep 1.5
echo -e "$yellow[!][Installing Module pv...]"
echo 2002 | sudo -S apt install -y pv
fi

which curl > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e "$green[+]-[Curl]............................[ SUCCESFUL ]"
sleep 1.5
else
echo -e "$red[-]-[Curl].........................[ FAILED ]"
sleep 1.5
echo -e "$yellow[!]-[Installing Module Curl...]"
echo 2002 | sudo -S apt install -y curl 
fi

which w3m > /dev/null 2>&1
if [ "$?" -eq "0" ]; then
echo -e "$green[+]-[w3m].............................[ SUCCESFUL ]"
sleep 1.5
else
echo -e "$red[-]-[w3m]..........................[ FAILED ]"
sleep 1.5
echo -e "$yellow[!]-[Installing Module w3m...]"
echo 2002 | sudo -S apt install -y w3m 
fi

red='\e[1;31m'
default='\e[0m'
yellow='\e[0;33m'
orange='\e[38;5;166m'
green='\033[92m'

cd 
cd
cd "$HOME/AllHackingTools"
cd Castom
cp ngrok $HOME/
cd
cd
chmod +x ngrok
sleep 2
echo -e "$yellow[+]-[Ngrok Installed!..............[ INSTALLED ]"
sleep 1.5

echo -e $yellow
echo -n [!] Installing Depencies...= ;
sleep 3 & while [ "$(ps a | awk '{print $1}' | grep $!)" ] ; do for X in '-' '\' '|' '/'; do echo -en "\b$X"; sleep 0.1; done; done 
echo ""

echo 2002 | sudo -S echo 2002 | sudo -S apt-get install -y nodejs
npm install --global speed-test
echo 2002 | sudo -S apt install -y apache2
echo 2002 | sudo -S apt install -y openssl
python3 -m pip install rich --break-system-packages
echo 2002 | sudo -S apt install -y python3-dev
python3 -m pip install passlib --break-system-packages
python3 -m pip install progressbar2 --break-system-packages
python3 -m pip install future --break-system-packages
python3 -m pip install colorama --break-system-packages
python3 -m pip install urllib3 --break-system-packageslib --break-system-packages
python3 -m pip install flask --break-system-packages
python3 -m pip install flask_socketio --break-system-packages
python3 -m pip install flask_cors --break-system-packages
python3 -m pip install mechanize --break-system-packages
python3 -m pip install rich --break-system-packages
