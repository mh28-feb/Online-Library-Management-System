from src.admin import AdminSystem

def login_screen(admin):
    print("\n--- LOGIN ---")
    u = input("Username: ")
    p = input("Password: ")
    user = admin.auth_manager.login(u, p)
    return user

def main_flow():
    admin = AdminSystem()
    current_user = None

    while not current_user:
        current_user = login_screen(admin)
        if not current_user:
            print("❌ Login failed!")

    print(f"\nWelcome, {current_user['username']} ({current_user['role']})")
    
    # Tiếp tục logic menu dựa trên role (admin/reader) như trước...
    # (Bạn có thể thêm điều kiện if current_user['role'] == 'admin': ...)
