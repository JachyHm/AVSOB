import data
import soundAPI

typPriorita = {"uziv":1,"Mbus":2,"Rbus":3,"Pbus":4}

class Main():
    def __init__(self):
        self.data = data.Data()
        self.soundAPI = soundAPI.soundAPI(self.data)
        vyhlas = Vyhlas()
        vyhlas.BudePristaveny(self,"Pbus",2,1,"01:25",39,False)
        vyhlas.BudePristaveny(self,"Mbus",1,1,"01:27",14,False)
        vyhlas.BudePristaveny(self,"Rbus",2,1,"01:28",7,False)
        vyhlas.BudePristaveny(self,"Mbus",2,1,"01:35",2,False)

    def vratPoleZastavok(self,trasaID):
        poleZastavok = []
        for zastavka in self.data.trasy[trasaID]:
            poleZastavok.append(zastavka)
        return poleZastavok

class Vyhlas():
    def BudePristaveny(self,objektMain,typ,spolocnost,trasa,odchod,nastupiste,vAJ):
        zahlasSubory = []

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["typ"][typ])
        # typ autobusu

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["dopravcia"][spolocnost])
        # spolocnost

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["smer"])
        # smer

        poleZastavok = objektMain.vratPoleZastavok(trasa)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["pravidelnyOdchod"])
        # pravidelný odchod

        hodiny,minuty = odchod.split(":")
        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # cas odchodu

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["budePristaveny"])
        # bude pristaveny

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["nastupiste"]["k"+str(nastupiste)])
        # nastupiste

        objektMain.soundAPI.pridejHlaseni([zahlasSubory,typPriorita[typ]])
        print(zahlasSubory)

m = Main()
        