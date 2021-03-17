CREATE TABLE bob (
  id INTEGER PRIMARY KEY,
  sex TEXT NOT NULL,
  weight_kg REAL NOT NULL,
  height_cm REAL NOT NULL,
  age INTEGER,
  exercise TEXT
);

INSERT INTO bob VALUES (null, 'Male', 79.3, 182.88, 30, 'run 30 miles');
INSERT INTO bob VALUES (null, 'Male', 79.3, 182.88, 30, '1 hour walk');
INSERT INTO bob VALUES (null, 'Male', 79.3, 182.88, 30, 'swim 30 mins');
INSERT INTO bob VALUES (null, 'Male', 79.3, 182.88, 30, '45 mins squash game');
INSERT INTO bob VALUES (null, 'Male', 79.3, 182.88, 30, '20 mins yoga');
INSERT INTO bob VALUES (null, 'Male', 79.3, 182.88, 30, '5km cycle ride');
INSERT INTO bob VALUES (null, 'Male', 79.3, 182.88, 30, '90 mins soccer match');

CREATE TABLE alice (
  id INTEGER PRIMARY KEY,
  sex TEXT NOT NULL,
  weight_kg REAL NOT NULL,
  height_cm REAL NOT NULL,
  age INTEGER,
  exercise TEXT
);

INSERT INTO alice VALUES (null, 'Female', 54.5, 167, 25, '20 mins walk');
INSERT INTO alice VALUES (null, 'Female', 54.5, 167, 25, '100 pushups');
INSERT INTO alice VALUES (null, 'Female', 54.5, 167, 25, '8 miles rowing');
INSERT INTO alice VALUES (null, 'Female', 54.5, 167, 25, '30 mins weights');
INSERT INTO alice VALUES (null, 'Female', 54.5, 167, 25, '10 miles cycling');
INSERT INTO alice VALUES (null, 'Female', 54.5, 167, 25, '1 hour table tennis');
INSERT INTO alice VALUES (null, 'Female', 54.5, 167, 25, '30 mins bowling');