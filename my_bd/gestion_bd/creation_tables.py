#! /bin/env python3
import sqlite3


conn = sqlite3.connect("tnf.bd")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE PRONOS(
id VARCHAR(8) PRIMARY KEY,
prono INT,
resultat INT,
gain INT)
""")
cursor.execute("""
CREATE TABLE MATCHS(
id VARCHAR(8) PRIMARY KEY,
date DATE,
HomeTeam VARCHAR(15),
AwayTeam VARCHAR(15),
FTR INT,
ODD_HOME FLOAT,
ODD_DRAW FLOAT,
ODD_AWAY FLOAT,
OD_DRAW_OR_AWAY FLOAT,
FTHG INT,
FTAG INT,
PSHG INT,
PSAG INT)
""")
conn.close()
