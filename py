import sqlite3

conn = sqlite3.connect('ma base')
cur = conn.cursor()
cur.execute("""CREATE TABLE "TABLE1" (
	"ID "	INTEGER NOT NULL,
	"Désignation"	TEXT,
	"reference"	INTEGER,
	"quantite"	INTEGER,
	"quantite minimal"	INTEGER,
	"adresse ip(esp)"	INTEGER,
	PRIMARY KEY("ID " AUTOINCREMENT)
))