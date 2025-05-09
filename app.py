from utils.auth import login
from roles.base import base_menu

def main():
    print("Welcome to the Real Estate App")
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    user = login(email, password)
    if not user:
        print("Invalid login credentials.")
        return

    base_menu(user)

if __name__ == "__main__":
    main()