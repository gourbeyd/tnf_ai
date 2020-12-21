import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.model_selection import train_test_split
import sys
import numpy
from sklearn import neighbors
import random as rd
import numpy as np


numpy.set_printoptions(threshold=sys.maxsize)
bundes_data = pd.read_csv('BSA1920.csv')

for k in range(len(bundes_data)):
    
    #bundes_data['PSHG'][k] = bundes_data['PSHG'][k]/bundes_data['PSAG'][k]
    if bundes_data['FTR'][k] == 'H':
        bundes_data['FTR'][k] = 1
    else:
        bundes_data['FTR'][k] = -1
bundes_data.to_csv(r'real/BSA1920_real.csv')
