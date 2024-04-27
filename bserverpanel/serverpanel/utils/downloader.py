import requests
import os

def downloadFile(url, nom_fichier, dossier_destination):
    if not os.path.exists(dossier_destination):
        os.makedirs(dossier_destination)

    response = requests.get(url)
    if response.status_code == 200:
        chemin_fichier = os.path.join(dossier_destination, nom_fichier)
        
        with open(chemin_fichier, 'wb') as f:
            f.write(response.content)
        
        print("Téléchargement terminé avec succès.")
    else:
        print("Échec du téléchargement.")

url_fichier = "https://api.papermc.io/v2/projects/paper/versions/1.20.4/builds/496/downloads/paper-1.20.4-496.jar"
nom_fichier_telecharge = "paper-1.20.4-496.jar"
dossier_destination = "test-folder/paper"
downloadFile(url_fichier, nom_fichier_telecharge, dossier_destination)
