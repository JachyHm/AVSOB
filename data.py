import sqlite3
class Data():
    def __init__(self):
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
                SQLdbTrasy.execute('select * from `'+str(IDtrasa[0])+'` where `zastavkaID`')
                for zastavkaTrasy in SQLdbTrasy.fetchall():
                    poleTrasyTemp.append(zastavkaTrasy[1])
                self.poleTrasy[IDtrasa[0]] = poleTrasyTemp

            print(str(self.poleTrasy))

d = Data()
