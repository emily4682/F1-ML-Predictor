
import csv
import pandas as pd
from dateutil.relativedelta import relativedelta
import datetime
from urllib.request import urlopen
import re

class dataCollector:

    def __init__(self) -> None:
        pass

    def getData(self):
        data = {
            'season': [],
            'startingPosition': [],
            'constructorPoints': [],
            'driverPoints': [],
            #'raining': [],
            'constructorID': [],
            'driverID': [],
            'driverPrevWins': [],
            'driverPrevPodiums': [],
            'driverStandingsPos': [],
            'constructorStandingsPos': [],
            'constructorWins': [],
            'constructorPodiums': [],
            'age': [],
            'won': [],
        }

        driverPoints = []
        constructorPoints = []
        constructorLog = []

        with open('Databases/results.csv', 'r', encoding="utf-8") as csvfile:
           
            reader = csv.reader(csvfile)

            for row in reader:
                if row[0] != 'resultId':
                    data['startingPosition'].append(int(row[5]))

                    # Check if driver won the race or not
                    if((row[6]) == '1'):
                        data['won'].append(1)
                    else:
                        data['won'].append(0)

                    with open('Databases/constructors.csv', 'r', encoding="utf-8") as csvfile2:
                        
                        reader2 = csv.reader(csvfile2)

                        for row2 in reader2:

                            if row2[0] == row[3]:
                                constructor = row2[1]
                               
                                data['constructorID'].append(int(row[3]))
                                constructorName = row2[2]

                    with open('Databases/drivers.csv', 'r', encoding="utf-8") as csvfile2:
                        
                        reader2 = csv.reader(csvfile2)

                        for row2 in reader2:
                            if row2[0] == row[2]:
                                driver = row2[1]
                               
                                data['driverID'].append(int(row[2]))
                                driverFullTitle = row2[4] + " " + row2[5]
                                driverDOB = row2[6]
                                driverDOB = datetime.datetime.strptime(driverDOB, '%Y-%m-%d').date()

                    with open('Databases/races.csv', 'r', encoding="utf-8") as csvfile2:
                        
                        reader2 = csv.reader(csvfile2)

                        for row2 in reader2:
                            if row2[0] == row[1]:
                                round = int(row2[2])
                                season = row2[1]
                                date = row2[5]
                                raceID = row2[0]
                                raceTitle = row2[4]
                                date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                                data['age'].append(int(relativedelta(date, driverDOB).years))

                    with open('Databases/constructor_results.csv', 'r', encoding="utf-8") as csvfile2:
                        
                        reader2 = csv.reader(csvfile2)

                        for row2 in reader2:

                            if row2[2] == row[3] and row2[1] == raceID:
                                points = 0
                                constPoints = 0
                                if round == 1:
                                    constPoints = float(row2[3])
                                    points = float(row[9])
                                    driverPoints.append([points, driver, season])
                                  
                                    exists = False
                                    for item in constructorPoints:
                                        if item[1] == constructor and item[2] == season:
                                            exists = True
                                            break
                                    
                                    if exists == False:
                                            constructorPoints.append([constPoints, constructor, season])
                                            constructorLog.append([constructor, season, round])
                                else:
                                    for item in driverPoints:
                                        if item[1] == driver and item[2] == season:
                                            points = float(item[0]) + float(row[9])
                                            item[0] = points
                                            break
                                    
                                    exists = False
                                    for item in constructorLog:
                                        if item[0] == constructor and item[1] == season and item[2] == round:
                                            exists = True
                                            for item in constructorPoints:
                                                if item[1] == constructor and item[2] == season:
                                                    constPoints = item[0]
                                            
                                    if exists == False:
                                        for item in constructorPoints:
                                            if item[1] == constructor and item[2] == season:
                                                constPoints = (float(item[0]) + float(row2[3]))
                                                item[0] = constPoints
                                                constructorLog.append([constructor, season, round])
                                                break
                   
                    data['driverPoints'].append(int(points))
                    data['constructorPoints'].append(int(constPoints))
                    data['season'].append(int(season))

                    with open('Databases/standings/constructors.csv', 'r', encoding="utf-8") as csvfile2:
                        
                        reader2 = csv.reader(csvfile2)
                        race = []
                        found = False

                        for row2 in reader2:
                            if row2[4] == (season + " " + raceTitle):
                                race.append([row2[0], row2[1], row2[2], row2[3]])
                            
                        for item in race:
                            if item[1] == constructorName:
                                found = True
                                data['constructorPodiums'].append(int(item[3]))
                                data['constructorWins'].append(int(item[2]))

                                if item[0] != "EX":
                                    data['constructorStandingsPos'].append(int(item[0]))
                                else:
                                    data['constructorStandingsPos'].append(len(race) + 1)
                                break
                        
                        if found == False:
                            data['constructorPodiums'].append(0)
                            data['constructorWins'].append(0)
                            data['constructorStandingsPos'].append(len(race) + 1)

                    with open('Databases/standings/drivers.csv', 'r', encoding="utf-8") as csvfile2:
                        
                        reader2 = csv.reader(csvfile2)
                        race = []
                        found = False

                        for row2 in reader2:
                            if row2[5] == (season + " " + raceTitle):
                                race.append([row2[0], row2[1], row2[3], row2[4]])
                            
                        for item in race:
                            if item[1] == driverFullTitle:
                                found = True
                                data['driverPrevPodiums'].append(int(item[3]))
                                data['driverPrevWins'].append(int(item[2]))

                                if item[0] != "DSQ":
                                    data['driverStandingsPos'].append(int(item[0]))
                                else:
                                    data['driverStandingsPos'].append(len(race) + 1)
                                break
                               
                                break
                        
                        if found == False:
                            data['driverPrevPodiums'].append(0)
                            data['driverPrevWins'].append(0)
                            data['driverStandingsPos'].append(len(race) + 1)
                print("fin")
        return data
                        
                    

# run this method if the final csv need to be refreshed
f = dataCollector()
df = pd.DataFrame.from_dict(f.getData())
df.to_csv("pythonFiles/FinalData/final.csv", index=True)


