CREATE DATABASE Place;
USE Place;

CREATE TABLE Places (
  id INT(11) AUTO_INCREMENT NOT NULL,
  name VARCHAR(255) NOT NULL,
  tel VARCHAR(255),
  address VARCHAR(255),
  img TEXT,

  PRIMARY KEY(id)
) ENGINE = InnoDB;

# platform, author, contextHash를 묶어서 유니크 값으로 취급한다.
CREATE TABLE Commends (
  placeId INT(11) NOT NULL,
  
  platform VARCHAR(255) NOT NULL,
  author VARCHAR(255) NOT NULL,
  contextHash CHAR(64),

  content TEXT,
  grade DOUBLE,

  PRIMARY KEY(platform, author, contextHash),
  FOREIGN KEY (placeId) REFERENCES Places (id)
) ENGINE = InnoDB;

CREATE TABLE Relations (
  placeId INT(11) NOT NULL,

  name VARCHAR(255) NOT NULL,
  link text,

  FOREIGN KEY (placeId) REFERENCES Places (id)
) ENGINE = InnoDB;