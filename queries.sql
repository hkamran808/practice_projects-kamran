SELECT * FROM users;

INSERT INTO users (name, age) VALUES ('Kamran', 18);
INSERT INTO users (name, age) VALUES ('Nuray', 19);

UPDATE users SET age = age + 1 WHERE name = 'Ronaldo' OR name = 'Messi';

DELETE FROM users WHERE name = 'Sancho';

SELECT * FROM users;