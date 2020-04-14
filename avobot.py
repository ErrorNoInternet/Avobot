import os
import time
import random
import tkinter
import datetime
import requests
import threading
from tkinter import *
from tkinter import ttk
from threading import Thread
from tkinter import messagebox
unknownResponse = ["I don't understand you", "What do you mean?", "I couldn't find an answer to that", "What did you say?", "Please say that in another way", "Couldn't find that in my database"]
try:
    with open("responses.data") as file:
        lines = [line.rstrip() for line in file]
except:
    messagebox.showerror("Error", "Could not find responses.data")
def waitExitThread():
    insertText("Goodbye! [2]")
    time.sleep(1)
    insertText("Goodbye! [1]")
    time.sleep(1)
    avobot.destroy()
    file.close()
    sys.exit()
def getWeatherText():
    insertText("Please wait, I'm checking the weather for %s now" %(inputBox.get()))
    cityName = inputBox.get()
    inputBox.bind("<Return>", (lambda event:evaluateInput(inputBox.get())))
    evaluateButton['command'] = lambda:evaluateInput(inputBox.get())
    checkWeatherThread = threading.Thread(target=checkWeather)
    checkWeatherThread.start()
def checkWeather():
    insertText("Please wait, I'm checking the weather for %s now" %(inputBox.get()))
    def format_response(weather):
        try:
            name = weather['name']
            desc = weather['weather'][0]['description']
            temp = weather['main']['temp']
            temp = temp-32	
            temp = temp*5/9
            temp = round(temp,2)
            finalWeather = 'Weather for %s: \nCondition: %s \nTemperature (°C): %s' % (name, desc, temp)
        except:
            finalWeather = 'There was a problem processing weather data'
        return finalWeather
    def getWeather(city):
        inputBox.delete(0, tkinter.END)
        try:
            weatherKey = 'a4aa5e3d83ffefaba8c00284de6ef7c3'
            url = 'https://api.openweathermap.org/data/2.5/weather'
            params = {'APPID': weatherKey, 'q': city, 'units': 'imperial'}
            response = requests.get(url, params=params)
            weather = response.json()
            insertText(format_response(weather))
        except:
            insertText("There was a problem retrieving the weather")
    getWeather(inputBox.get())
def writeName(name):
    dataFile = open("userData.data", "w+")
    dataFile.write(name)
    dataFile.close()
    with open("userData.data") as dataFile:
       lines2 = [line2.rstrip() for line2 in dataFile]
    userName = lines2[0]
    dataFile.close()
    inputBox.bind("<Return>", (lambda event:evaluateInput(inputBox.get())))
    evaluateButton['command'] = lambda:evaluateInput(inputBox.get())
    inputBox.delete(0, tkinter.END)
    insertText("Nice to meet you " + userName + "! How can I help you today?")
    with open("responses.data") as file:
        lines = [line.rstrip() for line in file]
def insertText(text):
    outputBox.delete('1.0', tkinter.END)
    outputBox.insert('1.0', str(text))
def evaluateInput(userInput):
    inputBox.delete(0, tkinter.END)
    lineCounter = 0
    containsKeyword = 0
    originalInput = userInput
    if userInput != "":
        userInput = userInput.upper()
        for line in lines:
            if line != "#ENDFILE#":
                if "q#" in line:
                    question = lines[lineCounter].split('q#')[1]
                    question = question.upper()
                    questionKeywords = question.split(":")
                    keywordsLength = len(questionKeywords)
                    for keyword in questionKeywords:
                        if keyword in userInput:
                            containsKeyword = containsKeyword + 1
                        else:
                            lineCounter = lineCounter + 1
                            containsKeyword = 0
                            break
                    if containsKeyword == keywordsLength:
                        userResponse = lines[lineCounter+1].split('|')
                        output = random.choice(userResponse)
                        if output == "Goodbye!":
                            insertText(output)
                            global waitExitThread
                            waitExitThread = threading.Thread(target=waitExitThread)
                            waitExitThread.start()
                        elif output == "Generating random number":
                            insertText(str(random.randint(1, 10))+"\n"+str(random.randint(11, 100))+"\n"+str(random.randint(101, 1000))+"\n"+str(random.randint(1001, 10000))+"\n"+str(random.randint(10001, 100000))+"\nDone")
                        elif output == "The time is":
                            insertText("The time is umm..")
                            localTime = time.localtime()
                            currentTime = time.strftime("%H:%M:%S", localTime)
                            insertText("The current time is " + currentTime)
                        elif output == "The date is":
                            date = datetime.datetime.now()
                            insertText("The current date is %s/%s/%s (Month, Day, Year)" %(date.month, date.day, date.year))
                        elif output == "Resetting your name":
                            try:
                                os.remove("userData.data")
                                insertText("I've resetted your name. Re-open me and set your new name!")
                            except:
                                insertText("I couldn't reset your name, did you already reset it?")
                        elif output == "Your name is":
                            with open("userData.data") as dataFile:
                               lines2 = [line2.rstrip() for line2 in dataFile]
                            userName = lines2[0]
                            dataFile.close()
                            insertText("Your name is " + userName + ". Did you forget?")
                        elif output == "Say-":
                            try:
                                sayString = originalInput.split(":", 1)[1]
                                checkString = sayString.upper()
                                if "I " in checkString and "STUPID" in checkString:
                                    insertText("I'M NOT STUPID!")
                                if "I'M " in checkString and "STUPID" in checkString:
                                    insertText("I'M NOT STUPID!")
                                if "IM " in checkString and "STUPID" in checkString:
                                    insertText("I'M NOT STUPID!")
                                elif "FUCK" in checkString or "BITCH" in checkString or "SHIT" in checkString:
                                    insertText("I won't swear")
                                else:
                                    insertText(sayString)
                            except:
                                insertText("Use \"Say:[Text]\"")
                        elif output == "Weather: Please wait...":
                            weatherCity = originalInput.replace(" like", "")
                            weatherCity = weatherCity.split(" for ")[1]
                            inputBox.delete(0, tkinter.END)
                            inputBox.insert(0, weatherCity)
                            checkWeatherThread = threading.Thread(target=checkWeather)
                            checkWeatherThread.start()
                        elif output == "Weather2: Please wait...":
                            weatherCity = originalInput.replace(" like", "")
                            weatherCity = weatherCity.split(" in ")[1]
                            inputBox.delete(0, tkinter.END)
                            inputBox.insert(0, weatherCity)
                            checkWeatherThread = threading.Thread(target=checkWeather)
                            checkWeatherThread.start()
                        elif output == "For which city?":
                            insertText("For which city?")
                            inputBox.bind("<Return>", (lambda event:getWeatherText()))
                            evaluateButton['command'] = lambda:getWeatherText()
                        else:
                            insertText(output)
                        break
                else:
                    lineCounter = lineCounter + 1
            else:
                insertText(random.choice(unknownResponse))
    else:
        insertText(random.choice(["You didn't enter anything", "Please enter something", "Say something...", "I don't see anything...?"]))
avobot = tkinter.Tk()
avobot.title("Avobot (Beta 0.05)")
avobot.resizable(False, False)
inputLabel = Label(avobot, text = "Input")
inputLabel.grid(row = 0, column = 0, sticky=N+W, ipadx=5, ipady=5, padx=5, pady=5)
inputBox = ttk.Entry(avobot, width = 40)
inputBox.grid(row = 0, column = 1)
outputBox = Text(avobot, font=("calibri", 12), height=10, width=48)
evaluateButton = ttk.Button(avobot, text="Done", command = lambda:evaluateInput(inputBox.get()))
inputBox.bind("<Return>", (lambda event:evaluateInput(inputBox.get())))
evaluateButton.grid(row = 0, column = 2, padx=5, pady=7)
outputBox.grid(row = 1, columnspan=3)
try:
    with open("userData.data") as dataFile:
       lines2 = [line2.rstrip() for line2 in dataFile]
    userName = lines2[0]
    dataFile.close()
    insertText("Hello " + userName + "! How can I help you today?")
except:
    insertText("Please tell me your name")
    inputBox.bind("<Return>", (lambda event:writeName(inputBox.get())))
    evaluateButton['command'] = lambda:writeName(inputBox.get())
avobot.mainloop()
