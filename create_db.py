"""
Small script for the database creation.
"""
from sqlite3 import connect

connection = connect('test_db.sqlite3')
cursor = connection.cursor()

with open('create_db.sql', 'r') as file:
    script = file.read()

cursor.executescript(script)
cursor.close()
connection.close()
