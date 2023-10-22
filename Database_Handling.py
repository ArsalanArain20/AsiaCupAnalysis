import json
import streamlit as st
import time
class DataBase:
    def __init__(self):
        # Initialize the database with an empty dictionary if the file doesn't exist
        try:
            with open("Database.json", "r") as R:
                self.data = json.load(R)
        except FileNotFoundError:
            self.data = {}

    def insert(self, name, email, password, re_password, favt_player):
        if email in self.data:
            return 0
        else:
            self.data[email] = [name, password, re_password, favt_player]
            with open("Database.json", "w") as W:
                json.dump(self.data, W, indent=4)
            return 1

    def fetch(self, email, password):
        if email in self.data:
            if self.data[email][1] == password:
                return 1
            else:
                print("Inner")
                return 0
        else:
            print("outer")
            return 0


# Calling
obj = DataBase()
#obj.insert("Ali", "@gmail.com", 112, 112, "Smith")

