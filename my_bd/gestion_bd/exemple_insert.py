#! /bin/env python3
import sqlite3
conn = sqlite3.connect("matchs.bd")

matchs = conn.cursor()
id_match = "xrejepde"
matchs.execute("""INSERT INTO MATCHS(id) VALUES(?)""", (id_match, ))
conn.commit()
conn.close()
