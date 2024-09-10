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

class predictor:
    def __init__(self) -> None:
        pass

    def predictWinner(self, driverEntries, constructorEntries, season, weather):

        data = []

        
        for driverEntry in driverEntries:
            startingPosition = driverEntry[1]
            driverPoints = driverEntry[4]
            driverWins = driverEntry[2]
            driverPodiums = driverEntry[3]
            driverStandingPosition = driverEntry[5]
            age = driverEntry[6]
            name = driverEntry[0]
            driverTeam = driverEntry[7]

            for constructorEntry in constructorEntries:
                if driverTeam == constructorEntry[0]:

                    constructorName = constructorEntry[0]
                    constructorPoints = constructorEntry[3]
                    constructorWins = constructorEntry[1]
                    constructorPodiums = constructorEntry[2]
                    constructorStandings = constructorEntry[4]

            with open('Databases/constructors.csv', 'r', encoding="utf-8") as csvfile:
                        
                reader = csv.reader(csvfile)
                for row in reader:
                    print(row[2])
                    print(constructorName)
                    if row[2] == constructorName.strip():
                        constructorID = row[0]
                        break
        
            with open('Databases/drivers.csv', 'r', encoding="utf-8") as csvfile:
                        
                reader = csv.reader(csvfile)
                for row in reader:
                    fullName = row[4] + " " + row[5]
                    print(fullName)
                    print(name)
                    if fullName.strip() == name.strip():
                        driverID = row[0]
                        break
            
            data.append([season.strip(), startingPosition.strip(), constructorPoints.strip(), driverPoints.strip(), constructorID.strip(), driverID.strip(), driverWins.strip(), driverPodiums.strip(), driverStandingPosition.strip(), constructorStandings.strip(), constructorWins.strip(), constructorPodiums.strip(), age.strip()])
        
        df = pd.read_csv('pythonFiles/FinalData/final.csv')
        df.head()
        df.describe()

        X = df[['season','startingPosition','constructorPoints','driverPoints','constructorID','driverID','driverPrevWins','driverPrevPodiums','driverStandingsPos','constructorStandingsPos', 'constructorWins' , 'constructorPodiums' , 'age']]
        Y = df['won']
        pr = PolynomialFeatures(degree=2, include_bias=False)
        X_poly = pr.fit_transform(X)
        lr_2 = LinearRegression()
        lr_2.fit(X_poly, Y)

        prob = lr_2.predict(np.array([data[0]], dtype=np.int64))
        winner = (data[0])[5]
        i = 1
        while i < len(data):
            driver2 = lr_2.predict(np.array([data[i]], dtype=np.int64))
            driver2ID = (data[i])[5]

            indexProb1 = str(prob).index("]")
            tempProb1 = str(prob)[1:indexProb1]

            indexProb2 = str(driver2).index("]")
            tempProb2 = str(driver2)[1:indexProb2]

            print(tempProb1)
            print(tempProb2)

            if float(tempProb1) < float(tempProb2):
                winner = driver2ID
                prob = driver2
            
            i = i + 1
        
        with open('Databases/drivers.csv', 'r', encoding="utf-8") as csvfile:
                        
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[0] == winner:
                        winner = row[4] + " " + row[5]

        prob = prob*100
        lastIndex = str(prob).index("]")
        prob = str(prob)[1:lastIndex]
        return [str(winner), str(prob)]

