#!/usr/bin/env python

from backend import app

import sqlite3


conn = sqlite3.connect('booko.db')
print("Opened database successfully")
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
if(('users',) in tables):
    print("Users table already present")
else:
    try:
        conn.execute('CREATE TABLE users (username TEXT, firstname TEXT, lastname TEXT, phoneno TEXT, emailid TEXT, password TEXT, country TEXT, interests TEXT, requested TEXT, approved TEXT, rejected TEXT, blocked TEXT)')
        conn.commit()
        print("Created table for users")
    except Exception as e:
        print("Failed to create tables due to : {}".format(e))
if(('books',) in tables):
    print("Books table already present")
else:
    try:
        conn.execute('CREATE TABLE books (name TEXT, author TEXT, genre TEXT, description TEXT, imagepath TEXT, owner TEXT, requests TEXT)')
        conn.commit()
        print("Created table for books")
    except Exception as e:
        print("Failed to create books due to : {}".format(e))
conn.close()