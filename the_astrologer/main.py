import requests
import os

# open signs list file
with open('assets/signs.txt', 'r', encoding='utf8') as f:
    signs_f = f.readlines()
f.close()

# get current sign to be posted
with open('assets/current.txt', 'r', encoding='utf8') as f:
    current = f.readlines()
    current = [int(s) for s in current[0].split() if s.isdigit()]
f.close()

# get emojis
with open('assets/emojis.txt', 'r', encoding='utf8') as f:
    emojis = f.readlines()
f.close()

# update list of current sign
with open('assets/current.txt', 'w', encoding='utf8') as f:
    if current[0] == 11:
        f.write('0')
    else:
        f.write(str(current[0] + 1))
f.close()

# remove \n
sign = signs_f[current[0]]
sign = sign[0:len(sign) - 1]

# remove \n from emoji
emoji = emojis[current[0]]
emoji = emoji[0:len(emoji) - 1]

# bot's api keys
API_KEY = os.environ['ASTROLOGER_API_KEY']
API_SECRET = os.environ['ASTROLOGER_API_SECRET']

# get horoscope for current sign
url = 'https://sameer-kumar-aztro-v1.p.rapidapi.com/'

querystring = {'sign': sign, 'day': 'today'}

headers = {
    'x-rapidapi-key': os.environ['HOROSCOPE_API_KEY'],
    'x-rapidapi-host': 'sameer-kumar-aztro-v1.p.rapidapi.com'
}

horoscope = requests.request(
    'POST', url, headers=headers, params=querystring).json()

# post horoscope on IA-e
url = 'https://api.iaebots.com/api/v1/posts'

data = {
    'body': "Today's horocope for {}: {}. Color: {}. Lucky number: {}. Compatibility: {}."
    .format(sign.capitalize() + ' ' + emoji, horoscope['description'], horoscope['color'],
            horoscope['lucky_number'], horoscope['compatibility'])
}

requests.post(url, data=data,  headers={
              'Authorization': 'Token api_key=' + API_KEY + ' api_secret=' + API_SECRET})
