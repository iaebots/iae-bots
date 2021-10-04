import requests
import os
import random

# open lyrics list file
with open('lyrics_raul.txt', 'r', encoding='utf8') as f:
    lyrics_raul = f.readlines()
f.close()

with open('lyrics_genivaldo.txt', 'r', encoding='utf8') as f:
    lyrics_genivaldo = f.readlines()
f.close()

# bot's api keys
API_KEY = str(os.environ.get('IAE_RAULGENIVAL_APIKEY'))
API_SECRET = str(os.environ.get('IAE_RAULGENIVAL_APISECRET'))

# post quote on IA-e
url = 'https://api.iaebots.com/api/v1/posts'

choice = random.randrange(1,3)
if choice == 1:
  quote = str(random.choice(lyrics_raul) + random.choice(lyrics_genivaldo))
else:
  quote = str(random.choice(lyrics_genivaldo) + random.choice(lyrics_raul))
print(quote)

data = {
    'body': quote
}

response = requests.post(url, data=data,  headers={
              'Authorization': 'Token api_key=' + API_KEY + ' api_secret=' + API_SECRET})
print(response)