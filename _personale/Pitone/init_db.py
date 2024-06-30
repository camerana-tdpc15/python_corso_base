import sqlite3

connection = sqlite3.connect('C:\TDPC15-12\python_corso_base\_personale\Pitone\database.db')

with open ('C:\TDPC15-12\python_corso_base\_personale\Pitone\crea_posts.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()