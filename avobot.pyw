import os
import re
import sys
import time
import random
import tkinter
import datetime
import requests
import threading
import subprocess
from tkinter import *
from tkinter import ttk
from threading import Thread
from tkinter import messagebox
from IPython.display import HTML
weatherAPIKey = "a4aa5e3d83ffefaba8c00284de6ef7c3"
bingSearchAPIKey = "537fecf13d894cbe8781e6c6a593dc61"
emotionCounter = 0
unknownResponse = ["I don't understand you", "What do you mean?", "I couldn't find an answer to that", "What did you say?", "Please say that in another way", "Couldn't find that in my database"]
try:
    with open("responses.data") as file:
        lines = [line.rstrip() for line in file]
except:
    messagebox.showerror("Error", "Could not find responses.data")
def createExitThread():
    global waitExitThread
    waitExitThread = threading.Thread(target=waitExitThread)
    waitExitThread.start()
def searchWeb():
    insertText("Searching the web for \"" + inputBox.get() + "\"")
    searchThread = threading.Thread(target=getWebResult)
    searchThread.start()
def getWebResult():
    try:
        subscriptionKey = bingSearchAPIKey
        assert subscriptionKey
        searchUrl = "https://api.cognitive.microsoft.com/bing/v7.0/search"
        searchTerm = inputBox.get()
        inputBox.delete(0, tkinter.END)
        headers = {"Ocp-Apim-Subscription-Key": subscriptionKey}
        params = {"q": searchTerm, "textDecorations": True, "textFormat": "HTML"}
        response = requests.get(searchUrl, headers=headers, params=params)
        response.raise_for_status()
        searchResults = response.json()
        rows = "\n".join(["""<tr>
                           <td><a href=\"{0}\">{1}</a></td>
                           <td>{2}</td>
                         </tr>""".format(v["url"], v["name"], v["snippet"])
                      for v in searchResults["webPages"]["value"]])
        HTML("<table>{0}</table>".format(rows))
        start_sep='<td>'
        end_sep='</td>'
        result=[]
        tmp=rows.split(start_sep)
        for par in tmp:
          if end_sep in par:
            result.append(par.split(end_sep)[0])
        start_sep='<td>'
        end_sep='</td>'
        result=[]
        tmp=rows.split(start_sep)
        counter = 0
        for par in tmp:
          if end_sep in par:
            if "href" in par.split(end_sep)[0]:
                result.append(par.split(end_sep)[0])
                counter = counter + 1
                result.append("\n")
            else:
                result.append(par.split(end_sep)[0])
                result.append("\n\n")
        new = ""
        for item in result:
            new += item
        new = new.replace("<a href=\"", "Link: ")
        new = new.replace("\">", "\nTitle: ")
        final = new.replace("</a>", "")
        final = final.replace("<b>", "")
        final = final.replace("</b>", "")
        final = final.replace("&#39;", "")
        final = final.replace("&quot;", "\"")
        final = final.replace("&amp;", "and")
        insertText("Found " + str(counter+1) + " results: \n\n" + final, "instant")
        inputBox.bind("<Return>", (lambda event:evaluateInput(inputBox.get())))
        evaluateButton['command'] = lambda:evaluateInput(inputBox.get())
    except Exception as error:
        insertText("Couldn't get any results from the web\n"+str(error))
def openFile(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])
def endlessClock():
    inputBox.bind("<Return>", (lambda event:print("Clock is running")))
    evaluateButton['command'] = lambda:print("Clock is running")
    while "STOP" not in inputBox.get().upper():
        localTime = time.localtime()
        date = datetime.datetime.now()
        currentTime = datetime.datetime.now().time()
        insertText("Time: " + str(currentTime) + "\nDate: %s/%s/%s (M/D/Y)" %(date.month, date.day, date.year), "instant")
        time.sleep(0.1)
    inputBox.bind("<Return>", (lambda event:evaluateInput(inputBox.get())))
    evaluateButton['command'] = lambda:evaluateInput(inputBox.get())
    inputBox.delete(0, tkinter.END)
    insertText("Stopped the clock", "instant")
def waitExitThread():
    userName = ""
    try:
        with open("userData.data") as dataFile:
            lines2 = [line2.rstrip() for line2 in dataFile]
        userName = lines2[0]
    except:
        userName = "User"
    outputBox.delete('1.0', tkinter.END)
    insertText("Bye " + userName + "! [2]")
    time.sleep(1)
    insertText("Bye " + userName + "! [1]")
    time.sleep(0.5)
    def fade():
        alpha = avobot.attributes("-alpha")
        if alpha > 0.003:
            alpha -= 0.003
            avobot.attributes("-alpha", alpha)
            avobot.after(1, fade)
        else:
            avobot.destroy()
            file.close()
            sys.exit()
            exit()
    fade()
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
            locationLon = weather['coord']['lon']
            locationLat = weather['coord']['lat']
            desc = weather['weather'][0]['description']
            temp = weather['main']['temp']
            feelslike = weather['main']['feels_like']
            tempMin = weather['main']['temp_min']
            tempMax = weather['main']['temp_max']
            speed = weather['wind']['speed']
            humidity = weather['main']['humidity']
            country = weather['sys']['country']
            desc = desc.title()
            def convertToCelsius(integer):
                integer = integer-32	
                integer = integer*5/9
                integer = round(integer, 2)
                return integer
            finalWeather = 'Weather for %s, %s: \nLongitude: %s, Latitude: %s\nCondition: %s \nCurrent Temperature (°C): %s\nLowest Temperature (°C): %s\nHighest Temperature (°C): %s\nTemperature Feels Like (°C): %s\nWind Speed (KM/H): %s\nAir Humidity (Percent): %s' % (name, country, locationLon, locationLat,desc, convertToCelsius(temp), convertToCelsius(tempMin), convertToCelsius(tempMax), convertToCelsius(feelslike), speed, humidity)
        except Exception as error:
            if emotionCounter == 1:
                finalWeather = "Couldn't get the weather"
            else:
                finalWeather = 'Your city name does not exist'
        return finalWeather
    def getWeather(city):
        inputBox.delete(0, tkinter.END)
        try:
            weatherKey = weatherAPIKey
            url = 'https://api.openweathermap.org/data/2.5/weather'
            params = {'APPID': weatherKey, 'q': city, 'units': 'imperial'}
            response = requests.get(url, params=params)
            weather = response.json()
            insertText(format_response(weather))
        except:
            if emotionCounter == 1:
                insertText("Couldn't get the weather")
            else:
                insertText("Failed to get the weather, are you connected to the internet?")
    getWeather(inputBox.get())
def writeName(name):
    try:
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
    except:
        insertText("I can't remember your name, try running me as administrator")
def insertCharacter(text, speed):
    if speed == None:
        speed = "normal"
    else:
        speed = "instant"
    if speed == "normal":
        textArray = []
        for character in text:
            textArray.append(character)
        for character in textArray:
            outputBox.insert(tkinter.END, character)
            time.sleep(0.01)
    else:
        outputBox.insert(tkinter.END, text)
def insertText(text, speed=None):
    outputBox.delete('1.0', tkinter.END)
    insertThread = threading.Thread(target=insertCharacter, args=(text, speed))
    insertThread.start()    
def evaluateInput(userInput):
    inputBox.delete(0, tkinter.END)
    lineCounter = 0
    containsKeyword = 0
    originalInput = userInput
    if userInput != "":
        userInput = userInput.upper()
        if "FUCK" in userInput or "BITCH" in userInput or "SHIT" in userInput and "SAY:" in userInput:
            pass
        if "FUCK" in userInput or "BITCH" in userInput or "SHIT" in userInput:
            if "SAY" in userInput:
                pass
            else:
                global emotionCounter
                emotionCounter = 1
        if "SORRY" in userInput:
            emotionCounter = 0
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
                            createExitThread()
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
                                if emotionCounter == 1:
                                    insertText("I couldn't reset your name")
                                elif emotionCounter == 0:
                                    insertText("I couldn't reset your name, did you already reset it?")
                                else:
                                    insertText("I couldn't reset your name, did you already reset it?")
                        elif output == "Your name is":
                            try:
                                with open("userData.data") as dataFile:
                                   lines2 = [line2.rstrip() for line2 in dataFile]
                                userName = lines2[0]
                                dataFile.close()
                                insertText("Your name is " + userName + ". Did you forget?")
                            except:
                                insertText("You've resetted your name, please restart Avobot to set a new name")
                        elif output == "Say-":
                            try:
                                if emotionCounter == 1:
                                    insertText("No, because you sweared")
                                else:
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
                            weatherCity = weatherCity.replace('?', "")
                            weatherCity = weatherCity.replace("today", "")
                            weatherCity = weatherCity.split(" for ")[1]
                            inputBox.delete(0, tkinter.END)
                            inputBox.insert(0, weatherCity)
                            checkWeatherThread = threading.Thread(target=checkWeather)
                            checkWeatherThread.start()
                        elif output == "Weather2: Please wait...":
                            weatherCity = originalInput.replace(" like", "")
                            weatherCity = weatherCity.replace('?', "")
                            weatherCity = weatherCity.replace("today", "")
                            weatherCity = weatherCity.split(" in ")[1]
                            inputBox.delete(0, tkinter.END)
                            inputBox.insert(0, weatherCity)
                            checkWeatherThread = threading.Thread(target=checkWeather)
                            checkWeatherThread.start()
                        elif output == "For which city?":
                            insertText("For which city?")
                            inputBox.bind("<Return>", (lambda event:getWeatherText()))
                            evaluateButton['command'] = lambda:getWeatherText()
                        elif output == "Running endless clock":
                            clockThread = threading.Thread(target=endlessClock)
                            clockThread.start()
                        elif output == "Opening":
                            startFile = originalInput
                            startFile = startFile.replace("OPEN", "open")
                            startFile = startFile.replace("Open", "open")
                            startFile = startFile.replace("oPEN", "open")
                            startFile = startFile.split("open ")[1]
                            try:
                                openFile(str(startFile))
                                insertText("Opened " + str(startFile))
                            except Exception as error:
                                insertText("Failed to open " + str(startFile) + "\n" + str(error))
                        elif output == "Searching web":
                            if "FOR" in userInput:
                                try:
                                    searchString = originalInput
                                    searchString = searchString.replace("SEARCH", "search")
                                    searchString = searchString.replace("Search", "search")
                                    searchString = searchString.replace("sEARCH", "search")
                                    searchString = searchString.replace("FOR", "for")
                                    searchString = searchString.replace("For", "for")
                                    searchString = searchString.replace("fOR", "for")
                                    searchTerm = searchString.split("search for ")[1]
                                    inputBox.delete(0, tkinter.END)
                                    inputBox.insert(0, searchTerm)
                                    insertText("Searching the web for \"" + inputBox.get() + "\"")
                                    searchThread = threading.Thread(target=getWebResult)
                                    searchThread.start()
                                except:
                                    insertText("Use \"Search for: [Term]\"")
                            else:
                                insertText("What do you want to search?")
                                inputBox.bind("<Return>", (lambda event:searchWeb()))
                                evaluateButton['command'] = lambda:searchWeb()
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
hideThread = threading.Thread(target=avobot.attributes("-alpha", 0))
hideThread.start()
avobot.protocol("WM_DELETE_WINDOW", createExitThread)
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
def fadeOpen():
        alpha = avobot.attributes("-alpha")
        if alpha < 100:
            alpha += 0.001
            avobot.attributes("-alpha", alpha)
            avobot.after(1, fadeOpen)
        else:
            avobot.attributes("-alpha", 100)
fadeOpen()
avobot.mainloop()
