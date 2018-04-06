import data
import soundAPI
import win32serviceutil, win32service
import win32event
import win32evtlogutil
import win32evtlog
import servicemanager
import sys
import vypis
import signal
import time
from datetime import datetime
import Pyro4

typPriorita = {"uziv":1,"Mbus":2,"Rbus":3,"Pbus":4}
vyhlasXminPred = 15
vyhlasXminPredDruhy = 7
prichadzaVyhlasXminPred = 3
hnedOdideLimit = 0

class Main():
    def __init__(self):
        self.vypis = vypis.Vypis()
        self.vypis.nastavVypis(2)
        self.data = data.Data()
        self.soundAPI = soundAPI.soundAPI(self.data)
        self.vyhlas = Vyhlas()
        self.vypis.vypis('Inicializacia aplikacie!',1)
        self.soundAPI.vyhlas(["hlas/SK/start.wav",self.data.poleHlasenie["SK"]["stanice_umisteni"]])

    def beh(self, 
            # objektSluzby
            ):
        # self.vyhlas.BudePristaveny(self,"Mbus",2,19,"19:43",13,False)
        # self.vyhlas.BudePristaveny(self,"Mbus",2,19,"19:43",13,False,True)
        # self.vyhlas.Stoji(self,"Mbus",2,1,19,"19:43",13,False)
        # self.vyhlas.Stoji(self,"Mbus",2,1,19,"19:43",13,False,True)
        # self.vyhlas.OdidePriNast(self,"Mbus",2,19,"19:43",13,False)
        # self.vyhlas.OdidePriNast(self,"Mbus",2,19,"19:43",13,False,True)
        # self.vyhlas.PrideTranzitny(self,"Mbus",2,1,19,"19:41","19:43",13,False)
        # self.vyhlas.PrideTranzitny(self,"Mbus",2,1,19,"19:41","19:43",13,False,True)
        # self.vyhlas.PrichadzaTranzitny(self,"Mbus",2,1,19,"19:41","19:43",13,False)
        # self.vyhlas.PrichadzaTranzitny(self,"Mbus",2,1,19,"19:41","19:43",13,False,True)
        # self.vyhlas.PrisielTranzitny(self,"Mbus",2,1,19,"19:41","19:43",13,False,False,False)
        # self.vyhlas.PrisielTranzitny(self,"Mbus",2,1,19,"19:41","19:43",13,False,True,False)
        # self.vyhlas.PrisielTranzitny(self,"Mbus",2,1,19,"19:41","19:43",13,False,False,True)
        # self.vyhlas.PrisielTranzitny(self,"Mbus",2,1,19,"19:41","19:43",13,False,True,True)
        # self.vyhlas.PrideKonciaci(self,"Mbus",2,1,"19:43",13,False)
        # self.vyhlas.PrideKonciaci(self,"Mbus",2,1,"19:43",13,False,True)
        # self.vyhlas.PrichadzaKonciaci(self,"Mbus",2,1,13,False)
        # self.vyhlas.PrichadzaKonciaci(self,"Mbus",2,1,13,False,True)
        # self.vyhlas.PrisielKonciaci(self,"Mbus",2,1,"19:41",13,False)
        # self.vyhlas.PrisielKonciaci(self,"Mbus",2,1,"19:41",13,False,True)
        while True:

            #----------CASY---------
            #aktualny cas
            localtime = time.localtime(time.time())
            denVTydnu = str(localtime.tm_wday)
            datum = str(localtime.tm_mday)+"."+str(localtime.tm_mon)+"."+str(localtime.tm_year)

            casMM = str(localtime.tm_min)
            while len(casMM) < 2:
                casMM = "0"+casMM

            casHH = str(localtime.tm_hour)
            while len(casHH) < 2:
                casHH = "0"+casHH
                
            cas = casHH+":"+casMM

            #aktualny cas - predstih hlasenie "pride"
            localtimePride = time.localtime(time.time()+vyhlasXminPred*60)

            casPrideMM = str(localtimePride.tm_min)
            while len(casPrideMM) < 2:
                casPrideMM = "0"+casPrideMM

            casPrideHH = str(localtimePride.tm_hour)
            while len(casPrideHH) < 2:
                casPrideHH = "0"+casPrideHH

            casPride = casPrideHH+":"+casPrideMM

            #aktualny cas - predstih hlasenie "zkraceny pride"
            localtimePrideDruhy = time.localtime(time.time()+vyhlasXminPredDruhy*60)

            casPrideDruhyMM = str(localtimePrideDruhy.tm_min)
            while len(casPrideDruhyMM) < 2:
                casPrideDruhyMM = "0"+casPrideDruhyMM

            casPrideDruhyHH = str(localtimePrideDruhy.tm_hour)
            while len(casPrideDruhyHH) < 2:
                casPrideDruhyHH = "0"+casPrideDruhyHH
                
            casPrideDruhy = casPrideDruhyHH+":"+casPrideDruhyMM

            #aktualny cas - predstih hlasenie "prichadza"
            localtimePrichadza = time.localtime(time.time()+prichadzaVyhlasXminPred*60)

            casPrichadzaMM = str(localtimePrichadza.tm_min)
            while len(casPrichadzaMM) < 2:
                casPrichadzaMM = "0"+casPrichadzaMM

            casPrichadzaHH = str(localtimePrichadza.tm_hour)
            while len(casPrichadzaHH) < 2:
                casPrichadzaHH = "0"+casPrichadzaHH
                
            casPrichadza = casPrichadzaHH+":"+casPrichadzaMM

            
            #----------VYHLASOVANIE PRICHODOV---------

            #pole prichodzich spoju k vyhlaseni
            vyhlasPrich = self.data.spojeDlaCasuPrichPride.pop(casPride,[])

            #pocetSpojuKVyhlaseni
            pocetSpojuPrich = len(vyhlasPrich)

            #vyhlasovani prichozich spoju
            for spoj in vyhlasPrich:
                spoj = self.data.spoje[spoj]

                #zisti, ci dnes spoj ide
                jedeDnes = False
                try:
                    self.data.datumy[spoj["IDplatnosti"]]["obecnaPlatnost"].index(denVTydnu)
                except:
                    try:
                        self.data.datumy[spoj["IDplatnosti"]]["jedeTake"].index(datum)
                    except:
                        pass
                    else:
                        jedeDnes = True
                else:
                    try:
                        self.data.datumy[spoj["IDplatnosti"]]["nejede"].index(datum)
                    except:
                        jedeDnes = True
                    else:
                        pass

                #pokial ano,
                if jedeDnes:
                    #pokial konci hlas konciaci
                    if spoj["konci"]:
                        #pokial je vela hlasenia vo fronte, alebo je naraz viac ako 5 hlaseni, hlas iba zkratene
                        if self.soundAPI.vratFrontuHlaseni() > 5 or pocetSpojuPrich > 5:
                            zkracene = True
                        else:
                            zkracene = False

                        self.vyhlas.PrideKonciaci(self,spoj["typ"],spoj["IDdopravca"],spoj["IDtrasyPrichod"],spoj["casPrichodu"],spoj["nastupiste"],spoj["hlasEN"],zkracene)
                    #pokial nekonci, hlas tranzitny
                    else:
                        #pokial je vela hlasenia vo fronte, alebo je naraz viac ako 5 hlaseni, hlas iba zkratene
                        if self.soundAPI.vratFrontuHlaseni() > 5 or pocetSpojuPrich > 5:
                            zkracene = True
                        else:
                            zkracene = False

                        self.vyhlas.PrideTranzitny(self,spoj["typ"],spoj["IDdopravca"],spoj["IDtrasyPrichod"],spoj["IDtrasyOdchod"],spoj["casPrichodu"],spoj["casOdchodu"],spoj["nastupiste"],spoj["hlasEN"],zkracene)


            #pole prichodzich spoju k vyhlaseni podruhe
            vyhlasPrichDruhy = self.data.spojeDlaCasuPrichPrideDruhy.pop(casPrideDruhy,[])

            #vyhlasovani prichozich spoju podruhe
            for spoj in vyhlasPrichDruhy:
                spoj = self.data.spoje[spoj]
                zkracene = True

                #zisti, ci dnes spoj ide
                jedeDnes = False
                try:
                    self.data.datumy[spoj["IDplatnosti"]]["obecnaPlatnost"].index(denVTydnu)
                except:
                    try:
                        self.data.datumy[spoj["IDplatnosti"]]["jedeTake"].index(datum)
                    except:
                        pass
                    else:
                        jedeDnes = True
                else:
                    try:
                        self.data.datumy[spoj["IDplatnosti"]]["nejede"].index(datum)
                    except:
                        jedeDnes = True
                    else:
                        pass

                #pokial ano,
                if jedeDnes:

                    #pokial konci hlas konciaci
                    if spoj["konci"]:
                        self.vyhlas.PrideKonciaci(self,spoj["typ"],spoj["IDdopravca"],spoj["IDtrasyPrichod"],spoj["casPrichodu"],spoj["nastupiste"],spoj["hlasEN"],zkracene)
                    #pokial nekonci
                    else:
                        self.vyhlas.PrideTranzitny(self,spoj["typ"],spoj["IDdopravca"],spoj["IDtrasyPrichod"],spoj["IDtrasyOdchod"],spoj["casPrichodu"],spoj["casOdchodu"],spoj["nastupiste"],spoj["hlasEN"],zkracene)


            #pole prichadza spoju k vyhlaseni
            vyhlasPrichadza = self.data.spojeDlaCasuPrichPrichadza.pop(casPrichadza,[])

            #pocetSpojuKVyhlaseni
            pocetSpojuPrichadza = len(vyhlasPrichadza)

            #vyhlasovani prichadza spoju
            for spoj in vyhlasPrichadza:
                spoj = self.data.spoje[spoj]

                #zisti, ci dnes spoj ide
                jedeDnes = False
                try:
                    self.data.datumy[spoj["IDplatnosti"]]["obecnaPlatnost"].index(denVTydnu)
                except:
                    try:
                        self.data.datumy[spoj["IDplatnosti"]]["jedeTake"].index(datum)
                    except:
                        pass
                    else:
                        jedeDnes = True
                else:
                    try:
                        self.data.datumy[spoj["IDplatnosti"]]["nejede"].index(datum)
                    except:
                        jedeDnes = True
                    else:
                        pass

                #pokial ano,
                if jedeDnes:
                    #pokial konci hlas konciaci
                    if spoj["konci"]:
                        #pokial je vela hlasenia vo fronte, alebo je naraz viac ako 5 hlaseni, hlas iba zkratene
                        if self.soundAPI.vratFrontuHlaseni() > 5 or pocetSpojuPrichadza > 5:
                            zkracene = True
                        else:
                            zkracene = False

                        self.vyhlas.PrichadzaKonciaci(self,spoj["typ"],spoj["IDdopravca"],spoj["IDtrasyPrichod"],spoj["nastupiste"],spoj["hlasEN"],zkracene)
                    #pokial nekonci, hlas tranzitny
                    else:
                        #pokial je vela hlasenia vo fronte, alebo je naraz viac ako 5 hlaseni, hlas iba zkratene
                        if self.soundAPI.vratFrontuHlaseni() > 5 or pocetSpojuPrichadza > 5:
                            zkracene = True
                        else:
                            zkracene = False

                        self.vyhlas.PrichadzaTranzitny(self,spoj["typ"],spoj["IDdopravca"],spoj["IDtrasyPrichod"],spoj["IDtrasyOdchod"],spoj["casPrichodu"],spoj["casOdchodu"],spoj["nastupiste"],spoj["hlasEN"],zkracene)


            #pole prisel spoju k vyhlaseni
            vyhlasPrisel = self.data.spojeDlaCasuPrichPrisiel.pop(cas,[])

            #pocetSpojuKVyhlaseni
            pocetSpojuPrisel = len(vyhlasPrisel)

            #vyhlasovani prisiel spoju
            for spoj in vyhlasPrisel:
                spoj = self.data.spoje[spoj]

                #zisti, ci dnes spoj ide
                jedeDnes = False
                try:
                    self.data.datumy[spoj["IDplatnosti"]]["obecnaPlatnost"].index(denVTydnu)
                except:
                    try:
                        self.data.datumy[spoj["IDplatnosti"]]["jedeTake"].index(datum)
                    except:
                        pass
                    else:
                        jedeDnes = True
                else:
                    try:
                        self.data.datumy[spoj["IDplatnosti"]]["nejede"].index(datum)
                    except:
                        jedeDnes = True
                    else:
                        pass

                #pokial ano,
                if jedeDnes:
                    #pokial konci hlas konciaci
                    if spoj["konci"]:
                        #pokial je vela hlasenia vo fronte, alebo je naraz viac ako 5 hlaseni, hlas iba zkratene
                        if self.soundAPI.vratFrontuHlaseni() > 5 or pocetSpojuPrisel > 5:
                            zkracene = True
                        else:
                            zkracene = False

                        self.vyhlas.PrisielKonciaci(self,spoj["typ"],spoj["IDdopravca"],spoj["IDtrasyPrichod"],spoj["casPrichodu"],spoj["nastupiste"],spoj["hlasEN"],zkracene)
                    #pokial nekonci, hlas tranzitny
                    else:
                        #pokial je vela hlasenia vo fronte, alebo je naraz viac ako 5 hlaseni, hlas iba zkratene
                        if self.soundAPI.vratFrontuHlaseni() > 5 or pocetSpojuPrisel > 5:
                            zkracene = True
                        else:
                            zkracene = False

                        #pokial je rozdil mensej ako nastaveny v hlavicke, vyhlas "hned odide"
                        s1 = spoj["casPrichodu"]
                        s2 = spoj["casOdchodu"]
                        TEMPLATE = '%H:%M'

                        rozdil = datetime.strptime(s2, TEMPLATE) - datetime.strptime(s1, TEMPLATE)

                        if rozdil <= hnedOdideLimit:
                            hnedOdide = True
                        else:
                            hnedOdide = False


                        self.vyhlas.PrisielTranzitny(self,spoj["typ"],spoj["IDdopravca"],spoj["IDtrasyPrichod"],spoj["IDtrasyOdchod"],spoj["casPrichodu"],spoj["casOdchodu"],spoj["nastupiste"],spoj["hlasEN"],zkracene,hnedOdide)


            #----------VYHLASOVANIE PRISTAVENIE---------

            #pole pristavovanych spoju k vyhlaseni
            vyhlasBudePristaveny = self.data.spojeDlaCasuOdchBudePristaveny.pop(casPride,[])

            #pocetSpojuKVyhlaseni
            pocetSpojuBudePristaveny = len(vyhlasBudePristaveny)

            #vyhlasovani pristavovanych spoju
            for spoj in vyhlasBudePristaveny:
                spoj = self.data.spoje[spoj]

                #zisti, ci dnes spoj ide
                jedeDnes = False
                try:
                    self.data.datumy[spoj["IDplatnosti"]]["obecnaPlatnost"].index(denVTydnu)
                except:
                    try:
                        self.data.datumy[spoj["IDplatnosti"]]["jedeTake"].index(datum)
                    except:
                        pass
                    else:
                        jedeDnes = True
                else:
                    try:
                        self.data.datumy[spoj["IDplatnosti"]]["nejede"].index(datum)
                    except:
                        jedeDnes = True
                    else:
                        pass

                #pokial ano,
                if jedeDnes:
                    #a je vela hlasenia vo fronte, alebo je naraz viac ako 5 hlaseni, hlas iba zkratene
                    if self.soundAPI.vratFrontuHlaseni() > 5 or pocetSpojuBudePristaveny > 5:
                        zkracene = True
                    #inak hlas plnu verziu
                    else:
                        zkracene = False

                    self.vyhlas.BudePristaveny(self,spoj["typ"],spoj["IDdopravca"],spoj["IDtrasyOdchod"],spoj["casOdchodu"],spoj["nastupiste"],spoj["hlasEN"],zkracene)


            #pole pristavovanych spoju k vyhlaseni podruhe
            vyhlasBudePristavenyDruhy = self.data.spojeDlaCasuOdchBudePristavenyDruhe.pop(casPrideDruhy,[])

            #vyhlasovani pristavovanych spoju podruhe
            for spoj in vyhlasBudePristavenyDruhy:
                spoj = self.data.spoje[spoj]
                zkracene = True

                #zisti, ci dnes spoj ide
                jedeDnes = False
                try:
                    self.data.datumy[spoj["IDplatnosti"]]["obecnaPlatnost"].index(denVTydnu)
                except:
                    try:
                        self.data.datumy[spoj["IDplatnosti"]]["jedeTake"].index(datum)
                    except:
                        pass
                    else:
                        jedeDnes = True
                else:
                    try:
                        self.data.datumy[spoj["IDplatnosti"]]["nejede"].index(datum)
                    except:
                        jedeDnes = True
                    else:
                        pass

                #pokial ano, vyhlas
                if jedeDnes:
                    self.vyhlas.BudePristaveny(self,spoj["typ"],spoj["IDdopravca"],spoj["IDtrasyOdchod"],spoj["casOdchodu"],spoj["nastupiste"],spoj["hlasEN"],zkracene)


            # if objektSluzby.stop:
            #     break

    def vratPoleZastavok(self,trasaID,zkraceny=False,prichodova=False):
        if zkraceny:
            if prichodova:
                return([self.data.trasy[trasaID][0]])
            else:
                return([self.data.trasy[trasaID][-1]])            
        else:
            poleZastavok = []
            for zastavka in self.data.trasy[trasaID]:
                poleZastavok.append(zastavka)
            return poleZastavok

class Vyhlas():
    def BudePristaveny(self,objektMain,typ,spolocnost,trasa,odchod,nastupiste,vAJ,zkraceny=False):
        zahlasSubory = []

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["typ"][typ])
        # typ autobusu

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["dopravcia"][spolocnost])
        # spolocnost

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["smer"])
        # smer

        poleZastavok = objektMain.vratPoleZastavok(trasa,zkraceny)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["pravidelnyOdchod"])
        # pravidelny odchod

        hodiny,minuty = odchod.split(":")
        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # cas odchodu

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["budePristaveny"])
        # bude pristaveny

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["nastupiste"]["k"+str(nastupiste)])
        # nastupiste

        objektMain.soundAPI.pridejHlaseni([zahlasSubory,typPriorita[typ]])

    def Stoji(self,objektMain,typ,spolocnost,trasaPrichod,trasaOdchod,odchod,nastupiste,vAJ,zkraceny=False):
        zahlasSubory = []

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["typ"][typ])
        # typ autobusu

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["dopravcia"][spolocnost])
        # spolocnost

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["smer"])
        # smer

        poleZastavok = objektMain.vratPoleZastavok(trasaPrichod,zkraceny)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky odchod

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["pravidelnyOdchod"])
        # pravidelny odchod

        hodiny,minuty = odchod.split(":")
        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # cas odchodu

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["budePristaveny"])
        # bude pristaveny

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["nastupiste"]["k"+str(nastupiste)])
        # nastupiste

        objektMain.soundAPI.pridejHlaseni([zahlasSubory,typPriorita[typ]])

    def OdidePriNast(self,objektMain,typ,spolocnost,trasa,odchod,nastupiste,vAJ,zkraceny=False):
        zahlasSubory = []

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["typ"][typ])
        # typ autobusu

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["dopravcia"][spolocnost])
        # spolocnost

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["smer"])
        # smer

        poleZastavok = objektMain.vratPoleZastavok(trasa,zkraceny)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["pravidelnyOdchod"])
        # pravidelny odchod

        hodiny,minuty = odchod.split(":")
        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # cas odchodu

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["stoji"])
        # "stoji"

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["nastupiste"]["na"+str(nastupiste)])
        # nastupiste

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["typ"]["Pbus"])
        # "autobus"

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["pripravenyOdchod"])
        # "je pripraveny na odchod"

        objektMain.soundAPI.pridejHlaseni([zahlasSubory,typPriorita[typ]])

    def PrideTranzitny(self,objektMain,typ,spolocnost,trasaPrichod,trasaOdchod,prichod,odchod,nastupiste,vAJ,zkraceny=False):
        zahlasSubory = []

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["typ"][typ])
        # typ autobusu

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["dopravcia"][spolocnost])
        # spolocnost

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["zoSmeru"])
        # zo smeru

        poleZastavok = objektMain.vratPoleZastavok(trasaPrichod,zkraceny,True)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["pravidelnyPrichod"])
        # pravidelny prichod

        hodiny,minuty = prichod.split(":")
        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # cas prichodu

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["ktoryDalejPokracuje"])
        # ktory dalej pokracuje smer

        poleZastavok = objektMain.vratPoleZastavok(trasaOdchod,zkraceny)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["pravidelnyOdchod"])
        # pravidelny odchod

        hodiny,minuty = odchod.split(":")
        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # cas odchodu

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["pride"])
        # "pride"

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["nastupiste"]["k"+str(nastupiste)])
        # nastupiste

        objektMain.soundAPI.pridejHlaseni([zahlasSubory,typPriorita[typ]])

    def PrichadzaTranzitny(self,objektMain,typ,spolocnost,trasaPrichod,trasaOdchod,prichod,odchod,nastupiste,vAJ,zkraceny=False):
        zahlasSubory = []

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["typ"][typ])
        # typ autobusu

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["dopravcia"][spolocnost])
        # spolocnost

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["zoSmeru"])
        # zo smeru

        poleZastavok = objektMain.vratPoleZastavok(trasaPrichod,zkraceny,True)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["pravidelnyPrichod"])
        # pravidelny prichod

        hodiny,minuty = prichod.split(":")
        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # cas prichodu

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["ktoryDalejPokracuje"])
        # ktory dalej pokracuje smer

        poleZastavok = objektMain.vratPoleZastavok(trasaOdchod,zkraceny)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky

        # zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["pravidelnyOdchod"])
        # # pravidelny odchod

        # hodiny,minuty = odchod.split(":")
        # zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        # zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # # cas odchodu

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["prichadza"])
        # "prichadza"

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["nastupiste"]["k"+str(nastupiste)])
        # nastupiste

        objektMain.soundAPI.pridejHlaseni([zahlasSubory,typPriorita[typ]])

    def PrisielTranzitny(self,objektMain,typ,spolocnost,trasaPrichod,trasaOdchod,prichod,odchod,nastupiste,vAJ,zkraceny=False,hnedOdide=False):
        zahlasSubory = []

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice_umisteni"])
        #stanice

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["typ"][typ])
        # typ autobusu

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["dopravcia"][spolocnost])
        # spolocnost

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["zoSmeru"])
        # zo smeru

        poleZastavok = objektMain.vratPoleZastavok(trasaPrichod,zkraceny,True)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["prisiel"])
        # "prisiel"

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["nastupiste"]["k"+str(nastupiste)])
        # nastupiste

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["typ"]["Pbus"])
        # "autobus"

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["dalejPokracuje"])
        # dalej pokracuje smer

        poleZastavok = objektMain.vratPoleZastavok(trasaOdchod,zkraceny)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["pravidelnyOdchod"])
        # pravidelny odchod

        hodiny,minuty = odchod.split(":")
        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # cas odchodu

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["nastupiste"]["na"+str(nastupiste)])
        # nastupiste

        if hnedOdide:
            zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["typ"]["Pbus"])
            # "autobus"

            zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["pripravenyOdchod"])
            # "je pripraveny na odchod"

        objektMain.soundAPI.pridejHlaseni([zahlasSubory,typPriorita[typ]])

    def PrideKonciaci(self,objektMain,typ,spolocnost,trasaPrichod,prichod,nastupiste,vAJ,zkraceny=False):
        zahlasSubory = []

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["typ"][typ])
        # typ autobusu

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["dopravcia"][spolocnost])
        # spolocnost

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["zoSmeru"])
        # zo smeru

        poleZastavok = objektMain.vratPoleZastavok(trasaPrichod,zkraceny,True)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["pravidelnyPrichod"])
        # pravidelny prichod

        hodiny,minuty = prichod.split(":")
        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # cas prichodu

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["pride"])
        # "pride"

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["nastupiste"]["k"+str(nastupiste)])
        # nastupiste

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["autobusKonci"])
        # "autobus tu jazdu konci"

        objektMain.soundAPI.pridejHlaseni([zahlasSubory,typPriorita[typ]])

    def PrichadzaKonciaci(self,objektMain,typ,spolocnost,trasaPrichod,nastupiste,vAJ,zkraceny=False):
        zahlasSubory = []

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["typ"][typ])
        # typ autobusu

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["dopravcia"][spolocnost])
        # spolocnost

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["zoSmeru"])
        # zo smeru

        poleZastavok = objektMain.vratPoleZastavok(trasaPrichod,zkraceny,True)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky

        # zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["pravidelnyPrichod"])
        # # pravidelny prichod

        # hodiny,minuty = prichod.split(":")
        # zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        # zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # # cas prichodu

        # zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["ktoryDalejPokracuje"])
        # # ktory dalej pokracuje smer

        # zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["pravidelnyOdchod"])
        # # pravidelny odchod

        # hodiny,minuty = odchod.split(":")
        # zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        # zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # # cas odchodu

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["prichadza"])
        # "prichadza"

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["nastupiste"]["k"+str(nastupiste)])
        # nastupiste

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["autobusKonci"])
        # "autobus tu jazdu konci"

    def PrisielKonciaci(self,objektMain,typ,spolocnost,trasaPrichod,prichod,nastupiste,vAJ,zkraceny=False):
        zahlasSubory = []

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice_umisteni"])
        #stanice

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["typ"][typ])
        # typ autobusu

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["dopravcia"][spolocnost])
        # spolocnost

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["zoSmeru"])
        # zo smeru

        poleZastavok = objektMain.vratPoleZastavok(trasaPrichod,zkraceny,True)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["pravidelnyPrichod"])
        # pravidelny prichod

        hodiny,minuty = prichod.split(":")
        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # cas prichodu

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["slova"]["prisiel"])
        # "prisiel"

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["nastupiste"]["k"+str(nastupiste)])
        # nastupiste

        zahlasSubory.append(objektMain.data.poleHlasenie["SK"]["vety"]["autobusKonciVystupte"])
        # "autobus tu jazdu konci"

        objektMain.soundAPI.pridejHlaseni([zahlasSubory,typPriorita[typ]])

    
class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "AVSOB"
    _svc_display_name_ = "AVSOB main service"
    _svc_description_ = "Main thread of Audio Visuálný Systém Odbavenia Autobusov"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        self.stop = False

    def SvcStop(self):
        self.stop = True
        M.soundAPI.zastav()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))


        M = Main()
        M.beh(self)

        servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STOPPED,
                (self._svc_name_, '')
                )


if __name__ == '__main__':
    # win32serviceutil.HandleCommandLine(AppServerSvc)
    
    M = Main()
    M.beh()
