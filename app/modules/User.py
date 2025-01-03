import pandas as pd
from modules.Commander import getUserName
from modules.DataFetcher import DataFetcher

class User:
    def __init__(self, username, password):
        self.username = getUserName(username)
        self.password = password
        self.dataFetcher = DataFetcher(self)


    def __repr__(self):
        return self.username
    

    def to_dict(self):
        return {"username": self.username, "password": self.password}


    @classmethod
    def from_dict(cls, data):
        return cls(data["username"], data["password"])
    

    @staticmethod
    def getLoggedUser(usr):
        return User.from_dict(usr)


