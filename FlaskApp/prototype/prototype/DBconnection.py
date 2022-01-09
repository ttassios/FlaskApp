from flask import Flask
import sqlite3
app = Flask(__name__)

conn = sqlite3.connect('DBergasias.db')
cur = conn.cursor()
print("Succesfully connected to sqlite.")

def create_users_table():
    createUsersTable = '''CREATE TABLE IF NOT EXISTS users (
                            user_id integer primary key autoincrement,
                            username text not null,
                            password text not null);'''
    cur.execute(createUsersTable)
    conn.commit()
    print("Users table created!")
create_users_table()

def create_guests_table():
    createGuestsTable = '''CREATE TABLE IF NOT EXISTS guests (
                                guest_id integer primary key autoincrement,
                                firstname text not null,
                                surname text not null,
                                phonenumber text not null,
                                date text not null,
                                time text not null);'''
    cur.execute(createGuestsTable)
    conn.commit()
    cur.close()
    print("Guests table created!")
create_guests_table()

