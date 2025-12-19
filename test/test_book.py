import os
import json
from book import BookManager

TEST_FILE = "data/test_books.json"

def setup_function():
    # Reset test file
    if not os.path.exists("data"):
        os.makedirs("data")
        
    with open(TEST_FILE, "w", encoding="utf-8") as f:
        f.write("[]")


def test_add_book():
    bm = BookManager(TEST_FILE)
    result = bm.add_book("Python", "Jack", "CNTT", "2024")

    assert "Book added successfully" in result

    data = bm.get_all_books()
    assert len(data) == 1
    assert data[0]["title"] == "Python"


def test_get_all_books():
    bm = BookManager(TEST_FILE)
    bm.add_book("A", "B", "C", "2000")
    bm.add_book("X", "Y", "Z", "2001")

    data = bm.get_all_books()

    assert len(data) == 2
    assert data[1]["author"] == "Y"
