import json
import os
import re

class ReaderManager:
    def __init__(self, path="data/readers.json"):
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
    #       VALIDATE EMAIL
    # =============================

    def _is_valid_email(self, email):
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

    # ==================================================
    #                 REGISTER READER
    # ==================================================
    def register_reader(self, reader_id_or_name, name_or_email=None, email=None):
        """Support two signatures:
        1. register_reader(name, email) - old API
        2. register_reader(reader_id, name, email) - test API
        """
        # Detect which signature is being used
        if email is not None:
            # Three-parameter call: register_reader(reader_id, name, email)
            reader_id = reader_id_or_name
            name = name_or_email
        else:
            # Two-parameter call (old): register_reader(name, email)
            # Auto-generate the ID
            name = reader_id_or_name
            email = name_or_email
            reader_id = None

        if not self._is_valid_email(email):
            return False

        readers = self._load()

        # Check for duplicate ID if provided
        if reader_id is not None:
            for r in readers:
                if r.get("reader_id") == reader_id:
                    return False  # Duplicate ID

        # Auto-generate ID if not provided
        if reader_id is None:
            reader_id = str(len(readers) + 1)

        reader = {
            "reader_id": reader_id,
            "name": name,
            "email": email,
            "borrowed_books": [],
            "history": []
        }

        readers.append(reader)
        self._save(readers)

        # Return the reader object for test compatibility, or a success message for CLI
        return reader if email is not None else f"✔ Reader registered successfully! ID: {reader_id}"

    # ==================================================
    def view_reader_info(self, reader_id):
        for r in self._load():
            if r["reader_id"] == reader_id:
                return r
        return "❌ Reader not found"

    def get_reader_by_id(self, reader_id):
        """Test-friendly version of view_reader_info"""
        for r in self._load():
            if r.get("reader_id") == reader_id:
                return r
        return None

    def add_to_history(self, reader_id, entry):
        """Add entry to reader's history"""
        readers = self._load()
        for i, r in enumerate(readers):
            if r.get("reader_id") == reader_id:
                r.setdefault("history", []).append(entry)
                readers[i] = r
                self._save(readers)
                return True
        return False

    def view_history(self, reader_id):
        for r in self._load():
            if r["reader_id"] == reader_id:
                return r.get("history", [])
        return "❌ Reader not found"