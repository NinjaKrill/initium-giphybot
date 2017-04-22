# Giphybot by NinjaKrill
# Do whatever you want with this, credit appreciated but not required
# Chat is being rewritten soon meaning this will become obsolete
# Enjoy it why you can

from bs4 import BeautifulSoup
import os
import time
import json
import requests
import re
import random

# Settings:
idToken = "default"                         # Chat ID token of the character you want to use
botName = "default"                         # Name of the character you're using, so the bot doesn't filter it's own messages
channel = "GlobalChat"                      # Channel the bot will recieve and send messages in
api_key = "default"                         # Giphy API key, obtain one from https://api.giphy.com/
tsFilename = "giphybot-timestamp.txt"       # Path of the file that the timestamp should be saved in


def sendMessage(channel, message, idToken):
    # Send a message.
    # Acceptable channels are: 
    # - GlobalChat, LocationChat, GroupChat, PartyChat
    url = "https://chat-dot-playinitium.appspot.com/messager"
    payload = {
        'channel' : channel, # Chat channel
        'message' : message, # Message content
        'idToken' : idToken  # Character's unique chat token
    }
    
    r = requests.post(url, params=payload, verify=False)
    input_data = r.text
    try:
        messages = json.loads(input_data)
    except:
        messages = "None"
    return messages;

def getMessages(idToken):
    # Pull messages and convert to Python list.
    print("Setting URL.")
    url = "https://chat-dot-playinitium.appspot.com/messager?&idToken=" + str(idToken)
    print("Pulling latest messages..")
    r = requests.get(url, verify=False)
    input_data = r.text
    messages = json.loads(input_data)
    return messages;

def executeCommand(message):
    # Define commands here
    messageContent = message['message']
    nickname = message['nickname']
    if messageContent.lower().startswith('!giphy'):
        try:
            query = messageContent[7:] # Remove the first 7 characters from the message, including the space ("!giphy ")
            query = re.sub(' ', '+', query)
            print query
            url = "http://api.giphy.com/v1/gifs/search?q="+query+"&api_key="+api_key
            input_data = requests.get(url, verify=False)
            parsed_input = json.loads(input_data.text)
            print parsed_input['data'][0]['url']
            sendMessage(channel, nickname+": [Top giphy result for '"+query+"']("+parsed_input['data'][random.choice([0,1,2,3])]['images']['original']['url']+")", idToken)
            time.sleep(1)
        except:
            sendMessage(channel, nickname+": No results found.", idToken)
            time.sleep(1)

# Check if timestamp file exists
if not os.path.isfile(tsFilename):
    file = open(tsFilename, 'w')
    file.write("0")

# Load timestamp
file = open(tsFilename, 'r')
timestamp = file.read()
lastTimestamp = timestamp
file.close()
print timestamp

while True:
    try:
        file = open(tsFilename, 'r')
        timestamp = file.read()
        lastTimestamp = timestamp
        file.close()
        print timestamp
        parsed_input = getMessages(idToken)
        for message in parsed_input[0]:
            soup = BeautifulSoup(message['message'], 'html.parser')
            if int(message['marker']) > int(timestamp):
                print "New message found."
                lastTimestamp = message['marker']
                time.sleep(1)
                # If message starts with !, it means it is a command.
                if message['message'].lower().startswith('!'):
                    print("Returned: !")
                    executeCommand(message)
                    break
        file = open(tsFilename, 'w')
        file.write(str(lastTimestamp))

    except:
        "Polling failed, retrying..."
