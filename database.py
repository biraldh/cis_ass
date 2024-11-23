import psycopg2
from psycopg2 import OperationalError

class Database:
    @staticmethod
    def get_db_connection():
        try:
            # connect to the database
            conn = psycopg2.connect(
                database="banana_game", 
                user="postgres", 
                password="Qwerty", 
                host="localhost", 
                port="5432"
            )
            # Check if the connection was successful
            print("Successfully connected to the database.")
            return conn
        except OperationalError as e:
            print(f"Error: Unable to connect to the database: {e}")
            return None
