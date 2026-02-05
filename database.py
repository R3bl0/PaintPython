import mysql.connector
import random

def connect_to_db():
    connection = mysql.connector.connect(
        host="sql7.freemysqlhosting.net",
        user="sql7711077",
        password="8WB7SQ9zND",
        database="sql7711077"
    )
    return connection

def random_topic():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute('SELECT Topics.Name FROM Topics')
    topics = cursor.fetchall()
    topic = random.choice(topics)[0]
    connection.close()
    return topic

def get_players():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute('SELECT Players.Nick, Players.Points FROM Players')
    players = cursor.fetchall()
    cursor.close()
    return players







