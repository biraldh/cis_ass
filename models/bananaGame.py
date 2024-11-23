import requests
from database import Database  
from flask import session

class Score:
    # scoring class
    def __init__(self):
        self.score = 0
        self.result = False
        self.current_solution = None  

    def set_score(self, solution):
        username = session.get('username')

        if not username:
            raise Exception("User is not logged in.")
        
        # csheck if the answer is correct
        if int(self.current_solution) == int(solution):
            self.score += 1
            self.result = True
            conn = Database.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO scores (username, score) 
                VALUES (%s, %s) 
                ON CONFLICT (username) 
                DO UPDATE SET score = EXCLUDED.score
            """, (username, self.score))
            conn.commit()
            cursor.close()
            conn.close()
        
        else:
            self.result = False
        
        return self.score, self.result
    
    def get_score(self):
        conn = Database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, score FROM scores ORDER BY score DESC LIMIT 10")  # Top 10 leaderboard
        leaderboard = cursor.fetchall()
        conn.close()
        return leaderboard

class Apicall:
    # call banana API for the question
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_question(self):
        response = requests.get(self.api_url)
        question_data = response.json()
        return question_data["question"], question_data["solution"]

class BananaGame(Score):
    # Main class that controls the game
    def __init__(self, api_url):
        super().__init__()
        self.api_service = Apicall(api_url)
        self.api_url = api_url

    def get_question(self):
        # Fetch question and solution from the Apicall class
        self.current_question_url, self.current_solution = self.api_service.fetch_question()
        return self.current_question_url, self.current_solution

    def submit_solution(self, solution):
        # Check and update score based on the submitted solution
        return self.set_score(solution)
