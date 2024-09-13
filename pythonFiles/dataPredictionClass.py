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

            # Extracting the data from the driver entries array
            startingPosition = driverEntry[1]
            driverPoints = driverEntry[4]
            driverWins = driverEntry[2]
            driverPodiums = driverEntry[3]
            driverStandingPosition = driverEntry[5]
            age = driverEntry[6]
            name = driverEntry[0]
            driverTeam = driverEntry[7]

            # Get constructor data for that driver
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
                    
                    # Figure out the constructor's ID
                    if row[2] == constructorName.strip():
                        constructorID = row[0]
                        break
        
            with open('Databases/drivers.csv', 'r', encoding="utf-8") as csvfile:
                        
                reader = csv.reader(csvfile)
                for row in reader:
                    fullName = row[4] + " " + row[5]
                    
                    # Figure out driver's ID
                    if fullName.strip() == name.strip():
                        driverID = row[0]
                        break
            
            # Create array with data to be used in model
            data.append([season.strip(), startingPosition.strip(), constructorPoints.strip(), driverPoints.strip(), weather, constructorID.strip(), driverID.strip(), driverWins.strip(), driverPodiums.strip(), driverStandingPosition.strip(), constructorStandings.strip(), constructorWins.strip(), constructorPodiums.strip(), age.strip()])
        
        #Create & train model with final.csv
        
        # Get data from previous races
        df = pd.read_csv('PythonFiles/FinalData/final.csv')
        df.head()
        df.describe()

        X = df[['season','startingPosition','constructorPoints','driverPoints', 'raining','constructorID','driverID','driverPrevWins','driverPrevPodiums','driverStandingsPos','constructorStandingsPos', 'constructorWins' , 'constructorPodiums' , 'age']]
        Y = df['won']

        pr = PolynomialFeatures(degree=2, include_bias=False)
        X_poly = pr.fit_transform(X) 


        # Build linear regression model
        lr_model = LinearRegression()
        lr_model.fit(X_poly, Y)
 
        # Predict winner for 1st driver with model
        poly = pr.fit_transform([data[0]])
        prob = lr_model.predict(np.array(poly, dtype=np.int64))
        winner = (data[0])[5]
        i = 1
        # For all other drivers, calculate win probability
        while i < len(data):
            poly2 = pr.fit_transform([data[i]])
            driver2 = lr_model.predict(np.array(poly2, dtype=np.int64))
            driver2ID = (data[i])[5]

            indexProb1 = str(prob).index("]")
            tempProb1 = str(prob)[1:indexProb1]

            indexProb2 = str(driver2).index("]")
            tempProb2 = str(driver2)[1:indexProb2]

            # If other driver has a higher probability, set them as the temporary winner
            if float(tempProb1) < float(tempProb2):
                winner = driver2ID
                prob = driver2
            
            i = i + 1
        
        with open('Databases/drivers.csv', 'r', encoding="utf-8") as csvfile:
                        
                # Get winner name
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[0] == winner:
                        winner = row[4] + " " + row[5]

        # Calculate probability as percentage
        prob = prob*100
        lastIndex = str(prob).index("]")
        prob = str(prob)[1:lastIndex]

        #Return winner
        return [str(winner), str(prob)]

