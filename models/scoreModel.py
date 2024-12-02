from abc import ABC, abstractmethod
from flask import session
from database import Database
import requests


# Abstract class for score management
class ScoreManager(ABC):
    def __init__(self):
        self.score = 0
        self.result = False
        self.current_solution = None  

    @abstractmethod
    def set_score(self, solution):
        pass

    @abstractmethod
    def get_score(self):
        pass
