import datetime
import requests
import ImageProcessor
import os
import json

def post(data, file):
    url = 'https://api.iaebots.com/api/v1/posts'
    API_KEY = os.environ['CLIMA_API_KEY']
    API_SECRET = os.environ['CLIMA_API_SECRET']
    requests.post(url, headers={'Authorization': 'Token api_key=' +
                  API_KEY + ' api_secret=' + API_SECRET}, data=data, files=file)

def weather_now():
    api_token = os.environ['WEATHER_API_TOKEN']
    url = 'http://apiadvisor.climatempo.com.br/api/v1/weather/locale/6993/current?token={}'.format(
        api_token)
    return requests.get(url).json()


def forecast():
    api_token = os.environ['WEATHER_API_TOKEN']
    url = 'http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/6993/hours/72?token={}'.format(
        api_token)

    response = requests.get(url)
    return json.loads(response.text)


def main():
    hour = datetime.datetime.now().hour

    if hour == 12 or hour == 15 or hour == 19:
        data = weather_now()

        img = ImageProcessor.ImageProcessor(data['data'])
        img.openImage()
        img.drawWeatherNowImage()

        media = {'body': 'Tempo agora'}
        file = {'media': open('output/forecast.png', 'rb')}
        post(media, file)
    else:
        data = forecast()
        img = ImageProcessor.ImageProcessor(data['data'])
        img.openImage()
        img.drawForecastImage()

        media = {'body': 'Previsão do tempo para o dia de hoje'}
        file = {'media': open('output/forecast.png', 'rb')}
        post(media, file)


if __name__ == "__main__":
    main()
