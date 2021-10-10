
path = 'image/'

class fishManager:
    def __init__(self, data):
        self.data = data

    def numFishSelector():
        #READ CONT FILE
        with open("files/cont","r",encoding="utf8") as f:
            conts = f.readlines()
        f.close()

        conts[0] = int(conts[0])
        conts[1] = int(conts[1])

        return conts

    def fishSelector(numFish):
        #READ FISHES FILE
        with open("files/fishes","r",encoding="utf8") as f:
            fish_r = f.readlines()
        f.close()

        fish = fish_r[numFish]
        fish = str(fish[0:len(fish)-1])

        return fish

    def fishUpdate(conts,response):
        with open("files/cont","w",encoding="utf8") as f:
            f.write(str(conts[0]+1)+'\n')
            if response:
                f.write(str(conts[1]+1))
            else:
                f.write(str(conts[1]))
        f.close()

