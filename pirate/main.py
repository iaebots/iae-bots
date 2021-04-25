import requests
import os

# get insult and turn it into a string
response = requests.get('https://pirate.monkeyness.com/api/insult')
insult = str(response.content)
insult = insult[2:]
insult = insult.strip('"')

# bot's api keys
API_KEY = os.environ['PIRATE_API_KEY']
API_SECRET = os.environ['PIRATE_API_SECRET']

url = 'https://api.iaebots.com/api/v1/posts'

data = {'body': insult}

requests.post(url, data=data, headers={
              'Authorization': 'Token api_key=' + API_KEY + ' api_secret=' + API_SECRET})
