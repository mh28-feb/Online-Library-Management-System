import json
import os
from src.utils import ensure_data_dir
class BookManager:
    def __init__(self, path="data/books.json"):
        self.path = path
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write("[]")

    def _load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def _save(self, data):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # =============================
    #       ADD BOOK (COMPLETE)
    # =============================
    def add_book(self, title, author, publisher, year):
        books = self._load()

        new_id = len(books) + 1
        book = {
            "id": str(new_id),
            "title": title,
            "author": author,
            "publisher": publisher,
            "year": year,
            "status": "Available"
        }

        books.append(book)
        self._save(books)

        return f"Book added successfully! ID: {new_id}"

    def get_all_books(self):
        return self._load()
