import os
from src.book import BookManager
from src.reader import ReaderManager
from src.borrow_return import BorrowManager
from src.auth import AuthManager
from src.utils import ensure_data_dir

class AdminSystem:
    def __init__(self, data_dir="data"):
        ensure_data_dir(data_dir)
        
        self.auth_manager = AuthManager(os.path.join(data_dir, "users.json"))
        self.book_manager = BookManager(path=os.path.join(data_dir, "books.json"))
        self.reader_manager = ReaderManager(path=os.path.join(data_dir, "readers.json"))
        self.borrow_manager = BorrowManager(
            os.path.join(data_dir, "borrows.json"), 
            self.book_manager, 
            self.reader_manager
        )
