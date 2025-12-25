from src.admin import AdminSystem

def run():
    admin = AdminSystem()
    
    while True:
        print("\n===== LIBRARY =====")
        print("1. Login")
        print("2. Register Reader")
        print("0. Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            u = input("Username: ")
            p = input("Password: ")
            user = admin.login(u, p)
            
            if not user:
                print("❌ Wrong credentials!")
                continue

            role = user.get("role")
            print(f"✔ Welcome {role}")

            # Menu phân quyền như file gốc của bạn
            if role == "admin":
                # admin.register_user(...)
                pass
            elif role == "reader":
                # admin.book_manager.search_book(...)
                pass
                
        elif choice == "2":
            # Logic đăng ký độc giả kết nối ReaderManager và AdminSystem
            name = input("Name: ")
            email = input("Email: ")
            reader = admin.reader_manager.register_reader(name, email)
            
            uname = input("Choose Username: ")
            pwd = input("Choose Password: ")
            print(admin.register_user(uname, pwd, role="reader", reader_id=reader.get("reader_id")))

        elif choice == "0":
            break

if __name__ == "__main__":
    run()
