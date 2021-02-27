# predict_status
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import StandardScaler

import pandas as pd
import joblib
import pickle
from random import randint


numeric = ["X1", "X2", "X7", "X10", "X13", "X14"]
category = ["X0", "X3", "X4", "X5", "X6", "X8", "X9", "X11", "X12"]
rnd_state = 12345 # фиксируем псевдослучайность

def predict_status(val):
    # заменим "выбросы" некоторыми пороговыми значениями
    p = {7: [20, 16, 20],
        10: [30, 25, 30],
        13: [1250, 1000, 1250],
        14: [20000, 10000, 20000]}
    for i in [7, 10, 13, 14]:
        if  val[i] > p[i][0]:
            val[i] = randint(p[i][1], p[i][2])
    dict_val = {}
    for i in range(len(val)):
        k = 'X' + str(i)
        dict_val[k] = [val[i]]
    df = pd.DataFrame(dict_val)
    
    X = df.copy(deep=True)
    # нормализуем числовые признаки
    sc = pickle.load(open('data/scaler.pkl','rb'))
    X[numeric] = sc.transform(X[numeric])
    # кодируем категории
    dict_cat = {0: ['b', 'a', 'nan'], 3:['u','y', 'nan'],
                 4: ['g', 'p', 'nan'],
                 5: ['c', 'q', 'w', 'i', 'aa', 'ff', 'k', 'cc', 'x', 'm', 'd', 'e', 'j', 'nan'],
                 6: ['v', 'h', 'bb', 'ff', 'j', 'z', 'dd' , 'nan'],
                 8: ['t', 'f'], 9: ['f', 't'], 11: ['f', 't'], 12: ['g', 's', 'p'],}
    
    for key in dict_cat:
        values = dict_cat[key]
        for v in sorted(values)[1:]:
            name_col = "X" + str(key) + "_" + v
            if val[key] == v:
                X[name_col] = 1
            else:
                X[name_col] = 0
 
    X.drop(category, axis=1, inplace=True)
    
    model = joblib.load('data/RandomForestClassifier.joblib')
    
    y_pred = model.predict(X)
    return y_pred

if __name__ == "__main__":
    val = ['b', 30.83, 0, 'u', 'g', 'w', 'v', 1.25, 't', 't', 1, 'f', 'g', 202.0, 0]
    print(predict_status(val))
