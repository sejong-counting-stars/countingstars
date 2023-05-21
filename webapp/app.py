from flask import Flask, render_template, url_for, redirect, request, session, flash
from pymongo import MongoClient # import the pymongo
from bson.objectid import ObjectId #import this to convert ObjectID from string to it's datatype in MongoDB
import functools
import bcrypt # to encrypt password
import os
from os.path import join, dirname, realpath
from werkzeug.utils import secure_filename # for secure name
from datetime import datetime #datetime

client = MongoClient("mongodb://localhost:27017/") # connect on the "localhost" host and port 27017
db = client["webapp"] # use/create "webapp" database

# Create the Flask application
app = Flask(__name__)

# route here
@app.route('/')
def index():
    return render_template("home.html")


# put the following code at the end of 'app.py' script
if __name__ == '__main__':
    app.run(debug=True) #debug is True, default host and port is 127.0.0.1:5000