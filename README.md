# Avobot

What is Avobot? Avobot is a simple chatbot that can chat with you when you're bored. It is made in Python, and has the ability to check the weather, check the time, the date, and much more. 

### Features

- Time and date checking
- Weather for any city
- Basic chatting
- Information database
- Editable ``responses.data`` file

# How to setup

This chatbot requires no Python modules to be installed. All the modules that it uses are already in Python. All you need to do is run the ``Avobot.py`` file (make sure that the `responses.data`` is also in the same folder) and chat with your bot!

# How the chatbot works

Everytime you run the chatbot, it will read from a file called ``responses.data`` and get all the lines from it. It will check if there is ``#q`` in the line, and if it is in the line, it will mark that line as a question. If it is not in the line, it will mark the line as an answer. Whenever you ask the chatbot a question, it will check for all the questions and answers.
