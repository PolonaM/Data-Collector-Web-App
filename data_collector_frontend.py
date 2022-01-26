"""
This is a PostgreSQL Database Web App made with Flask.
User needs to input height data and an email.
The app saves the data in the postgresql database.
The app then calculates the average height of the inputs in the database
and then sends back to the user the confirmation mail with the calculated average height.
"""

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

# Create Flask app
app = Flask(__name__)

# Specify what database the app connects with
# In pgadmin4 create database 'height_collector' and asign user 'postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres123@localhost/height_collector'

# Create sqlalchemy object for flask app
db = SQLAlchemy(app)

# Use class Model from the sqlalchemy object to define the table
class Data(db.Model):
    """
    This is a blueprint for creating a table in the database
    Use terminal to create an instance of Data class and thus table 'data':
    >>> from data_collector_frontend import db
    >>> db.create_all()
    """
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key = True)
    email_ = db.Column(db.String(120), unique = True) # unique = True - only accept unique values for email
    height_ = db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email_ = email_
        self.height_ = height_ #a single trailing underscore (postfix) is used by convention to avoid naming conflicts with Python keywords. This convention is explained in PEP 8.

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success', methods = ['POST'])
def success():
    if request.method == 'POST':
        email = request.form['email_name']
        height = request.form['height_name']
        if db.session.query(Data).filter(Data.email_ == email).count() == 0:
            data = Data(email, height)
            db.session.add(data)
            db.session.commit()
            average_height = db.session.query(func.avg(Data.height_)).scalar()
            average_height = round(average_height, 1)
            count = db.session.query(Data.height_).count()
            send_email(email, height, average_height, count)
            return render_template('success.html')
    return render_template('index.html', text = 'Seems like we have something from that email already!')


if __name__ == '__main__':
    app.debug = True
    app.run() #default port is 5000; you can also specify the port number
