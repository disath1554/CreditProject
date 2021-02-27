import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import  RandomForestClassifier

from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler

import joblib
import pickle

from random import randint

# подготовка признаков (функция)

numeric = ["X1", "X2", "X7", "X10", "X13", "X14"]
category = ["X0", "X3", "X4", "X5", "X6", "X8", "X9", "X11", "X12"]
rnd_state = 12345 # фиксируем псевдослучайность

#a1, a2 - тип предварительной обработки категориальных и числовых данных
def preparation_of_signs(a1="C", a2="D"): 
    url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/credit-screening/crx.data'
    data = pd.read_csv(url, header=None, na_values='?')
    # переименуем столбцы
    colnames = {}
    for i in range(data.shape[1] - 1):
        colnames[i] = "X" + str(i)
    colnames[15] = "Y"
    data.rename(columns = colnames, inplace = True)
    # закодируем целевой признак
    data["Y"] = data["Y"].replace('-', '0')
    data["Y"] = data["Y"].replace('+', '1')
    data["Y"] = data["Y"].astype(int)
    
    if a1 == "C":
        # создаем категорию пропуск
        for c in category:
            data[c].fillna('nan', inplace=True)
         
        # добавляем в категорию nan редкие значения (эксперимент!)
        data["X6"].replace('o', 'nan', inplace=True)
        data["X6"].replace('n', 'nan', inplace=True) 
        data["X5"].replace('r', 'nan', inplace=True) 
        data["X4"].replace('gg', 'nan', inplace=True) 
        data["X3"].replace('l', 'nan', inplace=True)
        
    sts = data.describe()
    
    if a2 == "D":
        # заполняем пропуски медианой (50% квартиль)
        for col in numeric:
            if data[col].isna().sum() > 0:
                data[col].fillna(sts[col]["50%"], inplace=True)
        
        # заменим "выбросы" некоторыми пороговыми значениями (эксперимент!)
        # при такой замене это можно делать до деления на train, valid, test
        p = {"X7": [20, 16, 20],
             "X10": [30, 25, 30],
             "X13": [1250, 1000, 1250],
             "X14": [20000, 10000, 20000]}
        for i in p.keys():
            for j in range(data.shape[0]):
                if  data[i][j] > p[i][0]:
                    data[i][j] = randint(p[i][1], p[i][2])
    
   
    # выделяем признаки и целевой признак   
    X = data.drop(["Y"], axis=1)
    y = data["Y"]
    #X.to_csv('test.csv')
    # кодируем категории
    cat_list = []
    for item in category:
        c = list(X[item].unique())
        print(c)

    X = pd.get_dummies(X,  columns=category, drop_first=True)
    
    # делим данные на тренировочный, валидационный и тестовый наборы 80%, 10%, 10%
    Xtrain, Xvalid, Ytrain, Yvalid = train_test_split(
        X, y, test_size=0.2, random_state=rnd_state)

    Xvalid, Xtest, Yvalid, Ytest = train_test_split(
        Xvalid, Yvalid, test_size=0.5, random_state=rnd_state)
    
    # стандартизируем числовые признаки
    scaler = StandardScaler()
    scaler.fit(Xtrain[numeric])
    Xtrain[numeric] = scaler.transform(Xtrain[numeric])
    Xvalid[numeric] = scaler.transform(Xvalid[numeric])
    Xtest[numeric] = scaler.transform(Xtest[numeric])
    
    pickle.dump(scaler, open('data\scaler.pkl','wb'))
    
    return Xtrain, Xvalid, Xtest, Ytrain, Yvalid, Ytest

Xtrain, Xvalid, Xtest, Ytrain, Yvalid, Ytest = preparation_of_signs()

# проверка работы функции
print(Xtrain.columns)
print("train ",Xtrain.shape, Ytrain.shape)
print("valid ",Xvalid.shape, Yvalid.shape)
print("test ",Xtest.shape, Ytest.shape)


depth = 6
estim = 80
print('RandomForestClassifier')
model = RandomForestClassifier(random_state=rnd_state,
                               n_estimators=estim,
                               class_weight='balanced',
                               max_depth=depth)
model.fit(Xtrain, Ytrain)

# сохранение модели
joblib.dump(model, 'data\RandomForestClassifier.joblib')
saved_model = pickle.dumps(model)
pickle.dump(saved_model, open('data\model.pkl','wb'))
        
       
