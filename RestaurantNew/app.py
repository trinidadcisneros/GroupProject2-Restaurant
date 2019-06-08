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

from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template

import pymysql
pymysql.install_as_MySQLdb()
import flask_sqlalchemy

app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

#################################################
# Database & Flask Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@127.0.0.1/restauranttable"
db = SQLAlchemy(app)

# Create an engine to the restaurants database
engine = create_engine('mysql+pymysql://root:root@127.0.0.1/restauranttable')

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
restaurants = Base.classes.restaurants


# Create a session
session = Session(bind=engine)

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

# Returns a list of all the cuisine categories
@app.route("/cuisine_categories")
def cuisine_categories():
    """Return a list of cuisine categories"""
    cuisines_categories = session.query(restaurants.cuisine_categories.distinct()).all()

    # converts a list of list into a single list (flattens list)
    flat_list = [item for sublist in list(cuisines_categories) for item in sublist]

    # return a list of column names (sample names)
    return jsonify(flat_list)

# ************************************
# RETURNS ONE RESTAURANT BY ID
# ************************************
@app.route("/restaurant_by_id/<int:business_id>", methods=['GET'])
def return_restaurant_by_id(business_id):
    
    # restauranttable column names:
    # restaurant_id, name, lat, lng, cuisines, cuisine_categories, price_range, ave_cost, menu_url, featured_image, vote, rating

    # Step 1: filter by all tables
    sel = [restaurants.restaurant_id, restaurants.name, restaurants.lat, restaurants.lng, restaurants.cuisines, restaurants.cuisine_categories, restaurants.price_range, restaurants.ave_cost, restaurants.menu_url, restaurants.featured_image, restaurants.vote, restaurants.rating]

    # Step 2: Run and store filtered query in results variable  
    result = session.query(*sel).filter(restaurants.restaurant_id == business_id).one()
    print(result)

    # Step 3: build a dictionary for the restaurant record
    restaurant_info = {
        "Id" : int(result[0]),
        "Name": result[1],
        # "restaurant_lat": float(result[2]),
        # "restaurant_lng": float(result[3]),
        "Options": result[4],
        "Category": result[5],
        "Price Range (1 (Low) - 5 (High))" :  int(result[6]),
        "Average Cost ($) " :  float(result[7]),
        # "menu_url" :  result[8],
        # "featured_image" :  result[9],
        "Nbr of Votes" : float(result[10]),
        "Rating (Out of 5) " : float(result[11])
    }
    print(restaurant_info)

    return jsonify(restaurant_info)


# ************************************
# RETURNS ALL RESTAURANT BY CUISINE
# ************************************
@app.route("/restaurants/<cuisine_category>", methods=['GET'])
def return_all_restaurants(cuisine_category):
    # returns a list of restaurants within a given cuisine category

    # Step 1: set up columns needed for this run
    sel = [restaurants.restaurant_id, restaurants.name, restaurants.lat, restaurants.lng, restaurants.cuisines, restaurants.cuisine_categories, restaurants.price_range, restaurants.ave_cost, restaurants.menu_url, restaurants.featured_image, restaurants.vote, restaurants.rating]

    # Step 2: Run and store filtered query in results variable 
    all_results = session.query(*sel).filter(restaurants.cuisine_categories == cuisine_category).all()

    # Step 3: Build a list of dictionary that contains all the restaurants in a given cuisine category
    restaurants_by_cuisine = []

    for r in all_results:
        transformed_dict = create_dict(r)
        restaurants_by_cuisine.append(transformed_dict)
    
    print(restaurants_by_cuisine)

    return jsonify(restaurants_by_cuisine)


# ************************************
# RETURNS ALL RESTAURANT DATA
# ************************************
@app.route("/restaurants", methods=['GET'])
def return_all_restaurants_data():

    # Step 1: set up columns needed for this run
    sel = [restaurants.restaurant_id, restaurants.name, restaurants.lat, restaurants.lng, restaurants.cuisines, restaurants.cuisine_categories, restaurants.price_range, restaurants.ave_cost, restaurants.menu_url, restaurants.featured_image, restaurants.vote, restaurants.rating]

    # Step 2: Run and store filtered query in results variable 
    all_results = session.query(*sel).all()

    # Step 3: Build a list of dictionary that contains all the restaurants in a given cuisine category
    all_restaurants = []

    for r in all_results:
        transformed_dict = create_dict(r)
        all_restaurants.append(transformed_dict)
    
    print(all_restaurants)

    return jsonify(all_restaurants)


if __name__ == "__main__":
    app.run()
