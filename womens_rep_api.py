from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt

class WomensRepAPI:

    def __init__(self, db_name="olympics"):
        client = MongoClient()
        self.db = client[db_name]
        self.athletes = self.db.athletes
        self.events = self.db.events