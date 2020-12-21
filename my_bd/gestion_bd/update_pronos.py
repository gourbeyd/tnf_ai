#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect("../pronos.bd")
pronos = conn.cursor()
pronos.execute("""SELECT * FROM PRONOS WHERE RESULTAT IS NULL""")
rows = pronos.fetchall()
for row in rows:
	print(row)

