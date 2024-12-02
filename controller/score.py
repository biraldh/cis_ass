from database import Database 
from flask import session
from models.scoreModel import ScoreManager  

class Score(ScoreManager):
    def __init__(self):
        super().__init__()

    def set_score(self, solution):
        username = session.get('username')

        if not username:
            raise Exception("User is not logged in.")
        
        # Check if the answer is correct
        if int(self.current_solution) == int(solution):
            self.score += 1
            self.result = True
            conn = Database.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO scores (username, score, updated_at)
                VALUES (%s, %s, NOW())
                ON CONFLICT (username)
                DO UPDATE SET score = EXCLUDED.score, updated_at = NOW()
            """, (username, self.score))
            conn.commit()
            cursor.close()
            conn.close()
        
        else:
            self.result = False
        
        return self.score, self.result

    def get_score():
        conn = Database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, score FROM scores ORDER BY score DESC LIMIT 10")  # Top 10 leaderboard
        leaderboard = cursor.fetchall()
        conn.close()
        return leaderboard
