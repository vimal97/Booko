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
                        return jsonify(success=True,message="User login successful",userData="{"+"userName:'{}',firstName:'{}',lastName:'{}',phoneNo:'{}',emailId:'{}',password:'{}',interests:'{}'".format(i[0],i[1],i[2],i[3],i[4],i[5],i[6])+"}")
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

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")