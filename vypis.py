import time

class Vypis():
    def nastavVypis(self,level):
        self.levelVypis = level

    def vypis(self,zprava,level=1,konec=False):
        if level <= self.levelVypis:
            levelSlovnik = {1:"INFO: ",2:"DEBUG: "}
            if not konec:
                print(time.strftime("%H:%M:%S ")+levelSlovnik[level]+str(zprava))
            else:
                input(time.strftime("%H:%M:%S ")+levelSlovnik[level]+str(zprava))