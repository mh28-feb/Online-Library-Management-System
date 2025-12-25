import json
import os
from src.utils import ensure_data_dir

class AuthManager:
    def __init__(self, path="data/users.json"):
        self.path = path
        ensure_data_dir(os.path.dirname(self.path))
        # Tạo admin mặc định nếu file chưa tồn tại
        if not os.path.exists(self.path):
            self._save_users([{"username": "admin", "password": "123", "role": "admin", "reader_id": None}])

    def _load_users(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def _save_users(self, users):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=4)

    def login(self, username, password):
        users = self._load_users()
        for u in users:
            if u["username"] == username and u["password"] == password:
                return u
        return None

    def register_user(self, username, password, role="reader", reader_id=None):
        users = self._load_users()
        if any(u["username"] == username for u in users):
            return {"error": "Username already exists"}
        
        new_user = {
            "username": username,
            "password": password,
            "role": role,
            "reader_id": reader_id
        }
        users.append(new_user)
        self._save_users(users)
        return {"status": "ok", "user": username}
