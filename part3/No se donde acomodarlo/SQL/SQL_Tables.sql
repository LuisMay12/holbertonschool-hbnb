CREATE TABLE User_Table (
id CHAR(36) PRIMARY KEY,
first_name VARCHAR(255),
last_name VARCHAR(255),
email VARCHAR(255) UNIQUE,
password VARCHAR(255),
is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE Place_Table (
id CHAR(36) PRIMARY KEY,
title VARCHAR(255),
description TEXT,
price DECIMAL(10, 2),
latitude FLOAT,
longitude FLOAT,
owner_id CHAR(36)
);

CREATE TABLE Review_Table (
id CHAR(36) PRIMARY KEY,
text TEXT,
rating INT,
user_id CHAR(36),
place_id CHAR(36)
);

CREATE TABLE Amenity_Table (
id CHAR(36) PRIMARY KEY,
name VARCHAR(255) UNIQUE
);

CREATE TABLE Place_Amenity_Table (
place_id CHAR(36),
amenity_id CHAR(36)
);

CREATE TABLE users (
id CHAR(36) PRIMARY KEY,
email VARCHAR(255) NOT NULL UNIQUE,
first_name VARCHAR(255),
last_name VARCHAR(255),
password VARCHAR(255),
is_admin BOOLEAN DEFAULT FALSE
);