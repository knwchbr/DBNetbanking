from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, reconstructor, backref
from datetime import datetime
import uuid
import requests
import re

app = Flask(__name__)
app.secret_key = 'Mac126218'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@127.0.0.1:5432/DBNetbanking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model) :
    __tablename__ = "User"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(Integer)
    password = Column(String)

class CardAccount(db.Model) :
    __tablename__ = "CardAccount"
    id = Column(Integer, primary_key=True)
    FullName = Column(String)
    email = Column(String)
    sex = Column(String)
    phone = Column(Integer)
    Address = Column(String)
    City = Column(String)
    State = Column(String)
    Zip = Column(Integer)
    Identity = Column(Integer)
    id_user = Column(Integer)
    Date = Column(String)

class CardMoney(db.Model) :
    __tablename__ = "CardMoney"
    id = Column(String, primary_key=True)
    Money = Column(Integer)
    CardID = Column(Integer)
    Limit = Column(Integer)
    LimitCount = Column(Integer)
    Date = Column(Integer)

class CardHistory(db.Model) :
    __tablename__ = "CardHistory"
    id = Column(String, primary_key=True)
    Money = Column(Integer)
    Destination = Column(String)
    DateTime = Column(String)
    Action = Column(String)
    CardID = Column(Integer)

@app.route('/')
def index() :
    return render_template('index.html')

@app.route('/about')
def about() :
    return render_template('about.html')

@app.route('/services')
def services() :
    return render_template('services.html')

@app.route('/contact')
def contact() :
    return render_template('contact.html')

@app.route('/profile')
def profile() :
    if 'logged_in' in session :
        return render_template('profile.html')
    else :
        return redirect(url_for("login"))

@app.route('/login', methods=['GET', 'POST'])
def login() :
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form :
        name = request.form['username']
        password = request.form['password']
        user = db.session.query(User).filter_by(name=name).first()
        if user : 
            if name == user.name and password == user.password :
                session['logged_in'] = True
                session['id'] = user.id
                return index()
            else :
                msg = "Incorrect username/password!"
        else :
            msg = "Not have account"
    return render_template('login.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register() :
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        id = len(User.query.all()) + 1
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['tel']
        user = User(id=id, name=username, email=email, password=password, phone=phone)
        Check = db.session.query(User).filter_by(name=username).first()
        if Check is not None :
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not re.match(r'[0-9]+', phone) :
            msg = 'Phone number must only number'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else :
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    elif request.method == 'POST' :
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)
if __name__ == '__main__' :
    app.run(debug=True, host='127.0.0.1')
