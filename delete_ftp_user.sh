#!/bin/bash
if [ "$(id -u)" != "0" ]; then
   echo "Ce script doit être exécuté en tant que root" 1>&2
   exit 1
fi
if [ $# -ne 1 ]; then
    echo "Usage: $0 <nom_utilisateur>"
    exit 1
fi
nom_utilisateur=$1
userdel -r $nom_utilisateur
sed -i "/# Configuration pour $nom_utilisateur/,/local_root=\/home\/$nom_utilisateur\/ftp\/.*/d" /etc/vsftpd.conf
sed -i "/$nom_utilisateur/d" /etc/vsftpd.user_list
systemctl restart vsftpd
echo "Utilisateur $nom_utilisateur supprimé avec succès ainsi que toutes les configurations associées."
