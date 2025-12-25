import os

def ensure_data_dir(directory="data"):
    """Đảm bảo thư mục dữ liệu tồn tại."""
    if not os.path.exists(directory):
        os.makedirs(directory)
