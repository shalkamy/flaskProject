import sqlite3

class UserRepository:
    def __init__(self):
        self.connection = sqlite3.connect("energy.db")
        print(self.connection.total_changes)