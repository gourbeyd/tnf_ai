#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import sys
import numpy
from sklearn import neighbors

def double_chance(c1, c2):
    m1=c2/(c1+c2)
    return round(m1*c1, 2)


training_data = pd.read_csv('training.csv')

training = training_data[['HomeTeam', 'AwayTeam', 'FTR', 'B365H', 'B365D', 'B365A', 'FTHG', 'FTAG', 'PSHG', 'PSAG','B365DC','PSDG', 'PLUSPETIT']]
training = training[training.B365H.notnull()]
training = training[training.B365A.notnull()]
training = training[training.B365D.notnull()]
x = np.matrix([np.ones(training.shape[0]), training['B365H'].values, training['PSDG'], training['B365DC'].values]).T
y = np.matrix([training['FTR'].values]).T
xtrain, xtest, ytrain, ytest = train_test_split(x, y, train_size=0.9)
white_data=pd.read_csv('ending/FR1718_ending.csv')
#white_data=pd.read_csv('real/FR1718_real.csv')
white = white_data[['HomeTeam', 'AwayTeam', 'FTR', 'B365H', 'B365D', 'B365A', 'FTHG', 'FTAG', 'PSHG', 'PSAG','B365DC','PSDG']]
x_white = np.matrix([np.ones(white.shape[0]), white['B365H'].values, white['PSDG'], white['B365DC'].values]).T
y_white = np.matrix([white['FTR'].values]).T
print(len(y_white))
for j in [ 53]:
    c_reu = 0
    pari =0
    gain_moy=0
    err_moy = 0
    n = 100
    for i in range(n):
        xtrain, xtest, ytrain, ytest = train_test_split(x, y, train_size=0.9)
        knn = neighbors.KNeighborsClassifier(n_neighbors=j)
        knn.fit(xtrain, np.ravel(ytrain))
        error = 1 - knn.score(x_white, y_white)
        err_moy += error
        ypredict = knn.predict(x_white)
        gain = 0
        compteur = 0
        for s in range(len(ypredict)):
            if ypredict[s]==1: #on predit win de l'equipe home
                if 1.3<x_white[s].tolist()[0][1]<3:
                    compteur += 1
                    if ypredict[s] == y_white[s]:
                        gain += x_white[s].tolist()[0][1]-1  
                        
                        #c_reu +=1;
                    else:
                        gain -= 1
                        #print(xtest[s].tolist()[0][1])
            elif ypredict[s]==-1:
                if 1.3<x_white[s].tolist()[0][3]<3:
                    compteur += 1
                    if ypredict[s] == y_white[s]:
                        gain += x_white[s].tolist()[0][3]-1 #on joue le double chance 
                        #c_reu +=1;
                    else:
                        #print(xtest[s].tolist()[0][3])
                        gain -= 1
        gain=round(gain, 2)
        #cotedc = double_chance(3.8, 1.95)
        if gain >0:
            c_reu +=1
        gain_moy += gain
    print(j, c_reu/n*100, "% positif | gain moyen :", round(gain_moy/n, 2), " | % de réussite : ",  round(1-(err_moy/n),2),"| nb de paris :", compteur)
     
