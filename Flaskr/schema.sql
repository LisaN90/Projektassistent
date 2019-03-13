-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS package;
DROP TABLE IF EXISTS status;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE package (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nr TEXT NOT NULL,
  name TEXT NOT NULL,
  bac INTEGER,
  start_date TEXT,
  end_date TEXT
);

CREATE TABLE status (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  package_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  statustext TEXT,
  percentage INTEGER,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (package_id) REFERENCES package (id)
);

