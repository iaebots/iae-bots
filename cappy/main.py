import requests
import os
import random

# search key-words in original post's caption
def search_cappy(text):
  i = text.find('#')
  text = text[:i]
  words = ['capybara', 'capivara', 'carpincho', 'capybaras', 'capivaras', 'carpinchos', 'capy', 'cappy']
  while len(words) > 0:
    i = text.find(words[0])
    if i != -1:
      return i
    words.pop(0)
  return -1


# bot's api keys
API_KEY = os.environ['CAPPY_API_KEY']
API_SECRET = os.environ['CAPPY_API_SECRET']

# tags to be searched on Instagram
tags = ['capybara', 'capivara', 'carpincho', 'capybaras', 'capivaras', 'carpinchos']

# select tag randomly
random.shuffle(tags)
tag = tags[0]

query = 'https://www.instagram.com/graphql/query?query_hash=298b92c8d7cad703f7565aa892ede943&variables={"tag_name":"' + tag + '","first":20}'

# add user-agent to avoid 429 from Instagram
header = {
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0"
}

response = requests.get(query, headers=header)

if response.status_code == 200:
  response_data = response.json()
  next_cursor = response_data['data']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
  edges = response_data['data']['hashtag']['edge_hashtag_to_media']['edges']
  random.shuffle(edges)

  for i in edges:
    text = i['node']['edge_media_to_caption']['edges'][0]['node']['text'] # gets caption of post
    if search_cappy(text) != -1:
      display_url = i['node']['display_url'] # if caption contains key-word, get its display_url
      break
  
  image = requests.get(display_url)
  
  if image.status_code == 200:
    url = 'https://api.iaebots.com/api/v1/posts'

    file = {'media': image.content}

    iae_response = requests.post(url, files=file, headers={
              'Authorization': 'Token api_key=' + API_KEY + ' api_secret=' + API_SECRET})
    
    if iae_response.status_code != 201:
      print('IA-e API error: ' + str(iae_response.status_code))
    
  else:
    print('Error while downloading image: ' + str(image.status_code))
else:
  print('Instagram error: ' + str(response.status_code))
