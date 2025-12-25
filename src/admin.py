import json
import os
from src.book import BookManager
from src.reader import ReaderManager
from src.borrow_return import BorrowManager
from src.utils import ensure_data_dir

class AdminSystem:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, "users.json")
        ensure_data_dir(data_dir)
        
        # Đảm bảo có file users và tài khoản admin mặc định
        if not os.path.exists(self.users_file):
            self.save_users([{"username": "admin", "password": "123", "role": "admin", "reader_id": None}])

        # Khởi tạo các module khác
        self.book_manager = BookManager(path=os.path.join(data_dir, "books.json"))
        self.reader_manager = ReaderManager(path=os.path.join(data_dir, "readers.json"))
        self.borrow_manager = BorrowManager(
            os.path.join(data_dir, "borrows.json"), 
            self.book_manager, 
            self.reader_manager
        )

    def load_users(self):
        try:
            with open(self.users_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def save_users(self, users):
        with open(self.users_file, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=4)

    def login(self, username, password):
        users = self.load_users()
        for user in users:
            if user.get("username") == username and user.get("password") == password:
                return user
        return None

    def register_user(self, username, password, role="reader", reader_id=None):
        users = self.load_users()
        if any(u.get("username") == username for u in users):
            return "❌ Username exists"
        users.append({"username": username, "password": password, "role": role, "reader_id": reader_id})
        self.save_users(users)
        return "✔ User created"
