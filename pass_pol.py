
import re
import sqlite3

class PasswordPolicyEnforcement:
    def __init__(self, db_name='Login_users.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def is_strong_password(self, password):

        Min_Len = 8
        Cont_Capt = re.search(r'[A-Z]', password)
        Cont_Lowe = re.search(r'[a-z]', password)
        Cont_Num = re.search(r'\d', password)
        Cont_Spec_Sign = re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\-]', password)

        if (len(password) < Min_Len or
            not Cont_Capt or
            not Cont_Lowe or
            not Cont_Num or
            not Cont_Spec_Sign):
            return False

        return True

    def register_user(self, username, password):
        try:
            self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            return "You're registered successfully."
        except sqlite3.IntegrityError:
            return "Username already exists. Please choose another one."

    def change_password(self, username, old_password, new_password):
        pass

    def login(self, username, password):
        self.cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        result = self.cursor.fetchone()

        if result is None:
            return "Login failed. Please check your username and password or you're not registered."

        stored_password = result[0]
        if stored_password == password:
            return "Login successful."
        else:
            return "Login failed. Please check your username and password or you're not registered."

    def close_database(self):
        self.conn.close()


password_policy = PasswordPolicyEnforcement()
print("Welcome to the Password Management System")

while True:
    print("\nMenu:")
    print("1. Register a new user")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        result = password_policy.register_user(username, password)
        print(result)
    elif choice == "2":
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        result = password_policy.login(username, password)
        print(result)
    elif choice == "3":
        password_policy.close_database()
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")
