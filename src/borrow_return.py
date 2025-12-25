import json
import os
from datetime import datetime, timedelta
from src.utils import ensure_data_dir

class BorrowManager:
    def __init__(self, path="data/borrows.json", book_manager=None, reader_manager=None):
        self.path = path
        self.book_manager = book_manager
        self.reader_manager = reader_manager
ensure_data_dir(os.path.dirname(self.path))
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

    # ===============================================================
    #                         BORROW BOOK
    # ===============================================================
    def borrow_book(self, reader_id, book_id):

        # Check if reader exists
        reader = self.reader_manager.view_reader_info(reader_id)
        if isinstance(reader, str):
            return "Reader not found"

        # Check if book exists
        books = self.book_manager.get_all_books()
        book = next((b for b in books if b["id"] == book_id), None)
        if not book:
            return "Book not found"

        # Check if book is available
        if book["status"] != "Available":
            return "Book is currently not available"

        # Create borrow record
        borrows = self._load()
        borrow_record = {
            "reader_id": reader_id,
            "book_id": book_id,
            "borrow_date": datetime.now().strftime("%Y-%m-%d"),
            "due_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "status": "Borrowed"
        }

        borrows.append(borrow_record)
        self._save(borrows)

        # Update book status
        book["status"] = "Borrowed"
        self.book_manager._save(books)

        # Update history
        reader["borrowed_books"].append(book_id)
        reader["history"].append({
            "action": "borrow",
            "book_id": book_id,
            "date": datetime.now().strftime("%Y-%m-%d")
        })

        readers = self.reader_manager._load()
        for r in readers:
            if r["reader_id"] == reader_id:
                r.update(reader)
        self.reader_manager._save(readers)

        return f"Book borrowed successfully! Due date: {borrow_record['due_date']}"

    # ===============================================================
    #                         RETURN BOOK
    # ===============================================================

    def return_book(self, reader_id, book_id):
        borrows = self._load()

        # Find the active borrow record
        record = next(
            (b for b in borrows if b["reader_id"] == reader_id and b["book_id"] == book_id and b["status"] == "Borrowed"),
            None
        )

        if not record:
            return "No valid borrowing transaction found"

        # Update the record
        record["status"] = "Returned"
        record["return_date"] = datetime.now().strftime("%Y-%m-%d")
        self._save(borrows)

        # Update book status
        books = self.book_manager.get_all_books()
        for b in books:
            if b["id"] == book_id:
                b["status"] = "Available"
        self.book_manager._save(books)

        # Update reader history
        reader = self.reader_manager.view_reader_info(reader_id)
        reader["history"].append({
            "action": "return",
            "book_id": book_id,
            "date": datetime.now().strftime("%Y-%m-%d")
        })
        if book_id in reader["borrowed_books"]:
            reader["borrowed_books"].remove(book_id)

        readers = self.reader_manager._load()
        for r in readers:
            if r["reader_id"] == reader_id:
                r.update(reader)
        self.reader_manager._save(readers)

        return "Book returned successfully!"

    # ===============================================================
    #                   CALCULATE FINE (OPTIONAL)
    # ===============================================================

    def calculate_fine(self, reader_id, book_id):
        borrows = self._load()

        record = next(
            (b for b in borrows if b["reader_id"] == reader_id and b["book_id"] == book_id),
            None
        )
        if not record:
            return "❌ Transaction not found"

        due = datetime.strptime(record["due_date"], "%Y-%m-%d")

        today = datetime.now()

        if today <= due:
            return "✔ No fine, returned on time."

        days_late = (today - due).days
        fine = days_late * 5000  # 5000 VND/day

        return f"❌ {days_late} days overdue. Fine: {fine}VND"

    # ===============================================================
    #                         RENEW BOOK
    # ===============================================================

    def renew_book(self, reader_id, book_id):
        borrows = self._load()

        record = next(
            (b for b in borrows if b["reader_id"] == reader_id and b["book_id"] == book_id and b["status"] == "Borrowed"),
            None
        )

        if not record:
            return "❌ Cannot renew this transaction"

        # Add 7 days
        due = datetime.strptime(record["due_date"], "%Y-%m-%d")
        new_due = due + timedelta(days=7)

        record["due_date"] = new_due.strftime("%Y-%m-%d")
        self._save(borrows)

        return f"✔ Renewed successfully! New due date: {record['due_date']}"
