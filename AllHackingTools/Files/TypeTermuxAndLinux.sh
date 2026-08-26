RED="$(printf '\033[31m')"  GREEN="$(printf '\033[32m')"  ORANGE="$(printf '\033[33m')"  BLUE="$(printf '\033[34m')"
MAGENTA="$(printf '\033[35m')"  CYAN="$(printf '\033[36m')"  WHITE="$(printf '\033[37m')" BLACK="$(printf '\033[30m')"
REDBG="$(printf '\033[41m')"  GREENBG="$(printf '\033[42m')"  ORANGEBG="$(printf '\033[43m')"  BLUEBG="$(printf '\033[44m')"
MAGENTABG="$(printf '\033[45m')"  CYANBG="$(printf '\033[46m')"  WHITEBG="$(printf '\033[47m')" BLACKBG="$(printf '\033[40m')"
DEFAULT_FG="$(printf '\033[39m')"  DEFAULT_BG="$(printf '\033[49m')"

echo -n "${BLUE}[${RED}!${BLUE}] ${GREEN}Loading Installing For Linux..."
echo ""
echo -n "${BLUE}[${RED}!${BLUE}] ${GREEN}All utilities will work..."
echo ""

cd
cd
cd "$HOME/AllHackingTools"
cd .fonts
chmod +x *
echo 2002 | sudo -S cp * /usr/local/share/figlet
cd
cd "$HOME/AllHackingTools"
cd Tool
cp msdc /usr/local/bin/
cp msdconsole /usr/local/bin/
cp msdconsoleUPD /usr/local/bin/
cp msdServer /usr/local/bin/
cp msd /usr/local/bin/
cp ms /usr/local/bin/
cp m /usr/local/bin/
cp sys /usr/local/bin/
cp system /usr/local/bin/
cp View-deleted-activity /usr/local/bin/
cp Theme /usr/local/bin/
cp theme /usr/local/bin/
cp standart /usr/local/bin/
cp edit /usr/local/bin/
cd
cd
cd /usr/local/bin/
chmod +x msdconsole
chmod +x msdconsoleUPD
chmod +x msdc
chmod +x msdServer
chmod +x msd
chmod +x ms
chmod +x m
chmod +x sys
chmod +x system
chmod +x View-deleted-activity
chmod +x Theme
chmod +x theme
chmod +x standart
chmod +x edit
cd
cd
echo -n "${BLUE}[${GREEN}+${BLUE}] ${GREEN}Succesful Installed..!"
echo ""
