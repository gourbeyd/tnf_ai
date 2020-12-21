#!/usr/bin/env python3
import numpy as np
import pandas as pd
import sqlite3

def double_chance(c1, c2):
    m1=c2/(c1+c2)
    return round(m1*c1, 2)

conn = sqlite3.connect("tnf.bd")
matchs = conn.cursor()

bundes_data = pd.read_csv('1920.csv')

v2 = bundes_data[['id', 'Date', 'HomeTeam', 'AwayTeam', 'FTR', 'B365H', 'B365D', 'B365A', 'FTHG', 'FTAG', 'PSHG', 'PSAG','B365DC','PSDG', 'PLUSPETIT']]
v2 = v2[v2.B365H.notnull()]
v2 = v2[v2.B365A.notnull()]
v2 = v2[v2.B365D.notnull()]
for k in range(len(v2['HomeTeam'])):
	id_match = str(v2['id'][k])
	date=v2['Date'][k]
	HomeTeam=str(v2['HomeTeam'][k])
	AwayTeam=str(v2['AwayTeam'][k])
	FTR=int(v2['FTR'][k])
	print(FTR)
	ODD_HOME=v2['B365H'][k]
	ODD_DRAW=v2['B365D'][k]
	ODD_AWAY=v2['B365A'][k]
	OD_DRAW_OR_AWAY=v2['B365DC'][k]
	FTHG = int(v2['FTHG'][k])
	FTAG = int(v2['FTAG'][k])
	PSHG = int(v2['PSHG'][k])
	PSAG = int(v2['PSAG'][k])
	matchs.execute("""INSERT INTO MATCHS(id, date, HomeTeam, AwayTeam, FTR, ODD_HOME, ODD_DRAW, ODD_AWAY, OD_DRAW_OR_AWAY, FTHG, FTAG, PSHG, PSAG) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (id_match, date, HomeTeam, AwayTeam, FTR, ODD_HOME, ODD_DRAW, ODD_AWAY, OD_DRAW_OR_AWAY, FTHG, FTAG, PSHG, PSAG))
	conn.commit()
conn.close()
