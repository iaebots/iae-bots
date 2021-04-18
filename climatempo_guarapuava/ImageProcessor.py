from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import textwrap

# Takes API's data and put them in a png image
class ImageProcessor:
    W, H = (600, 600)

    def __init__(self, data):
        self.temperature = data['temperature']
        self.humidity = data['humidity']
        self.wind = data['wind_velocity']
        self.icon = data['icon']
        self.sensation = data['sensation']
        self.condition = data['condition']

    # open background image
    def openImage(self):
        self.img = Image.open('assets/forecast.png')

    # open icon image
    def openIcon(self, name):
        self.icon = Image.open('assets/{}.png'.format(name))

    # draw texts on image
    def drawImage(self):
        draw = ImageDraw.Draw(self.img)
        carlitoRegular = ImageFont.truetype('Carlito-Regular.ttf', 22)
        carlitoBold = ImageFont.truetype('Carlito-Bold.ttf', 48)
        carlitoBoldSmall = ImageFont.truetype('Carlito-Bold.ttf', 24)

        # draw temperature and feels like temperature
        draw.text((85, 160), '{}°C'.format(self.temperature), (255, 255, 255), font=carlitoBold)
        draw.text((30, 210), 'Sensação Térmica {}°C'.format(self.sensation),
                  (255, 255, 255), font=carlitoBoldSmall)

        # draw humidity and wind velocity
        draw.text((400, 170), 'Umidade {}%'.format(self.humidity),
                  (255, 255, 255), font=carlitoBoldSmall)
        draw.text((420, 200), 'Ventos {}km/h'.format(self.wind),
                  (255, 255, 255), font=carlitoRegular)

        # draw condition
        msg = textwrap.wrap('{}'.format(self.condition), width=30)

        current_h, pad = (self.H) / 2, 10
        for line in msg:
            w, h = draw.textsize(line, font=carlitoBoldSmall)
            draw.text(((self.W - w) / 2, current_h),
                      line, font=carlitoBoldSmall)
            current_h += h + pad

        self.openIcon('{}'.format(self.icon))

        offset = (210, 350)
        self.img.paste(self.icon, offset, self.icon)

        self.img.save('output/forecast.png')
