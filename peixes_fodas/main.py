#IMPORTS
import os
import searchImages
import requests
import fishManager
import tweepy

#CONSTANTES

TWITTER_ACCESS_KEY = str(os.environ.get('TWITTER_PEIXESFODAS_ACCESSKEY'))
TWITTER_ACCESS_SECRET = str(os.environ.get('TWITTER_PEIXESFODAS_ACCESSSECRET'))

TWITTER_CONSUMER_KEY = str(os.environ.get('TWITTER_PEIXESFODAS_CONSUMERKEY'))
TWITTER_CONSUMER_SECRET = str(os.environ.get('TWITTER_PEIXESFODAS_CONSUMERSECRET'))

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
def twitterPost(image, status, ACCESS_KEY, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET):
    print(ACCESS_KEY)
    print(ACCESS_SECRET)
    print(CONSUMER_KEY)
    print(CONSUMER_SECRET)
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    filename = 'temp.jpg'
    request = requests.get(image, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as img:
            for chunk in request:
                img.write(chunk)
        try:
            api.update_status_with_media(status=status, filename=filename)
            print('tentativa')
            os.remove(filename)
            return True
        except Exception as e:
            print(e)
            os.remove(filename)   
            return False
    else:
        return False

#Finding Nemo
def main():
    fm = fishManager.fishManager
    conts = fm.numFishSelector()
    fish = fm.fishSelector(conts[0])
    print(fish)
    status = "Peixe foda #" + str(conts[1]) + " - " + fish
    data = {'body': status}
    images = searchImages.get_google_images_data(fish)
    if len(images) == 0:
        fm.fishUpdate(conts, False)
        main()
    for image in images:
        try:
            #responseI = iaePost(image, data, IAE_API_KEY, IAE_API_SECRET)
            responseT = twitterPost(image, status, TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
            print(responseT)
        except:
            continue
        #if responseI.ok and responseT.id:
        if responseT == True:
            #print(responseI)
            print(responseT)
            fm.fishUpdate(conts, True)
            break      

if __name__ == "__main__":
    main()
