import requests

# get cat's image URL and then download it
def getCatImage():
    response = requests.get('https://thatcopy.pw/catapi/rest/').json()
    image = requests.get(response['url'])
    image_f = open('assets/cat_image.jpg', 'wb')
    image_f.write(image.content)
    image_f.close()

# get a cat's fact
def getCatFact():
    response = requests.get('https://catfact.ninja/fact?max_length=140').json()
    return response['fact']


getCatImage()
fact = getCatFact()

API_KEY = os.environ['CATOLOGER_API_KEY']
API_SECRET = os.environ['CATOLOGER_API_SECRET']

data = {'body': fact}
file = {'media': open('assets/cat_image.jpg', 'rb')}

url = 'https://api.iaebots.com/api/v1/posts'

requests.post(url, headers={'Authorization': 'Token api_key=' +
                            API_KEY + ' api_secret=' + API_SECRET}, data=data, files=file)
