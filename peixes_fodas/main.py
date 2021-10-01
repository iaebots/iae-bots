#IMPORTS
import os
import requests
import fishManager

#CONSTANTES
#IAE_API_KEY = str(os.environ.get('IAE_PEIXESFODAS_APIKEY'))
#IAE_API_SECRET = str(os.environ.get('IAE_PEIXESFODAS_APISECRET'))
IAE_API_KEY = '6268b910f20ad20e2a0c84608e2f6a15'
IAE_API_SECRET = '8234db0b93f0daa1e1cc8aeb97b5192e'

GOOGLE_API_KEY = str(os.environ.get('GOOGLE_APIKEY'))
GOOGLE_PROJECT_KEY = str(os.environ.get('GOOLE_PROJECTKEY'))

#IaePost
def iaePost(image, conts, fish, API_KEY, API_SECRET):
    if image != []:
        #url = 'https://api.iaebots.com/api/v1/posts'
        url = 'http://localhost:3001/api/v1/posts'
        files = {'media': open(image[0], 'rb')}
        data = {'body': "Peixe foda #" + str(conts[1]) + " - " + fish}
        response = requests.post(url, headers = {'Authorization': 'Token api_key='+API_KEY+' api_secret='+API_SECRET}, files=files, data=data)
        return response

#twitterPost
#def twitterPost():
    #...

#Finding Nemo
def main():
    fm = fishManager.fishManager
    conts = fm.numFishSelector()
    fish = fm.fishSelector(conts[0])
    print(fish)
    image = fm.fishImage(fish, GOOGLE_API_KEY, GOOGLE_PROJECT_KEY)

    response = iaePost(image, conts, fish, IAE_API_KEY, IAE_API_SECRET)
    print(response)
    fm.fishUpdate(conts, response.ok)

if __name__ == "__main__":
    main()
