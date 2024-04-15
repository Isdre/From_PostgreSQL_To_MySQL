#import data from postgresql database

import psycopg2
import mysql.connector
import json


class PostgreSQLConnection:
    def __init__(self,json_filename : str) -> None:
        with open(json_filename, "r") as access_data_file:
            self.access_data = json.loads(access_data_file.read())
        self.actualDatabase = self.access_data["database"]
        self.connection = psycopg2.connect(database=self.actualDatabase,user=self.access_data["user"],password=self.access_data["password"],host=self.access_data["host"],port=self.access_data["port"])
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

class MySQLConnection:
    def __init__(self,json_filename : str) -> None:
        with open(json_filename, "r") as access_data_file:
            self.access_data = json.loads(access_data_file.read())
        self.actualDatabase = self.access_data["database"]
        self.connection = mysql.connector.connect(database=self.actualDatabase,user=self.access_data["user"],password=self.access_data["password"],host=self.access_data["host"],port=self.access_data["port"])
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()