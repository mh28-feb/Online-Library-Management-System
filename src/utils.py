import os

def ensure_data_dir(directory="data"):
    if not os.path.exists(directory):
        os.makedirs(directory)
