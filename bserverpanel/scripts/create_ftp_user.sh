#!/bin/bash
if [ "$(id -u)" != "0" ]; then
   echo "Ce script doit être exécuté en tant que root" 1>&2
   exit 1
fi
if [ $# -ne 3 ]; then
    echo "Usage: $0 <nom_utilisateur> <mot_de_passe> <répertoire>"
    exit 1
fi
nom_utilisateur=$1
mot_de_passe=$2
repertoire=$3

useradd -m $nom_utilisateur
echo "$nom_utilisateur:$mot_de_passe" | chpasswd
mkdir -p $repertoire
chown -R $nom_utilisateur:$nom_utilisateur $repertoire
echo "\n# Configuration pour $nom_utilisateur" >> /etc/vsftpd.conf
echo "local_root=$repertoire" >> /etc/vsftpd.conf
echo "$nom_utilisateur" >> /etc/vsftpd.user_list
systemctl restart vsftpd
echo "Utilisateur $nom_utilisateur créé avec succès avec le mot de passe spécifié et configuré pour le dossier $dossier."
