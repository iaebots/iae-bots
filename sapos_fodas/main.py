import requests
from bs4 import BeautifulSoup
import os
import csv

API_KEY = str(os.environ.get('IAE_SAPOSFODAS_APIKEY'))
API_SECRET = str(os.environ.get('IAE_SAPOSFODAS_APISECRET'))
CALPHOTOS_URL = 'https://calphotos.berkeley.edu'#/cgi/img_query?enlarge=1111+1111+1111+2648
PHOTOS_URL = CALPHOTOS_URL+'/cgi/img_query?where-taxon='#Alytes+cisternasii

with open('frog_id.txt','r+') as frog_file:
  frog_id = int(frog_file.readlines()[0])
  frog_file.seek(0)
  frog_file.write(str(int(frog_id)+1))
  frog_file.truncate()

with open('frogs.txt') as frogs:
  frogs = csv.reader(frogs, delimiter=',')
  for frog_line in frogs:
    if frogs.line_num == frog_id:
      frog = frog_line

photos_page = requests.get(PHOTOS_URL + frog[0].replace(" ", "+")).content
soup = BeautifulSoup(photos_page,features="html.parser")
table = soup.find('table', {"width":"100%"})
tds = table.findAll('td')

photo_page = requests.get(CALPHOTOS_URL + tds[0].a.get('href')).content
soup = BeautifulSoup(photo_page,features="html.parser")
table = soup.findAll('table', {"align":"center"})
tds = table[1].findAll('td')
image = CALPHOTOS_URL+tds[0].img.get('src')
photo_reference = tds[1].text[:len(tds[1].text)-1]

frog_quote = []
frog_quote.append('Sapo Foda #' + str(frog_id) + ' - ' + str(frog[0]) + ' (' + str(frog[2]) + ')')
if frog[1]:
  frog_quote.append('Nome comum: ' + str(frog[1]))
frog_quote.append('\nImage by ' + photo_reference)
frog_quote = '\n'.join(frog_quote)

frog_image = requests.get(image).content

#url = 'http://0.0.0.0:3001/api/v1/posts'
url = 'https://api.iaebots.com/api/v1/posts'
data = {'body': frog_quote}
file = {'media': frog_image}
response = requests.post(url, headers={'Authorization': 'Token api_key=' +
                                        API_KEY + ' api_secret=' + API_SECRET}, data=data, files=file)
print(response)
print(image)
print(photo_reference)
