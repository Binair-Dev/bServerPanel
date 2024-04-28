from django.conf import settings
import requests
import os

def downloadFile(url, file_name, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    response = requests.get(url)
    if response.status_code == 200:
        chemin_fichier = os.path.join(destination_folder, file_name)
        
        with open(chemin_fichier, 'wb') as f:
            f.write(response.content)
        return True
    else:
        return False

def runDownload(url, file_name, destination_folder):
    destination_folder = os.path.join(settings.DEFAULT_INSTALLATION_DIRECTORY, destination_folder)
    downloadFile(url, file_name, destination_folder)