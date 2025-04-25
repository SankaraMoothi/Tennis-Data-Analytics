CREATE DATABASE IF NOT EXISTS tennis_data;
USE tennis_data;

CREATE TABLE Categories (
  category_id VARCHAR(50) PRIMARY KEY,
  category_name VARCHAR(100)
);

CREATE TABLE Competitions (
  competition_id VARCHAR(50) PRIMARY KEY,
  competition_name VARCHAR(100),
  parent_id VARCHAR(50),
  type VARCHAR(50),
  gender VARCHAR(10),
  category_id VARCHAR(50),
  FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

CREATE TABLE Complexes (
  complex_id VARCHAR(50) PRIMARY KEY,
  name VARCHAR(100)
);

CREATE TABLE Venues (
  venue_id VARCHAR(50) PRIMARY KEY,
  name VARCHAR(100),
  city_name VARCHAR(100),
  country_name VARCHAR(100),
  country_code CHAR(3),
  timezone VARCHAR(100),
  complex_id VARCHAR(50),
  FOREIGN KEY (complex_id) REFERENCES Complexes(complex_id)
);

CREATE TABLE Competitors (
  competitor_id VARCHAR(50) PRIMARY KEY,
  name VARCHAR(100),
  country VARCHAR(100),
  country_code CHAR(3),
  abbreviation VARCHAR(10)
);

CREATE TABLE Competitor_Rankings (
  rank_id INT AUTO_INCREMENT PRIMARY KEY,
  `rank` INT,
  movement INT,
  points INT,
  competitions_played INT,
  competitor_id VARCHAR(50),
  FOREIGN KEY (competitor_id) REFERENCES Competitors(competitor_id)
);
