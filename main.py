from src.admin import AdminSystem

def menu():
    print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
    print("1. Add Book")
    print("2. View Book List")
    print("3. Register Reader")
    print("4. Borrow Book")
    print("5. Return Book")
    print("6. View Reader's Borrowing History")
    print("0. Exit")
    return input("Enter choice: ").strip()

def run():
    admin = AdminSystem()
    
    while True:
        choice = menu()

        if choice == "1":
            title = input("Book Title: ")
            author = input("Author: ")
            publisher = input("Publisher: ")
            year = input("Publication Year: ")
            result = admin.book_manager.add_book(title, author, publisher, year)
            print(f"✔ Result: {result}")

        elif choice == "2":
            print("\n--- BOOK LIST ---")
            books = admin.book_manager.get_all_books()
            if not books:
                print("No books available.")
            for b in books:
                print(b)

        elif choice == "3":
            name = input("Reader Name: ")
            email = input("Email: ")
            print(admin.reader_manager.register_reader(name, email))

        elif choice == "4":
            reader_id = input("Reader ID: ")
            book_id = input("Book ID: ")
            print(admin.borrow_manager.borrow_book(reader_id, book_id))

        elif choice == "5":
            reader_id = input("Reader ID: ")
            book_id = input("Book ID: ")
            print(admin.borrow_manager.return_book(reader_id, book_id))

        elif choice == "6":
            reader_id = input("Reader ID: ")
            history = admin.reader_manager.view_history(reader_id)
            print("\n--- BORROWING HISTORY ---")
            print(history)

        elif choice == "0":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    run()
