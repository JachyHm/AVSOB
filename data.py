import sqlite3
class Data():
    def __init__(self):
        self.poleHlasenie = {}
        self.nactiZastavkyNazvy()
        self.nactiTrasy()

    def nactiZastavkyNazvy(self):
        try:
            dbZastavkyNazvy = sqlite3.connect("data/zastavkyNazvy.dat")
        except sqlite3.OperationalError:
            input("Chyba čítanie modulu zastavky.dat!")
        else:            
            SQLdbZastavkyNazvy = dbZastavkyNazvy.cursor()
            SQLdbZastavkyNazvy.execute('select * from `zastavkyMena` where `IDzastavky`')
            self.poleZastavkyJmena = {}
            for tupleZastavka in SQLdbZastavkyNazvy.fetchall():
                self.poleZastavkyJmena[tupleZastavka[1]] = tupleZastavka[0]

    def nactiTrasy(self):
        try:
            dbTrasy = sqlite3.connect("data/trasy.dat")
        except sqlite3.OperationalError:
            input("Chyba čítanie modulu trasy.dat!")
        else:            
            SQLdbTrasy = dbTrasy.cursor()
            SQLdbTrasy.execute('select * from `seznamTras` where `IDtrasy`')
            self.poleTrasyID = []
            for IDtrasa in SQLdbTrasy.fetchall():
                self.poleTrasyID.append(IDtrasa)
                    
            self.poleTrasy = {}
            
            for IDtrasa in self.poleTrasyID:
                poleTrasyTemp = []
                SQLdbTrasy.execute('select * from `?` where `zastavkaID`',str(IDtrasa[0]))
                for zastavkaTrasy in SQLdbTrasy.fetchall():
                    poleTrasyTemp.append(zastavkaTrasy[1])
                self.poleTrasy[IDtrasa[0]] = poleTrasyTemp
                
     def nactiHlasenie(self, jazyk):
        try:
            dbHlasenie = sqlite3.connect("data/hlasenie.dat")
        except sqlite3.OperationalError:
            input("Chyba čítanie modulu hlasenie.dat")
        else:
            SQLdbHlasenie = dbHlasenie.cursor()
            poleHlasenie = {}
            SQLdbHlasenie.execute('select * from `stanice` where `cestaKSuboru`')
            for zastavka in SQLdbHlasenie.fetchall():
                poleHlasenie[zastavka[0]] = zastavka[1]
                
            SQLdbHlasenie.execute('select * from `slova` where `cestaKSuboru`')
            for slovo in SQLdbHlasenie.fetchall():
                poleHlasenie[slovo[0]] = slovo[1]
                
            SQLdbHlasenie.execute('select * from `minuty` where `cestaKSuboru`')
            for minuta in SQLdbHlasenie.fetchall():
                poleHlasenie[minuta[0]] = minuta[1]
                
            SQLdbHlasenie.execute('select * from `hodiny` where `cestaKSuboru`')
            for hodina in SQLdbHlasenie.fetchall():
                poleHlasenie[hodina[0]] = hodina[1]
                
            SQLdbHlasenie.execute('select * from `nastupiste` where `cestaKSuboru`')
            for nastupiste in SQLdbHlasenie.fetchall():
                poleHlasenie[nastupiste[0]] = nastupiste[1]
                
            SQLdbHlasenie.execute('select * from `vety` where `cestaKSuboru`')
            for veta in SQLdbHlasenie.fetchall():
                poleHlasenie[veta[0]] = veta[1]    
                
            self.poleHlasenie[jazyk) = poleHlasenie
            
d = Data()
