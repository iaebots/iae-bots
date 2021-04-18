import datetime
import requests
import ImageProcessor
import os

def post(data, file):
    url = 'https://api.iaebots.com/api/v1/posts'
    API_KEY = os.environ['CLIMA_API_KEY']
    API_SECRET = os.environ['CLIMA_API_SECRET']
    requests.post(url, headers = {'Authorization': 'Token api_key=' + API_KEY + ' api_secret=' + API_SECRET}, data=data, files=file)

def weather_now():
    api_token = os.environ['WEATHER_API_TOKEN']
    url = 'http://apiadvisor.climatempo.com.br/api/v1/weather/locale/6993/current?token={}'.format(api_token)
    response = requests.get(url)
    return response.json()

def main():
    data = weather_now()

    img = ImageProcessor.ImageProcessor(data['data'])
    img.openImage()
    img.drawImage()

    media = {'body': 'Tempo agora'}
    file = {'media': open('output/forecast.png', 'rb')}
    post(media, file)

if __name__ == "__main__":
    main()
