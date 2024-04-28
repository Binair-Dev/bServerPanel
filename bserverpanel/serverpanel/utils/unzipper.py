import os
import zipfile
import tarfile

def decompress_archive(archive_path, extract_to=None):
    if not os.path.exists(archive_path):
        return False
    
    if extract_to is None:
        extract_to = os.path.dirname(archive_path)
    
    if zipfile.is_zipfile(archive_path):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        return True
    elif tarfile.is_tarfile(archive_path):
        with tarfile.open(archive_path, 'r') as tar_ref:
            tar_ref.extractall(extract_to)
        return True
    elif archive_path.endswith('.tar.bz2'):
        with tarfile.open(archive_path, 'r:bz2') as tar_ref:
            tar_ref.extractall(extract_to)
        return True
    else:
        return False
