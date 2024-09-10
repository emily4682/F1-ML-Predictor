import tkinter 
from tkinter import *
from tkinter import messagebox
from dataPredictionClass import predictor

const_entries = []
season = None
weather = None
driver_entries = []

def calcConstructors():
    numConstructorsTitle.destroy()
    numConstructors = numConstructorsEntry.get()
    submit.destroy()
    numConstructorsEntry.destroy()
    
    i = 1

    while i <= int(numConstructors):
        var = tkinter.IntVar()

        constNum = Label(main, text="----- Constructor Num: " + str(i) + " -----")
        constNum.pack()

        nameTitle = Label(main, text="Constructor Title")
        nameTitle.pack()
        name = Entry(main)
        name.pack()

        pointsTitle = Label(main, text="Constructor Points")
        pointsTitle.pack()
        points = Entry(main)
        points.pack()

        winsTitle = Label(main, text="Constructor Wins So Far this Season")
        winsTitle.pack()
        wins = Entry(main)
        wins.pack()

        podiumTitle = Label(main, text="Constructor Podiums So Far this Season")
        podiumTitle.pack()
        podiums = Entry(main)
        podiums.pack()

        posTitle = Label(main, text="Constructor Standings Position")
        posTitle.pack()
        pos = Entry(main)
        pos.pack()

        submit2 = Button(main, text="Submit Entry", command=lambda: var.set(1))
        submit2.pack()
        submit2.wait_variable(var)

        const_entries.append([name.get(), wins.get(), podiums.get(), points.get(), pos.get()])
    
        constNum.destroy()
        pos.destroy()
        name.destroy()
        podiums.destroy()
        wins.destroy()
        points.destroy()
        nameTitle.destroy()
        posTitle.destroy()
        winsTitle.destroy()
        podiumTitle.destroy()
        pointsTitle.destroy()
        submit2.destroy()
        i = i + 1
    
    complete.pack()

def calcDrivers():
    l.destroy()
    submit.destroy()
    numDrivers = numDriversEntry.get()
    numDriversEntry.destroy()
    
    i = 1
    while i <= int(numDrivers):
        var = tkinter.IntVar()

        constNum = Label(main, text="----- Driver Num: " + str(i) + " -----")
        constNum.pack()

        nameTitle = Label(main, text="Driver Name (First Last)")
        nameTitle.pack()
        name = Entry(main)
        name.pack()

        pointsTitle = Label(main, text="Driver Points")
        pointsTitle.pack()
        points = Entry(main)
        points.pack()

        winsTitle = Label(main, text="Driver Wins So Far this Season")
        winsTitle.pack()
        wins = Entry(main)
        wins.pack()

        podiumTitle = Label(main, text="Driver Podiums So Far this Season")
        podiumTitle.pack()
        podiums = Entry(main)
        podiums.pack()

        posTitle = Label(main, text="Driver Standings Position")
        posTitle.pack()
        pos = Entry(main)
        pos.pack()

        ageTitle = Label(main, text="Driver Age")
        ageTitle.pack()
        age = Entry(main)
        age.pack()

        constructorTitle = Label(main, text="Constructor")
        constructorTitle.pack()
        constructor = Entry(main)
        constructor.pack()

        startingPosTitle = Label(main, text="Starting Position for this race")
        startingPosTitle.pack()
        startingPos = Entry(main)
        startingPos.pack()

        submit2 = Button(main, text="Submit Entry", command=lambda: var.set(1))
        submit2.pack()
        submit2.wait_variable(var)

        driver_entries.append([name.get(), startingPos.get(),  wins.get(), podiums.get(), points.get(), pos.get(), age.get(), constructor.get()])
    
        constructorTitle.destroy()
        constructor.destroy()
        startingPosTitle.destroy()
        startingPos.destroy()
        constNum.destroy()
        pos.destroy()
        name.destroy()
        podiums.destroy()
        wins.destroy()
        points.destroy()
        nameTitle.destroy()
        posTitle.destroy()
        winsTitle.destroy()
        podiumTitle.destroy()
        pointsTitle.destroy()
        ageTitle.destroy()
        age.destroy()
        submit2.destroy()
        i = i + 1

    predict.pack()

def predictWinner():
    pred = predictor()
    data = pred.predictWinner(driver_entries, const_entries, season, weather)
    winner = data[0]
    prob = data[1]

    winner = Label(main, text="The Predicted Winner of this race is: " + winner)
    probability = Label(main, text="With a probability of : " + prob + "%")
    winner.pack()
    probability.pack()

main = tkinter.Tk()
main.geometry("750x550")
var = tkinter.IntVar()

l = Label(main, text="F1 Race Winner Predictor")
l.pack()

main.title('F1 Race Predictor')

numConstructorsTitle = Label(main, text="Please enter the number of constructors in this race")
numConstructorsTitle.pack()
numConstructorsEntry = Entry(main)
numConstructorsEntry.pack()
submit = Button(main, text="Submit", command=calcConstructors)
submit.pack()

complete = Button(main, text="Continue", command=lambda: var.set(1))
complete.wait_variable(var)
complete.destroy()

var = tkinter.IntVar()
seasonTitle = Label(main, text="Please enter the season (year)")
seasonTitle.pack()
year = Entry(main)
year.pack()
complete = Button(main, text="Submit", command=lambda: var.set(1))
complete.pack()
complete.wait_variable(var)
season = year.get()
complete.destroy()
year.destroy()
seasonTitle.destroy()

var = tkinter.IntVar()
weatherTitle = Label(main, text="Please enter if it rained or not (Y/N)")
weatherTitle.pack()
weatherVal = Entry(main)
weatherVal.pack()
complete = Button(main, text="Submit", command=lambda: var.set(1))
complete.pack()
complete.wait_variable(var)
if weatherVal.get() == "Y":
    weather = '1'
else:
    weather = '0'
complete.destroy()
weatherVal.destroy()
weatherTitle.destroy()

l = Label(main, text="Please enter the number of drivers in this race")
l.pack()
numDriversEntry = Entry(main)
numDriversEntry.pack()
submit = Button(main, text="Submit", command=calcDrivers)
submit.pack()

var = tkinter.IntVar()
predict = tkinter.Button(main, text="Predict", width="50", command=predictWinner)

tkinter.mainloop()