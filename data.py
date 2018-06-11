import sqlite3
from collections import OrderedDict

cestaKSuborum = "D:/OIS/erik_system/AVSOB/"
class Data():
    def __init__(self):
        self.poleHlasenie = {}
        self.NactiZastavkyNazvy()
        self.NactiTrasy()
        self.NactiDatumy()
        self.NactiSpoje()
        self.NactiHlasenie("SK")
        self.NactiSvatky()

    def KedySuVelikonoce(self):
        import datetime
        datumObj = datetime.date.today()
        a = datumObj.year%19
        b = datumObj.year%4
        c = datumObj.year%7
        m = 24
        n = 5
        d = (19*a+m)%30
        e = (n+2*b+4*c+6*d)%7
        u = d + e - 9
        if u == 25 and d == 28 and e == 6 and a > 10:
            u = 18
            v = 4 
        elif u >= 1 and u <=25:
            v = 4
        elif u > 25:
            u = u -7
            v = 4
        else:
            u = 22 + d + e 
            v = 3
        pondeli = datetime.date(datumObj.year,v,u) + datetime.timedelta(days=1)
        patek = (pondeli - datetime.timedelta(days=3)).strftime("%d%m%Y")
        pondeli = pondeli.strftime("%d%m%Y")
        return [patek,pondeli]

    def NactiZastavkyNazvy(self):
        try:
            dbZastavky = sqlite3.connect(cestaKSuborum+"data/zastavky.dat")
        except sqlite3.OperationalError:
            pass
            # input("Chyba čítanie modulu zastavky.dat!")
        else:            
            SQLdbZastavky = dbZastavky.cursor()
            SQLdbZastavky.execute('select * from `zastavkyMena` where `IDzastavky`')
            self.zastavky = {}
            for tupleZastavka in SQLdbZastavky.fetchall():
                self.zastavky[tupleZastavka[0]] = tupleZastavka[1]
    
    def NactiDatumy(self):
        try:
            dbDatumy = sqlite3.connect(cestaKSuborum+"data/datumy.dat")
        except sqlite3.OperationalError:
            pass
            # input("Chyba čítanie modulu spoje.dat!")
        else:
            SQLdbDatumy = dbDatumy.cursor()
            SQLdbDatumy.execute('select * from `datumy`')
            self.datumy = {}
            for datumovaPoznamka in SQLdbDatumy.fetchall():
                datum = {}

                try:
                    datum["jede"] = datumovaPoznamka[1].split(",")
                except:
                    datum["jede"] = []
            
                try:
                    datum["jedeTake"] = datumovaPoznamka[2].split(",")
                except:
                    datum["jedeTake"] = []

                try:
                    datum["nejede"] = datumovaPoznamka[3].split(",")
                except:
                    datum["nejede"] = []

                try:
                    datum["jedeLiche"] = datumovaPoznamka[4]
                except:
                    datum["jedeLiche"] = 0

                try:
                    datum["jedeSude"] = datumovaPoznamka[5]
                except:
                    datum["jedeSude"] = 0

                self.datumy[datumovaPoznamka[0]] = datum

    def NactiSpoje(self):
        try:
            dbSpoje = sqlite3.connect(cestaKSuborum+"data/spoje.dat")
        except sqlite3.OperationalError:
            pass
            # input("Chyba čítanie modulu spoje.dat!")
        else:
            SQLdbSpoje = dbSpoje.cursor()
            SQLdbSpoje.execute('select * from `spoje`')
            self.spoje = {}
            self.spojeDlaCasuPrich = {}
            self.spojeDlaCasuOdch = {}
            for tupleSpoj in SQLdbSpoje.fetchall():
                spoj = {}
                spoj["IDplatnosti"] = tupleSpoj[1]
                spoj["hlasSK"] = tupleSpoj[2]
                spoj["hlasEN"] = tupleSpoj[3]
                spoj["IDtrasyPrichod"] = tupleSpoj[4]
                spoj["IDtrasyOdchod"] = tupleSpoj[5]
                spoj["casPrichodu"] = tupleSpoj[6]
                spoj["casOdchodu"] = tupleSpoj[7]
                spoj["konci"] = tupleSpoj[8]
                spoj["zacina"] = tupleSpoj[9]
                spoj["IDdopravca"] = tupleSpoj[10]
                spoj["linka"] = tupleSpoj[11]
                spoj["nastupiste"] = tupleSpoj[12]
                spoj["typ"] = tupleSpoj[13]
                spoj["obecnaPlatnost"] = tupleSpoj[14]
                self.spoje[tupleSpoj[0]] = spoj
                if tupleSpoj[9] == 0:
                    try:
                        _ = self.spojeDlaCasuPrich[tupleSpoj[6]]
                    except:
                        self.spojeDlaCasuPrich[tupleSpoj[6]] = [tupleSpoj[0]]
                    else:
                        self.spojeDlaCasuPrich[tupleSpoj[6]].append(tupleSpoj[0])
                
                if tupleSpoj[8] == 0:
                    try:
                        _ = self.spojeDlaCasuOdch[tupleSpoj[7]]
                    except:
                        self.spojeDlaCasuOdch[tupleSpoj[7]] = [tupleSpoj[0]]
                    else:
                        self.spojeDlaCasuOdch[tupleSpoj[7]].append(tupleSpoj[0])

            self.spojeDlaCasuPrichPride = self.spojeDlaCasuPrich
            self.spojeDlaCasuPrichPrideDruhy = self.spojeDlaCasuPrich
            self.spojeDlaCasuPrichPrichadza = self.spojeDlaCasuPrich
            self.spojeDlaCasuPrichPrisiel = self.spojeDlaCasuPrich
            self.spojeDlaCasuOdchBudePristaveny = self.spojeDlaCasuOdch
            self.spojeDlaCasuOdchBudePristavenyDruhe = self.spojeDlaCasuOdch
            self.spojeSerazene = OrderedDict(sorted(self.spoje.items(),key=lambda x:int(str(x[1]['casOdchodu'] if x[1]['casOdchodu'] != 0 else x[1]['casPrichodu']).replace(":", ""))))
            
    def NactiSvatky(self):
        import datetime
        try:
            dbSvatky = sqlite3.connect(cestaKSuborum+"data/svatky.dat")
        except sqlite3.OperationalError:
            pass
            # input("Chyba čítanie modulu trasy.dat!")
        else:            
            SQLdbSvatky = dbSvatky.cursor()
            SQLdbSvatky.execute('select * from `svatky` where `datum`')
        self.svatky = []
        for datum in SQLdbSvatky.fetchall():
            self.svatky.append(datum[0]+str(datetime.date.today().year))
        
        self.svatky.extend(self.KedySuVelikonoce())
        
    def NactiTrasy(self):
        try:
            dbTrasy = sqlite3.connect(cestaKSuborum+"data/trasy.dat")
        except sqlite3.OperationalError:
            pass
            # input("Chyba čítanie modulu trasy.dat!")
        else:            
            SQLdbTrasy = dbTrasy.cursor()
            SQLdbTrasy.execute('select * from `seznamTras` where `IDtrasy`')
            self.trasyID = []
            for IDtrasa in SQLdbTrasy.fetchall():
                self.trasyID.append(IDtrasa[0])
                    
            self.trasy = {}
            
            for IDtrasa in self.trasyID:
                trasyTemp = []
                SQLdbTrasy.execute('select * from `'+str(IDtrasa)+'` where `zastavkaID`')
                for zastavkaTrasy in SQLdbTrasy.fetchall():
                    trasyTemp.append(zastavkaTrasy[1])
                self.trasy[IDtrasa] = trasyTemp

    def NactiHlasenie(self, jazyk):
        try:
            dbHlasenie = sqlite3.connect(cestaKSuborum+"data/hlasenie_"+jazyk+".dat")
        except sqlite3.OperationalError:
            pass
            # input("Chyba čítanie modulu hlasenie_"+jazyk+".dat")
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
            poleHlasenie["stanice_umisteni"] = {}
            poleHlasenie["cestaKSuborum"] = cestaKSuborum

            SQLdbHlasenie.execute('select * from `stanice`')
            for stanica in SQLdbHlasenie.fetchall():
                poleHlasenie["stanice"][stanica[0]] = stanica[1]
                
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
                poleHlasenie["dopravcia"][dopravce[1]] = dopravce[2]
            
            SQLdbHlasenie.execute('select * from `znelky`')
            for znelka in SQLdbHlasenie.fetchall():
                poleHlasenie["znelky"][znelka[0]] = znelka[1]

            SQLdbHlasenie.execute('select * from `typ`')
            for typ in SQLdbHlasenie.fetchall():
                poleHlasenie["typ"][typ[0]] = typ[1]

            SQLdbHlasenie.execute('select * from `stanice_umisteni`')
            for stanica in SQLdbHlasenie.fetchall():
                poleHlasenie["stanice_umisteni"] = stanica[1]
            
            self.poleHlasenie[jazyk] = poleHlasenie
