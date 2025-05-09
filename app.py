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

    role = user['role']
    print(f"Logged in as {role.capitalize()}")

    if role == "admin":
        admin.menu(user['userid'])
    elif role == "agent":
        agent.menu(user['userid'])
    elif role == "client":
        client.menu(user['userid'])

if __name__ == "__main__":
    main()