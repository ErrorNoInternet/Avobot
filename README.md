# Avobot

Avobot is a simple chatbot that can chat with you when you're bored. It is made in Python, and has the ability to check the weather, check the time, the date, and much more. 

### Features

- Time and date checking
- Weather for any city
- Basic chatting
- Information database
- Editable ``responses.data`` file
- Random number generator
- Random word generator
- Memory (name and emotions only)
- Emotions (a few responses will change)
- Search results (from Bing)
- Launching anything on your PC

### Upcoming Features

- LAN messaging
- Calculator
- Timers and stopwatches
- Reminders and alarms
- Text-to-speech

# Requirements 

- Python 3.4+ (Built on 3.6.9) 
- Internet connection for searches
- ``pip install BeautifulSoup4``

# How to setup

First, make sure you've done all the requirements and then all you need to do is run the ``Avobot.py`` file (make sure that ``responses.data`` is also in the same folder) and chat with your bot!

# How the chatbot works

Everytime you run the chatbot, it will read from a file called ``responses.data`` and get all the lines from it. It will check if there is ``q#`` in the line, and if it is in the line, it will mark that line as a question. If it is not in the line, it will mark the line as an answer. Whenever you ask the chatbot a question, it will check for all the questions and answers (If you want to add your own, add it at the top of ``responses.data``).

### Libraries

- os (resetting data file)
- re (formatting HTML result)
- time (time and time.sleep)
- random (random responses)
- tkinter (window and messagebox)
- datetime (time and date)
- requests (weather and web search)
- threading (preventing GUI lag)
- BeautifulSoup (processing HTML data)
- subprocess (launching files)
- sys (checking system OS)
- urllib (getting HTML from Bing)
