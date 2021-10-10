#IMPORTS
import os
import searchImages
import requests
import fishManager

#CONSTANTES
IAE_API_KEY = str(os.environ.get('IAE_PEIXESFODAS_APIKEY'))
IAE_API_SECRET = str(os.environ.get('IAE_PEIXESFODAS_APISECRET'))
URL = 'https://api.iaebots.com/api/v1/posts'
#URL = 'http://localhost:3001/api/v1/posts'

#IaePost
def iaePost(image, data, API_KEY, API_SECRET):
        image = requests.get(image).content
        files = {'media': image}
        response = requests.post(URL, headers = {'Authorization': 'Token api_key='+API_KEY+' api_secret='+API_SECRET}, files=files, data=data)
        return response

#TwitterPost
#def twitterPost():
    #...

#Finding Nemo
def main():
    fm = fishManager.fishManager
    conts = fm.numFishSelector()
    fish = fm.fishSelector(conts[0])
    print(fish)
    data = {'body': "Peixe foda #" + str(conts[1]) + " - " + fish}
    images = searchImages.get_google_images_data(fish)
    if len(images) == 0:
        fm.fishUpdate(conts, False)
        main()
    for image in images:
        try:
            response = iaePost(image, data, IAE_API_KEY, IAE_API_SECRET)
        except:
            continue
        if response.ok:
            print(response)
            fm.fishUpdate(conts, response.ok)
            break      

if __name__ == "__main__":
    main()
