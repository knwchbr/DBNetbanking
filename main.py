from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, reconstructor, backref
from datetime import datetime
import uuid
import requests
import re
import random

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
    First_Name = Column(String)
    Last_Name = Column(String)
    Gender = Column(String)
    Date = Column(String)
    Email = Column(String)
    Phone = Column(Integer)
    Address = Column(String)
    City = Column(String)
    State = Column(String)
    Zipcode = Column(Integer)
    Identity = Column(Integer)
    Cardtype = Column(String)
    id_user = Column(Integer)
    

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
        Card = db.session.query(CardAccount).filter_by(id_user=session['id']).first()
        if Card :
            return render_template('profile.html')
        else :
            return redirect(url_for('profile1'))
    else :
        return redirect(url_for("login"))

@app.route('/profile1')
def profile1() :
    return render_template('profile1.html')

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

@app.route('/registercard', methods=['GET', 'POST'])
def registercard() :
    if request.method == 'POST' and 'fname' in request.form and 'lname' in request.form and 'gender' in request.form and 'date of birth' in request.form and 'email' in request.form and 'contact' in request.form and 'address' in request.form and 'city' in request.form and 'state' in request.form and 'zipcode' in request.form and 'Identity' in request.form and 'typecard' in request.form :
        fname = request.form['fname']
        lname = request.form['lname']
        gender = request.form['gender']
        date = request.form['date of birth']
        email = request.form['email']
        phone = request.form['contact']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']
        Identity = request.form['Identity']
        typecard = request.form['typecard']
    elif request.method == "POST" :
        print('1')
        
    return render_template('registercard.html')

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

@app.route('/logout')
def logout() :
    session.pop('logged_in', None)
    session.pop('id', None)
    session.pop('name', None)
    return redirect(url_for('index'))

if __name__ == '__main__' :
    app.run(debug=True, host='127.0.0.1')
