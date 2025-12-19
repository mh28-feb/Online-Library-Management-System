from admin import AdminSystem

def test_admin_init():
    admin = AdminSystem()

    assert admin.book_manager is not None
    assert admin.reader_manager is not None
    assert admin.borrow_manager is not None
