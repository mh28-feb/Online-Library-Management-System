import os
from src.book import BookManager
from src.reader import ReaderManager
from src.borrow_return import BorrowManager
from src.utils import ensure_data_dir

class AdminSystem:
    """Lớp điều phối kết nối các bộ quản lý dữ liệu."""
    
    def __init__(self, data_dir="data"):
        ensure_data_dir(data_dir)
        
        # Thiết lập đường dẫn file
        books_path = os.path.join(data_dir, "books.json")
        readers_path = os.path.join(data_dir, "readers.json")
        borrows_path = os.path.join(data_dir, "borrows.json")

        # Khởi tạo các Manager
        self.book_manager = BookManager(path=books_path)
        self.reader_manager = ReaderManager(path=readers_path)
        self.borrow_manager = BorrowManager(borrows_path, self.book_manager, self.reader_manager)
