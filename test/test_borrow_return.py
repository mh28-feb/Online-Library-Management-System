import os
import json

from book import BookManager
from reader import ReaderManager
from borrow_return import BorrowManager


TEST_BOOKS = "data/test_books.json"
TEST_READERS = "data/test_readers.json"
TEST_BORROWS = "data/test_borrows.json"


def setup_function():
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    # Reset test JSON files
    with open(TEST_BOOKS, "w", encoding="utf-8") as f:
        f.write("[]")
    with open(TEST_READERS, "w", encoding="utf-8") as f:
        f.write("[]")
    with open(TEST_BORROWS, "w", encoding="utf-8") as f:
        f.write("[]")


def test_borrow_book_success():
    bm = BookManager(TEST_BOOKS)
    rm = ReaderManager(TEST_READERS)
    br = BorrowManager(TEST_BORROWS, bm, rm)

    # Note: These add_book/register_reader calls return English success messages
    bm.add_book("Python", "Jack", "CNTT", "2024")
    rm.register_reader("Duy", "duy@gmail.com")

    # Assuming auto-IDs are "1" and "1"
    result = br.borrow_book("1", "1")

    assert "Book borrowed successfully" in result


def test_return_book_success():
    bm = BookManager(TEST_BOOKS)
    rm = ReaderManager(TEST_READERS)
    br = BorrowManager(TEST_BORROWS, bm, rm)

    bm.add_book("Python", "Jack", "CNTT", "2024")
    rm.register_reader("Duy", "duy@gmail.com")

    br.borrow_book("1", "1")
    result = br.return_book("1", "1")

    assert "Book returned successfully" in result


def test_borrow_book_not_exist():
    bm = BookManager(TEST_BOOKS)
    rm = ReaderManager(TEST_READERS)
    br = BorrowManager(TEST_BORROWS, bm, rm)

    rm.register_reader("Duy", "a@gmail.com")

    # Try to borrow book "99" (which doesn't exist)
    result = br.borrow_book("1", "99")

    assert "Book not found" in result
