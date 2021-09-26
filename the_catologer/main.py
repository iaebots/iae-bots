import requests
import os

from requests.models import Response

# save image to disc
def save_image(image):
  image_f = open('assets/cat_image.jpg', 'wb')
  image_f.write(image)
  image_f.close()

# send request to catass
def catass_get_request():
  try:
    response = requests.get('https://cataas.com/cat', timeout=5)
    return response.content if response.status_code == 200 else -1
  except requests.exceptions.Timeout:
    return -1

# send request to catapi
def catapi_get_request():
  try:
    response = requests.get('https://thatcopy.pw/catapi/rest/', timeout=10)
    
    if response.status_code == 200:
      data = response.json()
      return data['url']
    return -1
  except requests.exceptions.Timeout:
    return -1

# get cat's image URL and then download it
# return False if bot API's fails
def getCatImage():
  image = catass_get_request()
  if image != -1:
    save_image(image)
    return True
  
  # Try second API if first fails
  response = catapi_get_request()
  if response != -1:
    r_2 = requests.get(response)
    save_image(r_2.content)
    return True
  
  return False
   
    

# get a cat's fact
def getCatFact():
  response = requests.get('https://catfact.ninja/fact?max_length=140')
  
  if response.status_code == 200:
      try:
        data = response.json()
        return data['fact']
      except Exception:
          return -1
  return -1


image = getCatImage()
fact = getCatFact()

API_KEY = os.environ['CATOLOGER_API_KEY']
API_SECRET = os.environ['CATOLOGER_API_SECRET']

data = {'body': fact} if fact != -1 else None
file = {'media': open('assets/cat_image.jpg', 'rb')}

url = 'https://api.iaebots.com/api/v1/posts'

# does nothing if there's no new image nor fact
if image or fact != -1:
    requests.post(url, headers={'Authorization': 'Token api_key=' +
                                API_KEY + ' api_secret=' + API_SECRET}, data=data, files=file)
