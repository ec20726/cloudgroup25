DROP TABLE bob;
DROP TABLE alice;

CREATE TABLE bob (
  id INTEGER PRIMARY KEY,
  sex TEXT NOT NULL,
  weight_kg REAL NOT NULL,
  height_cm REAL NOT NULL,
  age INTEGER,
  exercise TEXT,
  calories REAL
);

INSERT INTO bob VALUES (null, 'Male', 79.3, 182.88, 30, 'run 30 miles', 3431);
INSERT INTO bob VALUES (null, 'Male', 79.3, 182.88, 30, '1 hour walk', 245);
INSERT INTO bob VALUES (null, 'Male', 79.3, 182.88, 30, 'swim 30 mins', 210);
INSERT INTO bob VALUES (null, 'Male', 79.3, 182.88, 30, '45 mins squash game', 383);
INSERT INTO bob VALUES (null, 'Male', 79.3, 182.88, 30, '20 mins yoga', 77);
INSERT INTO bob VALUES (null, 'Male', 79.3, 182.88, 30, '5km cycle ride', 146);
INSERT INTO bob VALUES (null, 'Male', 79.3, 182.88, 30, '90 mins soccer match', 1050);

CREATE TABLE alice (
  id INTEGER PRIMARY KEY,
  sex TEXT NOT NULL,
  weight_kg REAL NOT NULL,
  height_cm REAL NOT NULL,
  age INTEGER,
  exercise TEXT,
  calorie_est REAL
);

INSERT INTO alice VALUES (null, 'Female', 54.5, 167, 25, '20 mins walk', 82);
INSERT INTO alice VALUES (null, 'Female', 54.5, 167, 25, '100 pushups', 22);
INSERT INTO alice VALUES (null, 'Female', 54.5, 167, 25, '8 miles rowing', 168);
INSERT INTO alice VALUES (null, 'Female', 54.5, 167, 25, '30 mins weights', 123);
INSERT INTO alice VALUES (null, 'Female', 54.5, 167, 25, '10 miles cycling', 469);
INSERT INTO alice VALUES (null, 'Female', 54.5, 167, 25, '1 hour table tennis', 280);
INSERT INTO alice VALUES (null, 'Female', 54.5, 167, 25, '30 mins bowling', 133);