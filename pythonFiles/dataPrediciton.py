import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import model_selection
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn import metrics
from sklearn.metrics import classification_report
from urllib.request import urlopen

df = pd.read_csv('PythonFiles/FinalData/final.csv')
df.head()
df.describe()

X = df[['season','startingPosition','constructorPoints','driverPoints','constructorID','driverID','driverPrevWins','driverPrevPodiums','driverStandingsPos','constructorStandingsPos', 'constructorWins' , 'constructorPodiums' , 'age']]
Y = df['won']

pr = PolynomialFeatures(degree=2, include_bias=False)
X_poly = pr.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(X_poly, Y, test_size=0.3, random_state=42)
lr_2 = LinearRegression()
lr_2.fit(X_train, y_train)
y_pred= lr_2.predict(X_test)
from sklearn.metrics import mean_squared_error
RMSE = np.sqrt(mean_squared_error(y_test, y_pred))

print(y_pred)
print("RMSE: " + str(RMSE))