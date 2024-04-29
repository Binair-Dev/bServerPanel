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

def find_logs_directory(root_directory):
    for dirpath, _, _ in os.walk(root_directory):
        logs_dir = os.path.join(dirpath, "logs")
        if os.path.exists(logs_dir):
            return logs_dir
    return None

def get_latest_log_file(root_directory):
    logs_directory = find_logs_directory(root_directory)
    if logs_directory:
        log_files = [os.path.join(logs_directory, f) for f in os.listdir(logs_directory) if os.path.isfile(os.path.join(logs_directory, f))]

        if not log_files:
            return None

        latest_log_file = max(log_files, key=os.path.getmtime)
        return latest_log_file
    else:
        return None
    
def get_logs_with_token(root_directory):
    logs_directory = find_logs_directory(root_directory)
    if logs_directory:        
        log_files = [os.path.join(logs_directory, f) for f in os.listdir(logs_directory) if os.path.isfile(os.path.join(logs_directory, f))]
        if not log_files:
            return
        for log_file in log_files:
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as file:
                for line in file:
                    if "token=" in line:
                        token = line.strip().split("token=")[1]
                        return token
    return None
