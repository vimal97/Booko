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
        if(get_user("username",signupData['emailId']) != False):
            return jsonify(success=False,message="Username is already taken. Please try again with another username.",warn=True)
        try:
            with sql.connect("booko.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (username, firstname, lastname, phoneno, emailid, password, country, interests, requested, approved, rejected) VALUES (?,?,?,?,?,?,?,?,?,?,?)",(signupData['userName'],signupData['firstName'],signupData['lastName'],signupData['phoneNo'],signupData['emailId'],signupData['password'],signupData['country'],signupData['interests'],signupData['requested'],'[]','[]'))
                con.commit()
                print(" -> User resistration successful\n")
                return jsonify(success=True,message="User registered successfully",userData=json.dumps(signupData))
        except Exception as e:
            print(" -> User resistration failed due to {}\n".format(e))
            return jsonify(success=False,message="User registration failed. Check again later.",warn=False)

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
            if(loginData['emailId'] ==  'admin@booko' and loginData['password'] == 'admin@123'):
                return jsonify(success=True,message="User login successful",userName="Admin", admin=True)
            else:
                with sql.connect("booko.db") as con:
                    cur = con.cursor()
                    cur.execute("select * from users")
                    rows = cur.fetchall(); 
                    for i in rows:
                        if(i[4] == loginData['emailId'] and i[5] == loginData['password']):
                            print(" -> User login successful\n")
                            return jsonify(success=True,message="User login successful",userName=i[0],firstName=i[1],lastName=i[2],phoneNo=i[3],emailId=i[4],country=i[6],interests=i[7],requested=i[8],approved=i[9],rejected=i[10])
                    print(" -> User not found\n")
                    return jsonify(success=False,message="User not found",warn=False)
        except Exception as e:
            print(" -> User login failed due to {}\n".format(e))
            return jsonify(success=False,message="User login failed. Check again later.",warn=False)

@app.route('/dashboard')
@cross_origin()
def dashboard():
    print("\n#REQUEST FOR /dashboard\n")
    return render_template("dashboard.html")

@app.route('/profile', methods = ['POST', 'GET'])
@cross_origin()
def profile():
    if(request.method == 'GET'):
        print("\n#GET REQUEST FOR /profile\n")
        return render_template("profile.html")
    else:
        print("\n#POST REQUEST FOR /profile\n")
        profileData = json.loads(list(request.form)[0])
        print("--> Received data : {}".format(profileData))
        try:
            with sql.connect("booko.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE users SET firstname='{}', lastname='{}', emailid='{}', country='{}', phoneno='{}', interests='{}' WHERE username='{}'".format(profileData['firstName'],profileData['lastName'],str(profileData['emailId']),profileData['country'],profileData['phoneNo'],profileData['interests'],profileData['userName']))
                con.commit()
                print(" -> User profile updated\n")
                return jsonify(success=True,message="User profile updated",userData=json.dumps(profileData))
        except Exception as e:
            print(" -> User profile updation failed due to {}\n".format(e))
            return jsonify(success=False,message="User profile updation failed")

@app.route('/sell-books', methods = ['POST', 'GET'])
@cross_origin()
def sellBooks():
    if(request.method == 'GET'):
        print("\n#GET REQUEST FOR /sell-books\n")
        return render_template("sell-books.html")
    else:
        print("\n#POST REQUEST FOR /sell-books\n")
        bookData = json.loads(list(request.form)[0])
        print("--> Received data : {}".format(bookData))
        try:
            if(not find_book(bookData)):
                with sql.connect("booko.db") as con:
                    cur = con.cursor()
                    imagePath = "" #image path to be generated
                    cur.execute("INSERT INTO books (name, author, genre, description, imagepath, owner, requests) VALUES (?,?,?,?,?,?,?)",(bookData['name'],bookData['author'],bookData['genre'],bookData['description'],imagePath,bookData['owner'],"[]"))
                    con.commit()
                    print(" -> Book added successfully\n")
                    return jsonify(success=True,message="Book added successfully")
            else:
                return jsonify(success=False,message="This book is already registered.", warn=True)        
        except Exception as e:
            print(" -> Book registration failed due to {}\n".format(e))
            return jsonify(success=False,message="Book registration failed", warn=False)

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

@app.route('/all-books', methods = ['POST'])
@cross_origin()
def get_all_books():
    print("\n#REQUEST FOR /all-books\n")
    req = json.loads(list(request.form)[0])
    count = 0
    booksList = []
    if(req['type'] == "owned"):
        with sql.connect("booko.db") as con:
            cur = con.cursor()
            cur.execute("select * from books where owner='{}'".format(req['email']))
            rows = cur.fetchall()
        for i in rows:
            count = count + 1
            booksList.append([count, i[0], i[2], i[1], i[3]])
        return jsonify(success=True,books=booksList)
    elif(req['type'] == 'categories'):
        print(" --> Request received : {}".format(req))
        if(req['genre'] == "all"):
            with sql.connect("booko.db") as con:
                cur = con.cursor()
                cur.execute("select * from books")
                rows = cur.fetchall()
            print("Entire book list : {}".format(rows))
            for i in rows:
                count = count + 1
                username = get_user("username", i[5])
                booksList.append([count, i[0], i[2], i[1], username, i[3]])
            return jsonify(success=True,books=booksList)
        else:
            with sql.connect("booko.db") as con:
                cur = con.cursor()
                cur.execute("select * from books where genre='{}'".format(req['genre']))
                rows = cur.fetchall()
            for i in rows:
                count = count + 1
                username = get_user("username", i[5])
                booksList.append([count, i[0], i[2], i[1], username, i[3]])
            return jsonify(success=True,books=booksList)
    elif(req['type'] == "requested"):
        return "Success"
    return jsonify(success=False,message="Failed to fetch book of type {}".format(req['type']))

@app.route('/admin')
@cross_origin()
def admin():
    print("\n#REQUEST FOR /admin\n")
    return render_template("admin.html")

@app.route('/request-book', methods = ['POST'])
@cross_origin()
def request_book():
    print("\n#REQUEST FOR /request-book\n")
    requestData = json.loads(list(request.form)[0])
    try:
        with sql.connect("booko.db") as con:
            cur = con.cursor()
            cur.execute("select * from books")
            newRequests = []
            rows = cur.fetchall()
            cur.execute("select * from users")
            users = cur.fetchall()
            temp = []
            for i in rows:
                if(i[0] == requestData['name'] and i[5] == get_user("email", requestData['owner'])):
                    print(" --> Modifying the request array.")
                    newRequests = json.loads(i[6])
                    if(requestData['requested'] in newRequests):
                        return jsonify(success=False, message="You have already requested the same book. Check the 'Notifications' tab for updates.", warn=True)
                    newRequests.append(requestData['requested'])
            emailId = get_user("email", requestData['owner'])
            cur.execute("UPDATE books SET requests='{}' WHERE name='{}' AND owner='{}'".format(json.dumps(newRequests),requestData['name'],emailId))
            
            # print new books data
            print(" --> Updated book data : "),
            cur.execute("select * from books")
            rows = cur.fetchall()
            for i in rows:
                if(i[0] == requestData['name'] and i[5] == get_user("email",requestData['owner'])):
                    print(i)

            cur.execute("select * from users")
            newRequested = []
            rows = cur.fetchall()
            for i in rows:
                if(i[4] == get_user("email",requestData['requested'])):
                    newRequested = json.loads(i[8])
            print("Already present data : {}".format(newRequested))
            newRequested.append([requestData['name'], requestData['owner']])
            print("Updated present data : {}".format(newRequested))
            cur.execute("UPDATE users SET requested='{}' WHERE emailid='{}'".format(json.dumps(newRequested),get_user("email",requestData['requested'])))
            con.commit()
            return jsonify(success=True, message="Request sent successfully. Check the Notifications tab for updates. :)")
    except Exception as e:
        print(" -> Request addition failed due to {}\n".format(e))
        return jsonify(success=False, message="Request sent failed :(. its on us dont worry !")

@app.route('/respond-requests', methods = ['POST'])
@cross_origin()
def respond_requests():
    print("\n#POST REQUEST FOR /respond-requests\n")
    requestData = json.loads(list(request.form)[0])
    print("Data received : ",requestData)
    try:
        with sql.connect("booko.db") as con:
            if(requestData['approve'] == True):
                print(" --> Approval request")
                # Remove requestee from booksData
                cur = con.cursor()
                cur.execute("select * from books where owner='{}' AND name='{}'".format(requestData['owner'],requestData['name']))
                rows = cur.fetchall()
                requestorArray = json.loads(rows[0][6])
                requestorArray.remove(requestData['requestee'])
                cur.execute("update books SET requests='{}' where owner='{}' AND name='{}'".format(json.dumps(requestorArray), requestData['owner'], requestData['name']))
                # add book to users approved list
                cur.execute("select * from users where emailid='{}'".format(get_user("email",requestData['requestee'])))
                rows = cur.fetchall()
                requestedArray = json.loads(rows[0][8])
                approvedArray = json.loads(rows[0][9])
                indx = 0
                print(" # DEBUG Requested array : {}".format(requestedArray))
                for i in requestedArray:
                    if(i[0] == requestData['name'] and i[1] == requestData['owner']):
                        indx = requestedArray.index(i)
                requestedArray.pop(indx)
                approvedArray.append([requestData['name'], get_user("username", requestData['owner']), requestData['owner'], get_user("phoneno", requestData['owner'])])
                cur.execute("update users SET requested='{}',approved='{}' where emailid='{}'".format(json.dumps(requestedArray), json.dumps(approvedArray), get_user("email",requestData['requestee'])))
                # print_users()
                # print_books()
            else:
                print(" --> Reject request")
                cur = con.cursor()
                # Remove requestee from booksData
                cur.execute("select * from books where owner='{}' AND name='{}'".format(requestData['owner'],requestData['name']))
                rows = cur.fetchall()
                requestorArray = json.loads(rows[0][6])
                print(" # DEBUG Book requested array : {}".format(requestorArray))
                requestorArray.remove(requestData['requestee'])
                cur.execute("update books SET requests='{}' where owner='{}' AND name='{}'".format(json.dumps(requestorArray), requestData['owner'], requestData['name']))
                # add book to users reject list
                cur.execute("select * from users where emailid='{}'".format(get_user("email",requestData['requestee'])))
                rows = cur.fetchall()
                requestedArray = json.loads(rows[0][8])
                rejectedArray = json.loads(rows[0][10])
                indx = 0
                print(" # DEBUG Requested array of requestee before rejection: {} and rejected array {}".format(requestedArray, rejectedArray))
                for i in requestedArray:
                    if(i[0] == requestData['name'] and i[1] == requestData['owner']):
                        indx = requestedArray.index(i)
                requestedArray.pop(indx)
                print(" # DEBUG Requested array of requestee after rejection: {} and rejected array {}".format(requestedArray, rejectedArray))
                rejectedArray.append([requestData['name'], get_user("username",requestData['owner'])])
                cur.execute("update users SET requested='{}',rejected='{}' where emailid='{}'".format(json.dumps(requestedArray), json.dumps(rejectedArray), get_user("email",requestData['requestee'])))
                # print_users()
                # print_books()
            return jsonify(success=True)
    except Exception as e:
        print(" -> Fetching request failed due to {}\n".format(e))
        return jsonify(success=False, message="Fetching request failed")

@app.route('/get-requests', methods = ['POST'])
@cross_origin()
def get_requests():
    print("\n#POST REQUEST FOR /get-requests\n")
    userData = json.loads(list(request.form)[0])
    finalRequest = []
    if(userData['type'] == "requests"):
        try:
            with sql.connect("booko.db") as con:
                cur = con.cursor()
                cur.execute("select * from books where owner='{}'".format(userData['email']))
                rows = cur.fetchall()
                for i in rows:
                    if(i[6] != "[]"):
                        requests = json.loads(i[6])
                        finalRequest.append([i[0], json.loads(i[6])])
                return jsonify(success=True,requests=json.dumps(finalRequest))
        except Exception as e:
            print(" -> Fetching request array failed due to {}\n".format(e))
            return jsonify(success=False, message="Fetching request failed")
    elif(userData['type'] == "requested"):
        finalRequest = dict()
        try:
            with sql.connect("booko.db") as con:
                cur = con.cursor()
                cur.execute("select approved,rejected from users where emailid='{}'".format(userData['email']))
                rows = cur.fetchall()
                finalRequest['approved'] = rows[0][0]
                finalRequest['rejected'] = rows[0][1]
                return jsonify(success=True,requests=json.dumps(finalRequest))
        except Exception as e:
            print(" -> Fetching requested array failed due to {}\n".format(e))
            return jsonify(success=False, message="Fetching request failed")

def find_book(bookData):
    try:
        print("\n#Find book\n")
        with sql.connect("booko.db") as con:
            cur = con.cursor()
            cur.execute("select * from books")
            rows = cur.fetchall(); 
            for i in rows:
                if(i[0] == bookData['name'] and i[5] == bookData['owner']):
                    return True
            print(" -> Book not found\n")
            return False
    except Exception as e:
        print(" -> Book search failed due to {}\n".format(e))
        return False

def get_user(option1, option2):
    try:
        print("\n#Get user data\n")
        with sql.connect("booko.db") as con:
            cur = con.cursor()
            cur.execute("select * from users")
            rows = cur.fetchall()
            if(option1 == "email"):
                for i in rows:
                    if(i[0] == option2):
                        print(" -> User found\n")
                        return i[4]
            elif(option1 == "username"):
                for i in rows:
                    if(i[4] == option2):
                        print(" -> User found\n")
                        return i[0]
            elif(option1 == "phoneno"):
                for i in rows:
                    if(i[4] == option2):
                        print(" -> User found\n")
                        return i[3]
            print(" -> User not found\n")
            return False
    except Exception as e:
        print(" -> User search failed due to {}\n".format(e))
        return False

@app.route('/see-users')
@cross_origin()
def print_users():
    try:
        print("\n---------- Users Table-------------")
        with sql.connect("booko.db") as con:
            cur = con.cursor()
            cur.execute("select * from users")
            rows = cur.fetchall(); 
            for i in rows:
                print(i)
        print("---------- End of Users Table------\n")
        return jsonify(data=rows)
    except Exception as e:
        print(" -> Getting users table failed due to {}\n".format(e))
        return 

@app.route('/see-books')
@cross_origin()  
def print_books():
    try:
        print("\n---------- Books Table-------------")
        with sql.connect("booko.db") as con:
            cur = con.cursor()
            cur.execute("select * from books")
            rows = cur.fetchall(); 
            for i in rows:
                print(i)
        print("---------- End of Books Table------\n")
        return jsonify(data=rows)
    except Exception as e:
        print(" -> Getting books table failed due to {}\n".format(e))
        return

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")