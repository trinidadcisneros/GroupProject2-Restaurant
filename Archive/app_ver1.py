import os

import pandas as pd
import numpy as np

# Dependencies for API call
import requests
import json

import mysql.connector as mysql

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################



app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@127.0.0.1/RestaurantData"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
Samples_Metadata = Base.classes.sample_metadata
Samples = Base.classes.samples

# Restaurant API End Access
url = "https://developers.zomato.com/api/v2.1/search?entity_id=281&entity_type=city&start=1&count=100"
headers = {'user-key': "56f8a64be7b09ee8c81a59edfd692b34", "accept": "application/json"}

# Cuisine API End Point
c_url = "https://developers.zomato.com/api/v2.1/cuisines?city_id=281&entity_type=city&start=1&count=100"
c_headers = {'user-key': "56f8a64be7b09ee8c81a59edfd692b34", "accept": "application/json"}

def api_tojson_todict(a, b):
    response = requests.get(a, b).json()
    with open('restaurant_test.json', 'w') as json_file:
        json.dump(response, json_file)
    with open('restaurant_test.json', 'r') as JSON:
        json_dict = json.load(JSON)
    return json_dict

def create_dict(r):
    return {
    "name": r["restaurant"]["name"],
    "res_id": r["restaurant"]["R"]["res_id"],
    "ave_cost": r["restaurant"]["average_cost_for_two"],
    "cuisines": r["restaurant"]["cuisines"],
    "price_range": r["restaurant"]["price_range"],
    "featured_image": r["restaurant"]["featured_image"],
    "menu": r["restaurant"]["menu_url"],
    "lat": r["restaurant"]["location"]["latitude"],
    "lng": r["restaurant"]["location"]["longitude"],
    "rating": r["restaurant"]["user_rating"]["aggregate_rating"],
    "vote": r["restaurant"]["user_rating"]["votes"]
    }

def create_cuisine(r):
    return {
    "cuisine_id": r["cuisine"]["cuisine_id"],
    "cuisine_category": r["cuisine"]["cuisine_name"],
    }

# Adds the cuisine category to each restaurant
def addcategory(r):
    for i in r: 
        value = i["cuisines"]
        split_value = value.split()
        first_value = split_value[0]
        formated_value = first_value.replace(',', '')
        i["cuisine_category"] = formated_value
    return r

#################################################
# Create Table
#################################################
db = mysql.connect( host = "127.0.0.1", user = "root", passwd = "root")

def createTables():
cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS restaurantdata")
cursor.execute("USE restaurantdata")

#     Create Cuisine Table
    cursor.execute("DROP TABLE IF EXISTS cuisines")
    cursor.execute("CREATE TABLE IF NOT EXISTS cuisines (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, cuisine_id INT(11), cuisine_category VARCHAR(255),UNIQUE KEY `cuisine_id` (`cuisine_id`))ENGINE=InnoDB")
    cursor.execute("DESC cuisines")
    
#     Create Restaurant Table
    cursor.execute("DROP TABLE IF EXISTS restaurants")
    cursor.execute("CREATE TABLE IF NOT EXISTS restaurants (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, res_id INT(20), `name` VARCHAR(255), cuisines VARCHAR(255), cuisine_category VARCHAR(255), UNIQUE KEY `restaurants` (`res_id`)) ENGINE=InnoDB")
    cursor.execute("DESC restaurants")
    
    # Create location table
    cursor.execute("DROP TABLE IF EXISTS location")
    cursor.execute("CREATE TABLE IF NOT EXISTS location (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, `name` VARCHAR(255), lat DECIMAL(6,3), lng DECIMAL (6,3)) ENGINE=InnoDB")
    cursor.execute("DESC location")

    # Create price table
    cursor.execute("DROP TABLE IF EXISTS price")
    cursor.execute("CREATE TABLE IF NOT EXISTS price (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, `name` VARCHAR(255), price_range INT(2), ave_cost DECIMAL(6,2)) ENGINE=InnoDB")
    cursor.execute("DESC price")
    
    # Create media table
    cursor.execute("DROP TABLE IF EXISTS media")
    cursor.execute("CREATE TABLE IF NOT EXISTS media (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, `name` VARCHAR(255), menu VARCHAR(255), featured_image VARCHAR(255)) ENGINE=InnoDB")
    cursor.execute("DESC media")
    
    
    # Create reviews table
    cursor.execute("DROP TABLE IF EXISTS reviews")
    cursor.execute("CREATE TABLE IF NOT EXISTS reviews (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, `name` VARCHAR(255), vote DECIMAL(6,2), rating DECIMAL(6,2)) ENGINE=InnoDB")
    cursor.execute("DESC reviews")
    
#################################################
# Load Table
#################################################
def load_tables():
    
#     Load restaurant data
    restaurant_values = []
    def r_listify(v):
        return v["res_id"], v["name"], v["cuisines"], v["cuisine_category"]
    for v in restaurant_dict:
        entry_tuple = r_listify(v)
        cuisine_values.append(entry_tuple)    
    ## defining the Query
    query = "INSERT INTO restaurants (res_id, name, cuisines, cuisine_category) VALUES (%s, %s, %s, %s)"
    ## storing values in a variable
    values = restaurant_values
    ## executing the query with values
    cursor.executemany(query, values)
    ## to make final output we have to run the 'commit()' method of the database object
    db.commit()

#     Load location datat
    location_values = []
    def l_listify(v):
        return v["name"], v["lat"], v["lng"]

    for v in restaurant_dict:
        entry_tuple = l_listify(v)
        location_values.append(entry_tuple) 
    ## defining the Query
    query = "INSERT INTO location (name, lat, lng) VALUES (%s, %s, %s)"
    ## storing values in a variable
    values = location_values
    ## executing the query with values
    cursor.executemany(query, values)
    ## to make final output we have to run the 'commit()' method of the database object
    db.commit()

    
#     Load price data
    price_values = []
    def p_listify(v):
        return v["name"], v["price_range"], v["ave_cost"]

    for v in restaurant_dict:
        entry_tuple = p_listify(v)
        price_values.append(entry_tuple) 

    ## defining the Query
    query = "INSERT INTO price (name, price_range, ave_cost) VALUES (%s, %s, %s)"

    ## storing values in a variable
    values = price_values

    ## executing the query with values
    cursor.executemany(query, values)

    ## to make final output we have to run the 'commit()' method of the database object
    db.commit()

# Load Media Data
    media_values = []
    def m_listify(v):
        return v["name"], v["menu"], v["featured_image"]

    for v in restaurant_dict:
        entry_tuple = m_listify(v)
        media_values.append(entry_tuple)

    ## defining the Query
    query = "INSERT INTO media (name, menu, featured_image) VALUES (%s, %s, %s)"

    ## storing values in a variable
    values = media_values

    ## executing the query with values
    cursor.executemany(query, values)

    ## to make final output we have to run the 'commit()' method of the database object
    db.commit()
    
# Load Review Data    
    reviews_values = []
    def r_listify(v):
        return v["name"], v["vote"], v["rating"]

    for v in restaurant_dict:
        entry_tuple = r_listify(v)
        reviews_values.append(entry_tuple)

    ## defining the Query
    query = "INSERT INTO reviews (name, vote, rating) VALUES (%s, %s, %s)"

    ## storing values in a variable
    values = reviews_values

    ## executing the query with values
    cursor.executemany(query, values)

    ## to make final output we have to run the 'commit()' method of the database object
    db.commit()

    
# Load 

## storing values in a variable

#################################################
# Routes
#################################################    
    
# Renders index page
@app.route("/")
def index():
    """Return the homepage."""
    
    return render_template("index.html")

# 
@app.route("/restaurants")
def data():
    """Return restaurant dictionary."""
    restaurant_dict = []
    api_tojson_todict(url, headers)
    restaurants = json_dict["restaurants"]
    for r in restaurants:
        transformed_dict = create_dict(r)
        restaurant_dict.append(transformed_dict)
    addcategory(restaurant_dict)
    return restaurant_dict


@app.route("/cuisines")
def data():
    """Return restaurant dictionary."""
    cuisine_dict = []
    api_tojson_todict(c_url, c_headers)
    cuisines = json_dict["cuisines"]
    for r in cuisines:
        transformed_dict = create_cuisine(r)
        cuisine_dict.append(transformed_dict)
    return cuisine_dict


@app.route("/names")
def names():
    """Return a list of sample names."""

    results = db.sessions.query(

    # Return a list of the column names (sample names)
    return jsonify(list(df.columns)[2:])





if __name__ == "__main__":
    app.run()
