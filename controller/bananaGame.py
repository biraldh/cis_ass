import requests
from database import Database  
from flask import session
from controller.score import Score
from models.questionModel import ApiFetcher  

class Apicall(ApiFetcher):
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_question(self):
        response = requests.get(self.api_url)
        question_data = response.json()
        return question_data["question"], question_data["solution"]


class BananaGame(Score, Apicall):
    def __init__(self, api_url):
        # Initialize both Score and Apicall classes
        Score.__init__(self)
        Apicall.__init__(self, api_url)

    def get_question(self):
        # Fetch question and solution from the Apicall class
        self.current_question_url, self.current_solution = self.fetch_question()
        return self.current_question_url, self.current_solution

    def submit_solution(self, solution):
        # Check and update score based on the submitted solution
        return self.set_score(solution)