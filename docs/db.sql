CREATE DATABASE Place DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE Place;

CREATE TABLE Places (
  id INT(11) AUTO_INCREMENT NOT NULL,
  -- placeId VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  tel VARCHAR(255),
  address VARCHAR(255),
  img TEXT,

  PRIMARY KEY(id)
) default character set utf8 collate utf8_general_ci, ENGINE = InnoDB;

# placeId, platform, author, contextHash를 묶어서 유니크 값으로 취급한다.
CREATE TABLE Commends (
  id VARCHAR(255) NOT NULL -- 사이트에 표시된 장소 id
  placeId VARCHAR(255) NOT NULL, -- Places 테이블의 id
  platform VARCHAR(255) NOT NULL,
  author VARCHAR(255) NOT NULL,
  contextHash CHAR(64),

  content TEXT,
  grade DOUBLE,

  PRIMARY KEY(platform, author, contextHash),
  FOREIGN KEY (placeId) REFERENCES Places (id)
) default character set utf8 collate utf8_general_ci, ENGINE = InnoDB;

CREATE TABLE Relations (
  placeId INT(11) NOT NULL,

  name VARCHAR(255) NOT NULL,
  link text,

  FOREIGN KEY (placeId) REFERENCES Places (id)
) default character set utf8 collate utf8_general_ci, ENGINE = InnoDB;