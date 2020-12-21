#!/usr/bin/env python3
import sqlite3
import requests

conn = sqlite3.connect("tnf.bd")
cursor = conn.cursor()
cursor.execute("""SELECT * FROM PRONOS WHERE RESULTAT IS NULL""")

rows = cursor.fetchall()

for row in rows:
    adresse = "https://www.flashscore.fr/match/"+row[0]+"/#resume-du-match"
    r = requests.get(adresse)
    words = r.text.split()
    for k  in range(len(words)):
    	if words[k].startswith("<title>"):
    		score = words[k+1].split("-")
    		print(adresse, score)
    		if score!=['', '']:
	    		fthg = int(score[0])
	    		ftag = int(score[1])
	    		if fthg > ftag:
	    			resultat = 1
	    		else:
	    			resultat = -1
	    		
	    		cursor.execute("""UPDATE MATCHS set FTR=?, FTHG=?, FTAG=? WHERE id = (?)""", (resultat, fthg, ftag, row[0]))
	    		conn.commit()
	    		cursor.execute("""SELECT PRONO from PRONOS where id = (?)""", (row[0], ))
	    		if int(cursor.fetchall()[0][0]) == resultat:
	    			if resultat == -1:
	    				cursor.execute("""SELECT OD_DRAW_OR_AWAY from matchs where id = (?)""", (row[0],))
	    				gain = float(cursor.fetchall()[0][0])-1
	    			else:
	    				cursor.execute("""select ODD_HOME from matchs where id=(?)""", (row[0],))
	    				gain = float(cursor.fetchall()[0][0])-1
	    		else:
	    			gain = -1
	    		cursor.execute("""UPDATE PRONOS set resultat = ?, gain = ? WHERE id = (?)""", (resultat, gain, row[0]))
	    		conn.commit()
    		
conn.close()
