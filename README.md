# initium-giphybot
Simple, efficient chatbot for Initium written in Python using Requests.

## Dependancies
* Python 2.7
* Requests
* BeautifulSoup

## Configuration

I'm too lazy to make the bot import from a config file. You can configure the bot from within the script.

`idToken = "default"                         # Chat ID token of the character you want to use`

`botName = "default"                         # Name of the character you're using, so the bot doesn't filter it's own messages`

`channel = "GlobalChat"                      # Channel the bot will recieve and send messages in`

`api_key = "default"                         # Giphy API key, obtain one from https://api.giphy.com/`

`tsFilename = "giphybot-timestamp.txt"       # Path of the file that the timestamp should be saved in`
