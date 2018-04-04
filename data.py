import sqlite3
class Data():
    def __init__(self):
        self.poleHlasenie = {}
        self.NactiZastavkyNazvy()
        self.NactiTrasy()
        self.NactiHlasenie("SK")

    def NactiZastavkyNazvy(self):
        try:
            dbZastavky = sqlite3.connect("data/zastavky.dat")
        except sqlite3.OperationalError:
            input("Chyba čítanie modulu zastavky.dat!")
        else:            
            SQLdbZastavky = dbZastavky.cursor()
            SQLdbZastavky.execute('select * from `zastavkyMena` where `IDzastavky`')
            self.zastavky = {}
            for tupleZastavka in SQLdbZastavky.fetchall():
                self.zastavky[tupleZastavka[1]] = tupleZastavka[0]
    def NactiSpoje(self):
        try:
            dbSpoje = sqlite3.connect("data/spoje.dat")
        except:
            input("Chyba čítanie modulu spoje.dat!")
        else:
            SQLdbSpoje = dbSpoje.cursor()
            SQLdbSpoje.execute('select * from `spoje`')
            self.spoje = {}
            for tupleSpoj in SQLdbSpoje.fetchall():
                # self.spoje[tupleSpoj[0]] = 
                pass


    def NactiTrasy(self):
        try:
            dbTrasy = sqlite3.connect("data/trasy.dat")
        except sqlite3.OperationalError:
            input("Chyba čítanie modulu trasy.dat!")
        else:            
            SQLdbTrasy = dbTrasy.cursor()
            SQLdbTrasy.execute('select * from `seznamTras` where `IDtrasy`')
            self.trasyID = []
            for IDtrasa in SQLdbTrasy.fetchall():
                self.trasyID.append(IDtrasa)
                    
            self.trasy = {}
            
            for IDtrasa in self.trasyID:
                trasyTemp = []
                SQLdbTrasy.execute('select * from `'+str(IDtrasa[0])+'` where `zastavkaID`')
                for zastavkaTrasy in SQLdbTrasy.fetchall():
                    trasyTemp.append(zastavkaTrasy[1])
                self.trasy[IDtrasa[0]] = trasyTemp

    def NactiHlasenie(self, jazyk):
        try:
            dbHlasenie = sqlite3.connect("data/hlasenie_"+jazyk+".dat")
        except sqlite3.OperationalError:
            input("Chyba čítanie modulu hlasenie_"+jazyk+".dat")
        else:
            SQLdbHlasenie = dbHlasenie.cursor()
            poleHlasenie = {}
            poleHlasenie["stanice"] = {}
            poleHlasenie["slova"] = {}
            poleHlasenie["minuty"] = {}
            poleHlasenie["hodiny"] = {}
            poleHlasenie["nastupiste"] = {}
            poleHlasenie["vety"] = {}
            poleHlasenie["dopravcia"] = {}
            poleHlasenie["znelky"] = {}
            poleHlasenie["typ"] = {}

            SQLdbHlasenie.execute('select * from `stanice`')
            for zastavka in SQLdbHlasenie.fetchall():
                poleHlasenie["stanice"][zastavka[0]] = zastavka[1]
                
            SQLdbHlasenie.execute('select * from `slova`')
            for slovo in SQLdbHlasenie.fetchall():
                poleHlasenie["slova"][slovo[0]] = slovo[1]
                
            SQLdbHlasenie.execute('select * from `minuty`')
            for minuta in SQLdbHlasenie.fetchall():
                poleHlasenie["minuty"][minuta[0]] = minuta[1]
                
            SQLdbHlasenie.execute('select * from `hodiny`')
            for hodina in SQLdbHlasenie.fetchall():
                poleHlasenie["hodiny"][hodina[0]] = hodina[1]
                
            SQLdbHlasenie.execute('select * from `nastupiste`')
            for nastupiste in SQLdbHlasenie.fetchall():
                poleHlasenie["nastupiste"][nastupiste[0]] = nastupiste[1]
            
            SQLdbHlasenie.execute('select * from `vety`')
            for veta in SQLdbHlasenie.fetchall():
                poleHlasenie["vety"][veta[0]] = veta[1]
            
            SQLdbHlasenie.execute('select * from `dopravcia`')
            for dopravce in SQLdbHlasenie.fetchall():
                poleHlasenie["dopravcia"][dopravce[0]] = dopravce[2]
            
            SQLdbHlasenie.execute('select * from `znelky`')
            for znelka in SQLdbHlasenie.fetchall():
                poleHlasenie["znelky"][znelka[0]] = znelka[1]

            SQLdbHlasenie.execute('select * from `typ`')
            for typ in SQLdbHlasenie.fetchall():
                print(typ)
                poleHlasenie["typ"][typ[0]] = typ[1]
            
            self.poleHlasenie[jazyk] = poleHlasenie
