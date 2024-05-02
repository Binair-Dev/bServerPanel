apt update && apt upgrade -y

apt install nano wine sqlite3 bzip2 xinit ufw software-properties-common dirmngr apt-transport-https gnupg2 ca-certificates lsb-release debian-archive-keyring wget vsftpd -y

#Configuration VSFTP
echo "write_enable=YES" >> $vsftpd_conf
echo "chroot_local_user=YES" >> $vsftpd_conf
echo "allow_writeable_chroot=YES" >> $vsftpd_conf
systemctl restart vsftpd

#Configuration UFW pour accepter toutes les connexions entrantes (Paramêtrer Docker ensuite pour la plage de port en fonction des serveurs)
ufw reset
ufw enable

TVERSION=3.13.7
wget https://files.teamspeak-services.com/releases/server/${TVERSION}/teamspeak3-server_linux_amd64-${TVERSION}.tar.bz2
tar xfvj teamspeak3-server_linux_amd64-${TVERSION}.tar.bz2
chmod +rw /teamspeak3-server_linux_amd64/*