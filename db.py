import sqlite3
import json


connection = sqlite3.connect('database.db')
cursor = connection.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR,
    photo VARCHAR,
    username VARCHAR,
    telegram_id BIGINT NOT NULL
)
''')

connection.commit()

def add_user(first_name, last_name, telegram_id, photo, username):
    sql = "INSERT INTO users (first_name, last_name, telegram_id, photo, username) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(sql, (first_name, last_name, telegram_id, photo, username))
    connection.commit()


def select_user(telegram_id):
    sql = "SELECT * FROM Users WHERE telegram_id=?"
    return cursor.execute(sql, (telegram_id,)).fetchone()

def select_user_by_id(id):
    sql = "SELECT * FROM Users WHERE id=?"
    return cursor.execute(sql, (id,)).fetchone()

def select_all_users():
    sql = "SELECT * FROM Users"
    return cursor.execute(sql).fetchall()

