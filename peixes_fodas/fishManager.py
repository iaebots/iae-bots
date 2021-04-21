import os
import shutil
from google_images_search import GoogleImagesSearch

path = 'image/'

class fishManager:
    def __init__(self, data):
        self.data = data

    def numFishSelector():
        #READ CONT FILE
        with open("files/cont.txt","r",encoding="utf8") as f:
            conts = f.readlines()
        f.close()

        conts[0] = int(conts[0])
        conts[1] = int(conts[1])

        return conts


    def fishSelector(numFish):
        #READ FISHES FILE
        with open("files/fishes.txt","r",encoding="utf8") as f:
            fish_r = f.readlines()
        f.close()

        fish = fish_r[numFish]
        fish = str(fish[0:len(fish)-1]) + " peixe"

        return fish

    def fishImage(query, API_KEY, PROJECT_KEY):
        #QUERY SEARCH
        gis = GoogleImagesSearch(API_KEY, PROJECT_KEY)
        _search_params = {
            'q': query,
            'num': 1,
            'searchType': 'image',
            'safe': 'off',
            'imgType': 'photo',
            'fileType': 'jpg',
            'orTerms': 'peixe|fish|pesca|pescaria|rio|isca|nadando|nadar|água|mar|anzol'
        }

        #limit google API request in 5
        i = 0
        images = []
        gis.search(search_params=_search_params, path_to_dir = path)
        while gis.results() == [] and i < 5:
            try:
                gis.next_page()
            except:
                print('page '+i+' nothing found')
            i=i+1

        if os.path.exists(path):
            filename = os.listdir(path)
            os.rename(path + filename[0], path + 'post.jpg')

        if os.path.exists(path+'post.jpg'):
            images.append(path + 'post.jpg')

        return images


    def fishUpdate(conts,response):
        with open("files/cont.txt","w",encoding="utf8") as f:
            f.write(str(conts[0]+1)+'\n')
            if response:
                f.write(str(conts[1]+1))
            else:
                f.write(str(conts[1]))
        f.close()

        if os.path.exists(path+'1.jpg'):
            os.remove(path + '1.jpg')

        if os.path.exists(path):
            shutil.rmtree(path)
