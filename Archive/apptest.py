import os

import pandas as pd
import numpy as np

# Dependencies for API call
import requests
import json

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#################################################
# Database Setup & Flask Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@127.0.0.1/RestaurantData"
db = SQLAlchemy(app)

# Create an engine to the restaurants database
engine = create_engine('mysql+pymysql://root:root@127.0.0.1/restaurantdata')

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
cuisine = Base.classes.cuisines
location = Base.classes.location
media = Base.classes.media
price = Base.classes.price
restaurants = Base.classes.restaurants
reviews = Base.classes.reviews

# Create a session
session = Session(engine)


#################################################
# Flask Routes
#################################################  
    
# Renders index page
@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/restaurants")
def resturant_names():
    """Return restaurant json."""
    restaurant_names = session.query(restaurants.name).all()
    names = list(np.ravel(restaurant_names))
    return jsonify(names)


@app.route("/cuisine_categories")
def cuisine_categories():
    """Return a list of cuisine categories"""
    cuisines_categories = session.query(restaurants.cuisine_category.distinct()).all()

    # turns a list of list into a single list
    flat_list = [item for sublist in list(cuisines_categories) for item in sublist]

    # return a list of column names (sample names)
    return jsonify(flat_list)

@app.route("/location")
def location():
    """Return location json."""
    lat = session.query(location.lat).all()
    latitude = list(np.ravel(lat))
    return jsonify(latitude)


if __name__ == "__main__":
    app.run()
