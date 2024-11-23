from werkzeug.security import generate_password_hash, check_password_hash
from database import Database  

class UserManager:
    def __init__(self):
        self.users = {}

    def register_user(self, username, password):
        conn = Database.get_db_connection()  
        cursor = conn.cursor()

        # check if the username exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return False, "User already exists."

        # hash the password and insert the new user
        hashed_password = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()

        cursor.close()
        conn.close()
        return True, "User registered successfully."

    def login_user(self, username, password):
        conn = Database.get_db_connection()  
        cursor = conn.cursor()
        print(username)
        print(password)
        # fetch the user from the database
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        print(user[1])
        if user and check_password_hash(user[2], password): 
            cursor.close()
            conn.close()
            return True, "Login successful."
        else:
            return False, "Invalid username or password."
        cursor.close()
        conn.close()
        
