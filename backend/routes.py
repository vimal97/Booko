#!/usr/bin/env python

from flask import Flask, redirect, url_for, render_template, request, flash, jsonify
import json
from backend import app
import sqlite3 as sql
from flask_cors import CORS, cross_origin


@app.route('/home')
@cross_origin()
def home():
    print("\n#REQUEST FOR /home\n")
    return render_template("landing_page/landingpage.html")

@app.route('/signup', methods = ['POST', 'GET'])
@cross_origin()
def signup():
    if(request.method == 'GET'):
        print("\n# GET REQUEST FOR /signup\n")
        return render_template("landing_page/signup.html")
    else:
        print("\n# POST REQUEST FOR /signup")
        signupData = json.loads(list(request.form)[0])
        try:
            with sql.connect("booko.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (username, firstname, lastname, phoneno, emailid, password, interests) VALUES (?,?,?,?,?,?,?)",(signupData['userName'],signupData['firstName'],signupData['lastName'],signupData['phoneNo'],signupData['emailId'],signupData['password'],signupData['interests']))
                con.commit()
                print(" -> User resistration successful\n")
                return jsonify(success=True,message="User registered successfully",userData=json.dumps(signupData))
        except Exception as e:
            print(" -> User resistration failed due to {}\n".format(e))
            return jsonify(success=False,message="User registration failed")

@app.route('/login', methods = ['POST', 'GET'])
@cross_origin()
def login():
    if(request.method == 'GET'):
        print("\n# GET REQUEST FOR /login\n")
        return render_template("landing_page/login.html")
    else:
        print("\n# POST REQUEST FOR /login")
        loginData = json.loads(list(request.form)[0])
        try:
            with sql.connect("booko.db") as con:
                cur = con.cursor()
                cur.execute("select * from users")
                rows = cur.fetchall(); 
                for i in rows:
                    if(i[4] == loginData['emailId'] and i[5] == loginData['password']):
                        print(" -> User login successful\n")
                        return jsonify(success=True,message="User login successful",userName=i[0],firstName=i[1],lastName=i[2],phoneNo=i[3],emailId=i[4],password=i[5],interests=i[6])
                print(" -> User not found\n")
                return jsonify(success=False,message="User not found")
        except Exception as e:
            print(" -> User login failed due to {}\n".format(e))
            return jsonify(success=False,message="User login failed")

@app.route('/dashboard')
@cross_origin()
def dashboard():
    print("\n#REQUEST FOR /dashboard\n")
    return render_template("dashboard.html")

@app.route('/profile')
@cross_origin()
def profile():
    print("\n#REQUEST FOR /profile\n")
    return render_template("profile.html")

@app.route('/sell-books')
@cross_origin()
def sellBooks():
    print("\n#REQUEST FOR /sell-books\n")
    return render_template("sell-books.html")

@app.route('/my-books')
@cross_origin()
def myBooks():
    print("\n#REQUEST FOR /my-books\n")
    return render_template("my-books.html")

@app.route('/categories')
@cross_origin()
def categories():
    print("\n#REQUEST FOR /categories\n")
    return render_template("categories.html")

@app.route('/notifications')
@cross_origin()
def notifications():
    print("\n#REQUEST FOR /notifications\n")
    return render_template("notifications.html")

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")