from abc import ABC, abstractmethod
from flask import session
from database import Database
import requests

# Abstract class for API fetching
class ApiFetcher(ABC):
    @abstractmethod
    def fetch_question(self):
        pass
