from abc import ABC, abstractmethod

# Abstract class for user management
class UserManagerBase(ABC):
    @abstractmethod
    def register_user(self, username, password):
        pass

    @abstractmethod
    def login_user(self, username, password):
        pass
