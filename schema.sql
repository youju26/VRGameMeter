CREATE TABLE vr_games (
  game_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name varchar(255),
  steam_reviews int,
  steam_id int UNIQUE,
  vr_only bool,
  last_updated timestamp DEAFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);