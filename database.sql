-- Create and use customer_db
CREATE DATABASE IF NOT EXISTS RestaurantData;
USE RestaurantData;

DROP TABLE restaurants;

-- Create tables for raw data to be loaded into
CREATE TABLE IF NOT EXISTS restaurants (
    id = Column(Integer, primary_key=True),
    name VARCHAR(255),
    lat FLOAT(5),
    lng FLOAT(5),
    cuisine VARCHAR(255),
    ave_cost FLOAT(2),
    rating INTEGER,
    vote INTEGER,
    price_range INTEGER,
    featured_image VARCHAR(255),
    menu VARCHAR(255)
);

