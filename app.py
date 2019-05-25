import os

import pandas as pd
import numpy as np
from decimal import Decimal

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
# Database & Flask Setup
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
cuisines = Base.classes.cuisines
media = Base.classes.media
prices = Base.classes.prices
restaurants = Base.classes.restaurants
reviews = Base.classes.reviews

# Create a session
session = Session(engine)

#################################################
# Functions
#################################################  

def create_dict(r):
    return {
    "restaurant_id" : int(r[0]),
    "restaurant_name": r[1],
    "restaurant_lat": float(r[2]),
    "restaurant_lng": float(r[3]),
    "cuisine_offerings": r[4],
    "main_cuisine_category": r[5],
    "price_range" :  int(r[6]),
    "ave_cost" :  float(r[7]),
    "menu_url" :  r[8],
    "featured_image" :  r[9],
    "nbr_votes" : float(r[10]),
    "restaurant_rating" : float(r[11])
    }

#################################################
# Flask Routes
#################################################  
    
# Renders index page
@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/cuisine_categories")
def cuisine_categories():
    """Return a list of cuisine categories"""
    cuisines_categories = session.query(cuisines.cuisine_categories.distinct()).all()

    # converts a list of list into a single list (flattens list)
    flat_list = [item for sublist in list(cuisines_categories) for item in sublist]

    # return a list of column names (sample names)
    return jsonify(flat_list)


@app.route("/metadata/<int:business_id>", methods=['GET'])
def restaurant_metadata(business_id):
    
    # Step 1: filter by all tables


    # Step 2: Run and store filtered query in results variable  
    results = session.query(*sel).filter(restaurants.restaurant_id == cuisines.restaurant_id).filter(cuisines.restaurant_id == prices.restaurant_id).filter(prices.restaurant_id == media.restaurant_id).filter(media.restaurant_id == reviews.restaurant_id).filter(restaurants.restaurant_id == business_id).one()

    # Step 3: build a dictionary for the restaurant record
    restaurant_info = {
        "restaurant_id" : int(results[0]),
        "restaurant_name": results[1],
        "restaurant_lat": float(results[2]),
        "restaurant_lng": float(results[3]),
        "cuisine_offerings": results[4],
        "main_cuisine_category": results[5],
        "price_range" :  int(results[6]),
        "ave_cost" :  float(results[7]),
        "menu_url" :  results[8],
        "featured_image" :  results[9],
        "nbr_votes" : float(results[10]),
        "restaurant_rating" : float(results[11])
    }

    return jsonify(restaurant_info)

@app.route("/cuisines/<cuisine_categories>", methods=['GET'])
def cuisine_cagetgory_metadata(cuisine_categories):
    # get cuisine category
    # filter all restaurants by category
    # get the first restaurant in this list
    # this one will be used in the init method in js

    # Step 1: set up columns needed for this run
    sel = [restaurants.restaurant_id, restaurants.name, restaurants.lat, restaurants.lng, cuisines.cuisines, cuisines.cuisine_categories, prices.price_range, prices.ave_cost, media.menu_url, media.featured_image, reviews.vote, reviews.rating]

    # Step 2: Run and store filtered query in results variable 
    all_results = session.query(*sel).filter(restaurants.restaurant_id == cuisines.restaurant_id).filter(cuisines.restaurant_id == prices.restaurant_id).filter(prices.restaurant_id == media.restaurant_id).filter(media.restaurant_id == reviews.restaurant_id).filter(cuisines.cuisine_categories == cuisine_categories).all()

    # Step 3: Build a list of dictionary that contains all the restaurants in a given cuisine category
    restaurants_by_cuisine = []

    for r in all_results:
        transformed_dict = create_dict(r)
        restaurants_by_cuisine.append(transformed_dict)

    return jsonify(restaurants_by_cuisine)


if __name__ == "__main__":
    app.run()
