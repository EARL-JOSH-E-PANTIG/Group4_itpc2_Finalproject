CREATE DATABASE games_db;
USE games_db;

CREATE TABLE games (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    platform VARCHAR(50) NOT NULL,
    play_status ENUM('Unplayed', 'Playing', 'Completed', 'Abandoned') NOT NULL,
    hours_played DECIMAL(5,1),
    rating INT
);

INSERT INTO games (title, platform, play_status, hours_played, rating)
VALUES ();

SELECT * FROM games;