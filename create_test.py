# подготовка признаков
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler

from sklearn.model_selection import train_test_split

import pandas as pd
import pickle

numeric = ["X1", "X2", "X7", "X10", "X13", "X14"]
category = ["X0", "X3", "X4", "X5", "X6", "X8", "X9", "X11", "X12"]

url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/credit-screening/crx.data'
df = pd.read_csv(url, header=None, na_values='?')

rnd_state = 12345 # фиксируем псевдослучайность
# делим данные на тренировочный, валидационный и тестовый наборы 80%, 10%, 10%
train, valid  = train_test_split(
    df, test_size=0.2, random_state=rnd_state)

valid, test = train_test_split(
    valid, test_size=0.5, random_state=rnd_state)
new_col = {'index': 'ID', 0: 'X0', 1: 'X1', 2: 'X2',
           3: 'X3', 4: 'X4', 5: 'X5',
           6: 'X6', 7: 'X7', 8: 'X8',
           9: 'X9', 10: 'X10', 11: 'X11',
           12: 'X12', 13: 'X13', 14: 'X14', 15: 'V'}
test.reset_index(inplace=True)
test = test.rename(columns=new_col)
test['ID'] = test['ID'].apply(lambda x: 'IR' + str(x).zfill(6))
print(test)
test.to_csv('data/test.csv')
print('OK')

       
