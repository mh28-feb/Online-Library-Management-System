import pytest
from reader import ReaderManager


def test_register_and_history(tmp_path):
    data_file = tmp_path / "readers.json"
    rm = ReaderManager(path=data_file)
    assert rm.register_reader("R1", "A", "a@b.com")
    assert not rm.register_reader("R1", "A", "a@b.com")  # duplicate id
    assert not rm.register_reader("R2", "B", "invalid-email")
    r = rm.get_reader_by_id("R1")
    assert r is not None
    rm.add_to_history("R1", {"note": "test"})
    h = rm.view_history("R1")
    assert any("note" in e for e in h)
