apt update && apt upgrade -y

apt install nano bzip2 ufw software-properties-common dirmngr apt-transport-https gnupg2 ca-certificates lsb-release debian-archive-keyring wget -y

ufw allow 22
ufw allow 9987/udp
ufw allow 30033/tcp
ufw allow 10011/tcp
ufw allow 10022/tcp
ufw allow 10080/tcp
ufw enable

TVERSION=3.13.7
wget https://files.teamspeak-services.com/releases/server/${TVERSION}/teamspeak3-server_linux_amd64-${TVERSION}.tar.bz2
tar xfvj teamspeak3-server_linux_amd64-${TVERSION}.tar.bz2
chmod +rw /teamspeak3-server_linux_amd64/*