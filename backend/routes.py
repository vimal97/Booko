from flask import Flask, redirect, url_for, render_template, request, flash
from backend import app

@app.route('/home')
def home():
    print("\n#REQUEST FOR /home\n")
    return render_template("landing_page/landingpage.html")

@app.route('/signup')
def signup():
    print("\n#REQUEST FOR /signup\n")
    return render_template("landing_page/signup.html")

@app.route('/login')
def login():
    print("\n#REQUEST FOR /login\n")
    return render_template("landing_page/login.html")

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")