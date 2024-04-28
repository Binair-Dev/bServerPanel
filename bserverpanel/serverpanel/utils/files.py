import os
from django.conf import settings

def create_directory(directory_name):
    directory_path = os.path.join(settings.BASE_DIR, directory_name)  # BASE_DIR est le répertoire racine de votre projet Django
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def list_files_in_directory(directory_name):
    directory_path = os.path.join(settings.BASE_DIR, directory_name)
    if os.path.exists(directory_path):
        files = os.listdir(directory_path)
        return files
    else:
        return None

def write_file(file_name, destination_folder, content):
    folder = os.path.join(settings.DEFAULT_INSTALLATION_DIRECTORY, destination_folder)
    file_path = os.path.join(folder, file_name)
    with open(file_path, 'w') as f:
        f.write(content)

def create_eula_file(destination_folder):
    folder = os.path.join(settings.DEFAULT_INSTALLATION_DIRECTORY, destination_folder)
    file_path = os.path.join(folder, "eula.txt")
    with open(file_path, 'w') as f:
        f.write("eula=true")