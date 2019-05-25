DROP DATABASE restaurantdata;
CREATE DATABASE IF NOT EXISTS restaurantdata;
USE restaurantdata;
-- SHOW DATABASES;

-- DELETE TABLES
DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS media;
DROP TABLE IF EXISTS restaurants_cuisines;
DROP TABLE IF EXISTS prices;
DROP TABLE IF EXISTS cuisines;
DROP TABLE IF EXISTS restaurants;

-- DESC cuisines;
# Create restaurant table
CREATE TABLE IF NOT EXISTS restaurants (
id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
`name` VARCHAR(128),
lat DECIMAL(6,3), 
lng DECIMAL (6,3)
) ENGINE=InnoDB;
-- DESC restaurants;

# Create cuisine table
CREATE TABLE IF NOT EXISTS cuisines (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, restaurant_id INT(11), cuisines VARCHAR(128), cuisine_categories VARCHAR(64), KEY restaurant_id_fk (`restaurant_id`)) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS restaurants_cuisines (
id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
restaurant_id INT(11), 
cuisine_id INT(11),
KEY restaurant_id_fk (`restaurant_id`),
KEY cuisine_id_fk (`cuisine_id`),
CONSTRAINT `fk_restaurants_cuisines_restaurants` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurants` (`id`) ON UPDATE CASCADE,
CONSTRAINT `fk_restaurants_cuisines_cuisines` FOREIGN KEY (`cuisine_id`) REFERENCES `cuisines` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB;

# Create price table
CREATE TABLE IF NOT EXISTS prices (
id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
restaurant_id INT(11), 
price_range INT(2), 
ave_cost DECIMAL(6,2),
created_at DATETIME,
KEY restaurant_id_fk (`restaurant_id`),
CONSTRAINT `fk_prices_restaurants` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurants` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB;
DESC price;

# Create media table
CREATE TABLE IF NOT EXISTS media (
id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
restaurant_id INT(11), 
menu_url VARCHAR(255), 
featured_image VARCHAR(255),
KEY restaurant_id_fk (`restaurant_id`),
CONSTRAINT `fk_media_restaurants` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurants` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB;
-- DESC media;

# Create reviews table
CREATE TABLE IF NOT EXISTS reviews (
id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
restaurant_id INT(11), 
vote DECIMAL(6,2), 
rating DECIMAL(6,2),
created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
KEY restaurant_id_fk (`restaurant_id`),
CONSTRAINT `fk_reviews_restaurants` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurants` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB;
-- DESC reviews-- 