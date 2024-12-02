from werkzeug.security import generate_password_hash, check_password_hash
from database import Database  
from models.userModel import UserManagerBase

class UserManager(UserManagerBase):
    def __init__(self):
        self.users = {}

    def register_user(self, username, password):
        conn = Database.get_db_connection()  
        cursor = conn.cursor()

        # Check if the username exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return False, "User already exists."

        # Hash the password and insert the new user
        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()

        cursor.close()
        conn.close()
        return True, "User registered successfully."

    def login_user(self, username, password):
        conn = Database.get_db_connection()  
        cursor = conn.cursor()

        # Fetch the user from the database
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user[2], password):  # user[2] is the hashed password
            cursor.close()
            conn.close()
            return True, "Login successful."
        else:
            cursor.close()
            conn.close()
            return False, "Invalid username or password."
