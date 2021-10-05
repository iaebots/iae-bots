import requests
from bs4 import BeautifulSoup
import os
API_KEY = str(os.environ.get('IAE_WIKIHALL_APIKEY'))
API_SECRET = str(os.environ.get('IAE_WIKIHALL_APISECRET'))
WIKIHOW = 'https://pt.wikihow.com/Especial:Randomizer'

webpage = requests.get(WIKIHOW).content
soup = BeautifulSoup(webpage,features="html.parser")

article_title = soup.find("meta", property="og:title")
article_url = soup.find("meta", property="og:url")
article_img = soup.find("meta", property="og:image")

article_img_data = requests.get(article_img['content']).content

url = 'https://api.iaebots.com/api/v1/posts'
data = {'body': article_title['content']}
file = {'media': article_img_data}

response = requests.post(url, headers={'Authorization': 'Token api_key=' +
                                        API_KEY + ' api_secret=' + API_SECRET}, data=data, files=file)

print('post:'+str(response)+'-'+article_title['content'])

if response.ok:
  try:
    bot_id = response.json()['data']['bot_id']
    post_id = response.json()['data']['id']
    comment_url = 'https://api.iaebots.com/api/v1/'+str(bot_id)+'/posts/'+str(post_id)+'/comment'
    comment_data = {'body': article_url['content']}
    comment_response = requests.post(comment_url, headers={'Authorization': 'Token api_key=' +
                                          API_KEY + ' api_secret=' + API_SECRET}, data=comment_data)
    print('comment:'+str(comment_response)+'-'+article_url['content'])
  except:
    print('!!comment not created!!')
