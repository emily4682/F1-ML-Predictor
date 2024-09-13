
import csv
import pandas as pd
from dateutil.relativedelta import relativedelta
import datetime
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup

class dataCollector:

    def __init__(self) -> None:
        pass

    def getData(self):
        data = {
            'season': [],
            'startingPosition': [],
            'constructorPoints': [],
            'driverPoints': [],
            'raining': [],
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
        weather = []

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

                                # Calculate driver age
                                driverDOB = row2[6]
                                driverDOB = datetime.datetime.strptime(driverDOB, '%Y-%m-%d').date()

                    with open('Databases/races.csv', 'r', encoding="utf-8") as csvfile2:
                        
                        reader2 = csv.reader(csvfile2)

                        for row2 in reader2:
                            if row2[0] == row[1]:
                                print(row[0])
                                raceTitle = row2[4]
                                season = row2[1]
                                fullRaceTitle = str(season) + " " + raceTitle
                                url = str(row2[7])

                                # Change HTTP links to HTTPS
                                if "https" not in url:
                                    url = 'https:' + str(url)[5:len(url)]

                                # Check if we have already found the weather for that race
                                if [fullRaceTitle, 0] in weather or [fullRaceTitle, 1] in weather:
                                    for item in weather:
                                        if item[0] == fullRaceTitle:
                                            data['raining'].append(item[1])
                                else:
                                    # Get weather data from wikipedia URL
                                    page = requests.get(url)
                                    content = BeautifulSoup(page.text, 'html.parser')
                                    infoElements = content.find_all('tr')
                                    foundWeather = False
                                    for item in infoElements:
                                        
                                        labels = item.find_all('th', class_="infobox-label")
                                        for label in labels:
                                            if label.text == "Weather":
                                                foundWeather = True
                                                weatherText = item.find('td', class_="infobox-data").text
                                                if 'rain' in weatherText.lower():
                                                    data['raining'].append("1")
                                                    weather.append([fullRaceTitle, 1])
                                                
                                                else:
                                                    data['raining'].append("0")
                                                    weather.append([fullRaceTitle, 0])
                                                

                                    # Back up website if weather not stated on wikipedia page (weather data only available for races up to the 2022 season)
                                    if foundWeather == False and int(season) < 2023:
                                        url = 'https://www.racing-statistics.com/en/events/' + season + "-" + (raceTitle.lower()).replace(" ", "-")
                                        page = requests.get(url)
                                        content = BeautifulSoup(page.text, 'html.parser')
                                        infoElements = content.find_all('tr')          
                                        for item in infoElements:

                                            labels = item.find_all('label')
                                            for label in labels:
                                                # For this site, if the sky condition is clear, precipitation tag isn't included
                                                # Therefore check for this first as if it is clear, we know there was no rain
                                                if label.text == "skycondition":
                                                   
                                                    weatherText = item.find_all('td')
                                                    weatherText = weatherText[1].text
                                                    if 'clear' in weatherText.lower():
                                                        foundWeather = True
                                                        data['raining'].append("0")
                                                        weather.append([fullRaceTitle, 0])
                                                        
                                                
                                                # If it was not clear, then check precipitation 
                                                if foundWeather == False and label.text == "precipation type":
                                                    foundWeather = True
                                                    weatherText = item.find_all('td')
                                                    weatherText = weatherText[1].text
                                                    print(weatherText)
                                                    if 'rain' in weatherText.lower():
                                                        data['raining'].append(1)
                                                        weather.append([fullRaceTitle, 1])
                                                    else:
                                                        data['raining'].append(0)
                                                        weather.append([fullRaceTitle, 0])
                                                    
                                    
                                    # If weather still can't be found, assume it was dry
                                    if foundWeather == False:
                                        data['raining'].append("0")
                                        weather.append([fullRaceTitle, 0])

                                round = int(row2[2])
                                date = row2[5]
                                raceID = row2[0]
                                date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                                data['age'].append(int(relativedelta(date, driverDOB).years))

                    with open('Databases/constructor_results.csv', 'r', encoding="utf-8") as csvfile2:
                        
                        reader2 = csv.reader(csvfile2)

                        for row2 in reader2:
                            # Get correct constructor and race 
                            if row2[2] == row[3] and row2[1] == raceID:
                                points = 0
                                constPoints = 0

                                # Calculate number of points for drivers and constructors 
                                if round == 1:
                                    constPoints = float(row2[3])
                                    points = float(row[9])
                                    driverPoints.append([points, driver, season])
                                  
                                    exists = False
                                    # Check if constructor has already been added (as 2 drivers per team)
                                    for item in constructorPoints:
                                        if item[1] == constructor and item[2] == season:
                                            exists = True
                                            break

                                    # If not, add to array & log it
                                    if exists == False:
                                            constructorPoints.append([constPoints, constructor, season])
                                            constructorLog.append([constructor, season, round])
                                else:
                                    # Increaser driver's points 
                                    for item in driverPoints:
                                        if item[1] == driver and item[2] == season:
                                            points = float(item[0]) + float(row[9])
                                            item[0] = points
                                            break
                                    
                                    exists = False
                                    # Check if constructor points have already been updated
                                    for item in constructorLog:
                                        if item[0] == constructor and item[1] == season and item[2] == round:
                                            exists = True
                                            for item in constructorPoints:
                                                if item[1] == constructor and item[2] == season:
                                                    constPoints = item[0]
                                            
                                    # if not, update their points
                                    if exists == False:
                                        for item in constructorPoints:
                                            if item[1] == constructor and item[2] == season:
                                                constPoints = (float(item[0]) + float(row2[3]))
                                                item[0] = constPoints
                                                constructorLog.append([constructor, season, round])
                                                break
                   
                   # Add to dictionary
                    data['driverPoints'].append(int(points))
                    data['constructorPoints'].append(int(constPoints))
                    data['season'].append(int(season))

                    with open('Databases/standings/constructors.csv', 'r', encoding="utf-8") as csvfile2:
                        
                        reader2 = csv.reader(csvfile2)
                        race = []
                        found = False

                        # Add constructor standings
                        for row2 in reader2:
                            # add position, constuctor title, points and wins to array for that race
                            if row2[4] == (season + " " + raceTitle):
                                race.append([row2[0], row2[1], row2[2], row2[3]])
                            
                        # Then add the constructor wins/podiums/position to data
                        for item in race:
                            if item[1] == constructorName:
                                found = True
                                data['constructorPodiums'].append(int(item[3]))
                                data['constructorWins'].append(int(item[2]))

                                # Make sure constructor wasn't excluded
                                if item[0] != "EX":
                                    data['constructorStandingsPos'].append(int(item[0]))
                                else:
                                    # If EX, position is at the back
                                    data['constructorStandingsPos'].append(len(race) + 1)
                                break
                        
                        # If constructor was not in the csv, they were at the back of the standings with no wins and no podiums
                        if found == False:
                            data['constructorPodiums'].append(0)
                            data['constructorWins'].append(0)
                            data['constructorStandingsPos'].append(len(race) + 1)

                    with open('Databases/standings/drivers.csv', 'r', encoding="utf-8") as csvfile2:
                        
                        reader2 = csv.reader(csvfile2)
                        race = []
                        found = False

                        # Repeat the process above but for drivers
                        for row2 in reader2:
                            if row2[5] == (season + " " + raceTitle):
                                race.append([row2[0], row2[1], row2[3], row2[4]])
                            
                        for item in race:
                            if item[1] == driverFullTitle:
                                found = True
                                data['driverPrevPodiums'].append(int(item[3]))
                                data['driverPrevWins'].append(int(item[2]))

                                # Check driver wasn't disqualified
                                if item[0] != "DSQ":
                                    data['driverStandingsPos'].append(int(item[0]))
                                else:
                                    # If DSQ, position is last
                                    data['driverStandingsPos'].append(len(race) + 1)
                                break
                               
                                break
                        
                        # If driver not listed, assume they are last with no wins/no podiums
                        if found == False:
                            data['driverPrevPodiums'].append(0)
                            data['driverPrevWins'].append(0)
                            data['driverStandingsPos'].append(len(race) + 1)
        return data
                        
                    

# run this method if the final csv need to be refreshed
f = dataCollector()
df = pd.DataFrame.from_dict(f.getData())
df.to_csv("pythonFiles/FinalData/final.csv", index=True)


