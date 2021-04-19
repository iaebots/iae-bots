from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from datetime import datetime, timedelta
import textwrap

# Use API's data and turn them into a png image

class ImageProcessor:
    W, H = (600, 600)
    carlitoRegular = ImageFont.truetype('Carlito-Regular.ttf', 22)
    carlitoBold = ImageFont.truetype('Carlito-Bold.ttf', 48)
    carlitoBoldSmall = ImageFont.truetype('Carlito-Bold.ttf', 24)

    def __init__(self, data):
        self.data = data

    # open background image
    def openImage(self):
        self.img = Image.open('assets/forecast.png')

    # open icon image
    def openIcon(self, name):
        self.icon = Image.open('assets/{}.png'.format(name))

    # fetch data from API's response that will be used for weather_now report
    def weatherNowData(self):
        self.temperature = self.data['temperature']
        self.humidity = self.data['humidity']
        self.wind = self.data['wind_velocity']
        self.icon = self.data['icon']
        self.sensation = self.data['sensation']
        self.condition = self.data['condition']

    # round hour to closest hour
    def hour_rounder(self, t):
        return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
                + timedelta(hours=t.minute // 30))

    # find index of wished forecast from API's response given it's date and hour
    def find(self, time):
        j = 0
        for i in self.data:
            if i['date'] == time:
                break
            j += 1
        return j

    # get forecast for morning at 8am, afternoon at 3pm and evening at 9pm
    def forecastData(self):
        morning = self.hour_rounder(
            datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        afternoon = self.hour_rounder(
            (datetime.now() + timedelta(hours=6))).strftime("%Y-%m-%d %H:%M:%S")
        evening = self.hour_rounder(
            (datetime.now() + timedelta(hours=12))).strftime("%Y-%m-%d %H:%M:%S")

        j = self.find(morning)
        self.m_temperature = self.data[j]['temperature']['temperature']
        self.m_precipitation = self.data[j]['rain']['precipitation']
        self.m_wind = self.data[j]['wind']['velocity']
        self.m_humidity = self.data[j]['humidity']['humidity']

        j = self.find(afternoon)
        self.a_temperature = self.data[j]['temperature']['temperature']
        self.a_precipitation = self.data[j]['rain']['precipitation']
        self.a_wind = self.data[j]['wind']['velocity']
        self.a_humidity = self.data[j]['humidity']['humidity']

        j = self.find(evening)
        self.e_temperature = self.data[j]['temperature']['temperature']
        self.e_precipitation = self.data[j]['rain']['precipitation']
        self.e_wind = self.data[j]['wind']['velocity']
        self.e_humidity = self.data[j]['humidity']['humidity']

    # draw texts on image
    def drawWeatherNowImage(self):
        draw = ImageDraw.Draw(self.img)

        self.weatherNowData()

        # draw temperature and feels like temperature
        draw.text((85, 160), '{}°C'.format(self.temperature),
                  (255, 255, 255), font=self.carlitoBold)
        draw.text((30, 210), 'Sensação Térmica {}°C'.format(self.sensation),
                  (255, 255, 255), font=self.carlitoBoldSmall)

        # draw humidity and wind velocity
        draw.text((400, 170), 'Umidade {}%'.format(self.humidity),
                  (255, 255, 255), font=self.carlitoBoldSmall)
        draw.text((400, 200), 'Ventos {}km/h'.format(self.wind),
                  (255, 255, 255), font=self.carlitoRegular)

        # draw condition
        msg = textwrap.wrap('{}'.format(self.condition), width=30)

        current_h, pad = (self.H) / 2, 10
        for line in msg:
            w, h = draw.textsize(line, font=self.carlitoBoldSmall)
            draw.text(((self.W - w) / 2, current_h),
                      line, font=self.carlitoBoldSmall)
            current_h += h + pad

        self.openIcon('{}'.format(self.icon))

        offset = (210, 350)
        self.img.paste(self.icon, offset, self.icon)

        self.img.save('output/forecast.png')

    # draw weather forecast for morning, afternoon and evening
    def drawForecastImage(self):
        draw = ImageDraw.Draw(self.img)

        self.forecastData()

        draw.text((20, 160), 'Manhã', font=self.carlitoBold)
        draw.text((250, 160), 'Tarde', font=self.carlitoBold)
        draw.text((460, 160), 'Noite', font=self.carlitoBold)

        # draw temperature and precipitation for moning
        draw.text((50, 230), '{}°C'.format(self.m_temperature),
                  (255, 255, 255), font=self.carlitoBold)
        draw.text((20, 300), 'Precipitação {}%'.format(self.m_precipitation),
                  (255, 255, 255), font=self.carlitoBoldSmall)

        # draw humidity and wind velocity for morning
        draw.text((20, 360), 'Umidade {}%'.format(self.m_humidity),
                  (255, 255, 255), font=self.carlitoBoldSmall)
        draw.text((20, 420), 'Ventos {}km/h'.format(self.m_wind),
                  (255, 255, 255), font=self.carlitoRegular)

        # draw temperature and precipitation for afternoon
        draw.text((260, 230), '{}°C'.format(self.a_temperature),
                  (255, 255, 255), font=self.carlitoBold)
        draw.text((230, 300), 'Precipitação {}%'.format(self.a_precipitation),
                  (255, 255, 255), font=self.carlitoBoldSmall)

        # draw humidity and wind velocity for afternoon
        draw.text((230, 360), 'Umidade {}%'.format(self.a_humidity),
                  (255, 255, 255), font=self.carlitoBoldSmall)
        draw.text((230, 420), 'Ventos {}km/h'.format(self.a_wind),
                  (255, 255, 255), font=self.carlitoRegular)

        # draw temperature and precipitation for evening
        draw.text((480, 230), '{}°C'.format(self.e_temperature),
                  (255, 255, 255), font=self.carlitoBold)
        draw.text((430, 300), 'Precipitação {}%'.format(self.e_precipitation),
                  (255, 255, 255), font=self.carlitoBoldSmall)

        # draw humidity and wind velocity for evening
        draw.text((430, 360), 'Umidade {}%'.format(self.e_humidity),
                  (255, 255, 255), font=self.carlitoBoldSmall)
        draw.text((430, 420), 'Ventos {}km/h'.format(self.e_wind),
                  (255, 255, 255), font=self.carlitoRegular)

        self.img.save('output/forecast.png')
