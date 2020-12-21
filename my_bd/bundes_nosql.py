#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import sys
import numpy
from sklearn import neighbors
import sqlite3
conn = sqlite3.connect("tnf.bd")
pronos = conn.cursor()

def double_chance(c1, c2):
    m1=c2/(c1+c2)
    return round(m1*c1, 2)

numpy.set_printoptions(threshold=sys.maxsize)

bundes_data = pd.read_csv('1920.csv')

v2 = bundes_data[['HomeTeam', 'AwayTeam', 'FTR', 'B365H', 'B365D', 'B365A', 'FTHG', 'FTAG', 'PSHG', 'PSAG','B365DC','PSDG', 'PLUSPETIT']]
v2 = v2[v2.B365H.notnull()]
v2 = v2[v2.B365A.notnull()]
v2 = v2[v2.B365D.notnull()]
x = np.matrix([np.ones(v2.shape[0]), v2['B365H'].values, v2['PSDG'], v2['B365DC'].values]).T
y = np.matrix([v2['FTR'].values]).T
xtrain, xtest, ytrain, ytest = train_test_split(x, y, train_size=0.6)
cotedc = double_chance(float(sys.argv[2]), float(sys.argv[3]))
cote_home = float(sys.argv[1])
diff_but = float(sys.argv[4])
#\print(len(ytest))
id_match = sys.argv[5]
for j in [53]:
    c_reu = 0
    pari =0
    gain_moy=0
    err_moy = 0
    n = 100
    for i in range(n):
        xtrain, xtest, ytrain, ytest = train_test_split(x, y, train_size=0.6)
        knn = neighbors.KNeighborsClassifier(n_neighbors=j)
        knn.fit(xtrain, np.ravel(ytrain))
        error = 1 - knn.score(xtest, ytest)
        err_moy += error
        ypredict = knn.predict(xtest)
        gain = 0
        compteur = 0
        for s in range(len(ypredict)):
            if ypredict[s]==1: #on predit win de l'equipe home
                if 1.4<xtest[s].tolist()[0][1]<5:
                    compteur += 1
                    if ypredict[s] == ytest[s]:
                        gain += xtest[s].tolist()[0][1]-1  
                        #c_reu +=1;
                    else:
                        gain -= 1
                        #print(xtest[s].tolist()[0][1])
            elif ypredict[s]==-1:
                if 1.4<xtest[s].tolist()[0][3]<5:
                    compteur += 1
                    if ypredict[s] == ytest[s]:
                        gain += xtest[s].tolist()[0][3]-1 #on joue le double chance 
                        #c_reu +=1;
                    else:
                        #print(xtest[s].tolist()[0][3])
                        gain -= 1
        gain=round(gain, 2)
        #cotedc = double_chance(3.8, 1.95)
        pari += knn.predict([[1., cote_home, diff_but, cotedc]])
        if gain >0:
            c_reu +=1
        gain_moy += gain
    #print("cote:", cotedc)
    if pari > 30:
        print("home team to win @", cote_home, pari)
        #pronos.execute("""INSERT INTO PRONOS(id, prono) VALUES(?, ?)""", (id_match, 1))
        conn.commit()
    elif pari < -30:
    	#pronos.execute("""INSERT INTO PRONOS(id, prono) VALUES(?, ?)""", (id_match, -1))
    	conn.commit()
    	print("away team or draw @", cotedc, pari)
    else:
        print("close one, better no gamble")
    #print(j, c_reu, pari, gain_moy/n, err_moy/n, compteur)
