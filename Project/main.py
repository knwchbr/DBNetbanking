from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, reconstructor, backref
from datetime import datetime
import uuid
import requests
import re

app = Flask(__name__)

db = SQLAlchemy(app)

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

if __name__ == '__main__' :
    app.run(debug=True, host='127.0.0.1')
