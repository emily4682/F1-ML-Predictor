# F1 Race Predictor using ML (Linear Regression)
 *Machine Learning Program based in Python to predict results for F1 Races.*
 
 **STILL TO ADD (to be added this week):**
 - Weather (Wet/Dry conditions)

 Description
 -
 
 This project was my first try at a machine learning program. It was also the first python project I've done in quite a while! But I was up for the challenge.

 Overall, this project took me around 5/6 days with the programming and research.

 This project is able to take data from 1950-2024 and figure out the correlation between certain pieces of data and a driver winning a race in order to make a rough predicition on who will win. However, due to the unpredicable nature of F1, no prediciton can account for the unexpected events that can occur on track.

 The data I used to predict the winner was:
- Driver's Staring Position
- Driver Themself
- Driver's Current Championship Points
- Driver's Wins That Season
- Driver's Podiums That Season
- Place in the Driver's Championship
- Driver's Age
- Car (The Constructor)
- Constructor's Points
- Constructor's Wins
- Constructor's Podiums 
- Place in the Constructor's Championship
- If the weather was wet or dry

This data allowed the model to get a feel for the driver's ability, the ability of their car, and the race conditions. To collect this data I used the data from the CSV files provided by Kaggle. (the data collection process can be seen in **dataCollection.py**)

 To allow users to test the model on real-time races, I built a basic UI using tkinter to allow users to input the data for a season up to the latest qualifying in order to predict the outcome for the following race. This UI can be seen in **UI.py**

 I thought that the driver's/constructor's place in the current championship was very important. However, that data wasn't provided by the datasets I used (Kaggle). So I used an automation tool (UiPath) and built an automated bot that would go through each race from 1950-2024 on https://pitwall.app/ in order to get the driver's & constructor's position in their championships after each round.

 *My Chosen ML Model*
 -

- **dataPrediction.py**
    - Shows the training & testing model

- **dataPredictionClass.py**
    - Shows how the model makes a prediciton from the user input & determines the most probable outcome

 I used a Polynomial regression model for this project that had a RMSE value of 0.1644 (to 4 d.p). Meaning the model had an accuracy of around 84% (or an error rate of 16%). A polynomial regression model was 0.97% more accurate than a linear model.

  To get this RMSE value, the data from 1950-2024 (up to 2024 British GP) was tested using a train/test model. I trained the model with 70% of the data and then tested with the remaining 30%. 

 ````python
#ML Model for testing & training

df = pd.read_csv('PythonFiles/FinalData/final.csv')
df.head()
df.describe()

X = df[['season','startingPosition','constructorPoints','driverPoints', 'raining','constructorID','driverID','driverPrevWins','driverPrevPodiums','driverStandingsPos','constructorStandingsPos', 'constructorWins' , 'constructorPodiums' , 'age']]
Y = df['won']

pr = PolynomialFeatures(degree=2, include_bias=False)
X_poly = pr.fit_transform(X) 

#Split data into train & test
X_train, X_test, y_train, y_test = train_test_split(X_poly, Y, test_size=0.3, random_state=42)

# Built linear regression model with training data
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# Predict test data
y_pred= lr_model.predict(X_test)

# Calculate RMSE value to test accuracy
from sklearn.metrics import mean_squared_error
RMSE = np.sqrt(mean_squared_error(y_test, y_pred))

print("RMSE: " + str(RMSE))

>> RMSE = 0.16439617852664945

````
````python  

# ML Model for predicting based on user input

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
winner = (data[0])[5] #Get DriverID

# The model will iterativley predict for each driver and find the driver with the highest probability
````

 *Limitations when predicting F1 race outcomes*
 -

 Due to the nature of the sport. Unexpected events can occur. It is hard to predict critial moments in an F1 race so there are limitations as to how accurate the model can be. 

 **For Example:**
 The model interprets a driver's skill level through their win history, points, number of podiums, their position in the championship and their results in previous seasons. But this won't account for a driver taking too much risk in a corner and crashing (for example). Therefore, there will always be unexpected results. 

 There is also the strategy the team decides to choose in the race, and this is a huge impact on the outcome.
 We can try to predict how well a team can strategise using the constructors championship/points etc.. However, that will not account for a bad/good strategy on the day of the race.

However, this predictor does mange to give a rough idea of who the winner could be from a race. 

*Limitations to be worked on*
-

There are still limitations with the current project that I wish to work on in the future. 

Some of these factors are thing like some circuits are better for overtaking and some are worse. Therefore the correlation between certain grid positions and a win will be different for each circuit. 

So, in a further iteration of this project I'd like the project to be able to model the probabilities based on the circuit itself.

Also taking into account a driver's personal crash rate would help increase accuracy. As if a driver is very prone to crashing, this will reduce their overall chance of winning, as they have a higher chance of crashing the car during the race. 

Along the same line, I could also add a check to see if drivers are more likely to crash at one circuit than another. 

**For Example**: Due to the close walls at Monaco and other narrow street circuits, there is generally a higher probability of a driver crashing compared to a track circuit that is built with run off areas.

*Refrences*
-

 Inspiration from this project: https://towardsdatascience.com/formula-1-race-predictor-5d4bfae887da

 Datasets from: https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020 

 Data also used from:
 https://pitwall.app/
