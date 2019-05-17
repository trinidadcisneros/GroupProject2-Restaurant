-- Create and use customer_db
CREATE DATABASE IF NOT EXISTS RestaurantData;
USE RestaurantData;

DROP TABLE restaurants;

-- Create tables for raw data to be loaded into
CREATE TABLE IF NOT EXISTS restaurants (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    lat DECIMAL(6,3),
    lng DECIMAL(6,3),
    cuisine VARCHAR(255),
    ave_cost INT(2),
    rating DECIMAL(4,2)
    vote INT(5),
    price_range INT(2),
    featured_image VARCHAR(255),
    menu VARCHAR(255)
);

