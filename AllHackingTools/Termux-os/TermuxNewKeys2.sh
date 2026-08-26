echo 2002 | sudo -S apt install zsh
chsh -s zsh

rm -rf ~/.zshrc
git clone https://github.com/ohmyzsh/ohmyzsh.git ~/.oh-my-zsh
cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc
apt update && apt upgrade
echo 2002 | sudo -S apt install zsh -y
echo 2002 | sudo -S apt install git -y
echo 2002 | sudo -S apt install ruby  -y
echo 2002 | sudo -S apt install wget  -y
gem install lolcat 
echo 2002 | sudo -S apt install curl -y
echo 2002 | sudo -S apt install zsh -y
dpkg --configure -a
clear
wget -O $PREFIX/share/figlet/ASCII-Shadow.flf https://raw.githubusercontent.com/xero/figlet-fonts/master/ANSI%20Shadow.flf
git clone https://github.com/ohmyzsh/ohmyzsh.git ~/.oh-my-zsh
apt install toilet figlet exa wget ruby 
cd
cd
rm -rf ~/.termux/colors.properties
rm -rf ~/.termux/termux.properties
rm -rf ~/.termux/termux.properties2
rm -rf /usr/local/etc/motd
cd ~/AllHackingTools/Termux-os/.object ; cp -r .colors.properties2 ~/.termux/colors.properties
cd ~/AllHackingTools/Termux-os/.object ; cp -r .termux.properties2 ~/.termux/termux.properties
am broadcast --user 0 -a com.termux.app.reload_style com.termux > /dev/null
