CREATE DATABASE Place DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE Place;

CREATE TABLE Places (
  id INT(11) AUTO_INCREMENT NOT NULL,
  -- placeId VARCHAR(255) NOT NULL,
  name VARCHAR(255) NOT NULL,
  tel VARCHAR(255),
  address VARCHAR(255),
  img TEXT,

  PRIMARY KEY(id)
) default CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci, ENGINE = InnoDB;

# placeId, platform, author, contentHash를 묶어서 유니크 값으로 취급한다.
CREATE TABLE Comments (
  placeId INT(11) NOT NULL, -- Places 테이블의 id
  
  platform VARCHAR(30) NOT NULL,
  siteId VARCHAR(255) NOT NULL, -- 사이트에 표시된 장소 id
  author VARCHAR(255) NOT NULL,
  content TEXT,
  
  contentHash CHAR(64),

  grade DOUBLE,

  PRIMARY KEY(platform, siteId, author, contentHash),
  FOREIGN KEY (placeId) REFERENCES Places (id)
) default CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci, ENGINE = InnoDB;

CREATE TABLE Relations (
  placeId INT(11) NOT NULL,

  name VARCHAR(255) NOT NULL,
  link text,

  FOREIGN KEY (placeId) REFERENCES Places (id)
) default CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci, ENGINE = InnoDB;