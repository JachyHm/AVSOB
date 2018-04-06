import sqlite3
cestaKSuborum = "D:/OIS/erik_system/AVSOB/"
class Data():
    def __init__(self):
        self.poleHlasenie = {}
        self.NactiZastavkyNazvy()
        self.NactiTrasy()
        self.NactiDatumy()
        self.NactiSpoje()
        self.NactiHlasenie("SK")

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
                self.zastavky[tupleZastavka[1]] = tupleZastavka[0]
    
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
                    datum["obecnaPlatnost"] = datumovaPoznamka[1].split(",")
                except:
                    datum["obecnaPlatnost"] = []
            
                try:
                    datum["jedeTake"] = datumovaPoznamka[2].split(",")
                except:
                    datum["jedeTake"] = []

                try:
                    datum["nejede"] = datumovaPoznamka[3].split(",")
                except:
                    datum["nejede"] = []

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
                poleHlasenie["dopravcia"][dopravce[0]] = dopravce[2]
            
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
