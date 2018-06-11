import csv
from colorama import init, Fore, Back, Style
from prompter import yesno
import sqlite3
from datetime import date, timedelta, datetime
import os
init()
typAutobusu = {"A":"Pbus","B":"Pbus","N":"Mbus","P":"Mbus","V":"Pbus","Z":"Rbus"}
zadaneOd = False
zadaneDo = False
cestaKSuboru = "D:/OIS/erik_system/AVSOB/"

print(Back.CYAN+Fore.RED+"*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*"+Style.RESET_ALL)
print(Back.CYAN+Fore.RED+"                            IMPORT DAT ZO SUBOROV CIS                      "+Style.RESET_ALL)
print(Back.CYAN+Fore.RED+"                            verzia aplikacie 7.4.2018                      "+Style.RESET_ALL)
print(Back.CYAN+Fore.RED+"                             copyright Urbano (2018)                       "+Style.RESET_ALL)
print(Back.CYAN+Fore.RED+"*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*"+Style.RESET_ALL)
print("Nacitam subor s verzi jednotneho datoveho formatu VerzeJDF.txt...     ",end="")
def isLast(itr):
    for old in itr:
        for new in itr:
            yield False, old
            old = new
        yield True, old
        break

def nacti():
    verzeJDF = ""
    verzeDatCIS = ""
    ################### VerzeJDF.txt ###################
    try:
        with open(cestaKSuboru+'CIS/VerzeJDF.txt', newline='') as csvfile:
            print(" ["+Fore.GREEN+"OK"+Style.RESET_ALL+"]")
            radky = csv.reader(csvfile, delimiter=',', quotechar='"')
            print("Zpracovavam subor s verzi jednotneho datoveho formatu VerzeJDF.txt... ",end="")
            for radek in radky:
                try:
                    verzeJDF = radek[0]
                    verzeDatCIS = radek[4]
                except:
                    chyba = True
                    break
            try:
                chyba
            except:
                print(" ["+Fore.GREEN+"OK"+Style.RESET_ALL+"]")
            else:
                print(" ["+Fore.RED+"CHYBA"+Style.RESET_ALL+"]")
                print(Fore.RED+"Subor VerzeJDF.txt je poskodeny, overte integritu dat!"+Style.RESET_ALL)
                return()
            
    except:
        print(" ["+Fore.RED+"CHYBA"+Style.RESET_ALL+"]")
        print(Fore.RED+"Nepodarilo sa otvorit subor VerzeJDF.txt!"+Style.RESET_ALL)
        return()

    if verzeJDF != "1.10" and verzeJDF != "1.11":
        print(Fore.RED+"Aplikacie podporuje iba VerzieJDF 1.10 a 1.11. Verzia JDF je {}!".format(verzeJDF)+Style.RESET_ALL)
        return()

    verzeDatCIS = int(verzeDatCIS[4:8]+verzeDatCIS[2:4]+verzeDatCIS[0:2])
    try:
        with open("data/verziaDat.txt","r") as file:
            radek = file.readline()
            verzeDatLokal = int(radek)
    except:
        verzeDatLokal = 0
        print(Fore.RED+"Nelze overit verziu lokalnych dat."+Fore.CYAN+"\nImportovane data mozu byt starsie ako aktualne!\nOpravdu pokracovat?"+Style.RESET_ALL,end="")
        if yesno("", default="no"):
            return()
    
    if verzeDatCIS < verzeDatLokal:
        print(Fore.RED+"Importovane data su starsie ako aktualne!"+Fore.CYAN+" Opravdu pokracovat?"+Style.RESET_ALL,end="")
        if yesno("", default="no"):
            return()
    

    # ################### SPOJDAT.txt ###################                                 ----------------------------------CHYBNA STRUKTURA DAT!!! NEPOUZIVAT!!!
    # print("Nacitam subor s datumovymi poznamkami spojdat.txt...                  ",end="")
    # datumovePoznamky = {}
    # day_of_year = datetime.now().timetuple().tm_yday
    # # try:
    # with open(cestaKSuboru+'CIS/spojdat.txt', newline='') as csvfile:
    #     print(" ["+Fore.GREEN+"OK"+Style.RESET_ALL+"]")
    #     radky = csv.reader(csvfile, delimiter=',', quotechar='"')
    #     print("Zpracovavam subor s datumovymi poznamkami spojdat.txt...              ",end="")
    #     for i, radek in enumerate(radky):
    #         try:
    #             try:
    #                 _ = datumovePoznamky[int(radek[0])]
    #             except:
    #                 datumovePoznamky[int(radek[0])] = {}
    #             else:
    #                 pass
    #             datumovePoznamky[int(radek[0])][int(radek[1])] = radek[2][:-1]
    #         except:
    #             chyba = i
    #             break
    #     try:
    #         chyba
    #     except:
    #         print(" ["+Fore.GREEN+"OK"+Style.RESET_ALL+"]")
    #     else:
    #         print(" ["+Fore.RED+"CHYBA"+Style.RESET_ALL+"]")
    #         print(Fore.RED+"Na riadku {} v subore spojdat.txt je chyba, overte integritu dat!".format(chyba)+Style.RESET_ALL)
    #         return()

    # prevedDatumovePrepinaceNaObecnou(datumovePoznamky[802401][1],2018)
            
    # except:
    #     print(" ["+Fore.RED+"CHYBA"+Style.RESET_ALL+"]")
    #     print(Fore.RED+"Nepodarilo sa otvorit subor spojdat.txt!"+Style.RESET_ALL)
    #     return()
    
    ################### LINKY.txt ###################
    print("Nacitam subor s linkami linky.txt...                                  ",end="")
    linky = {}
    dopravcovia = []
    try:
        with open(cestaKSuboru+'CIS/linky.txt', newline='') as csvfile:
            print(" ["+Fore.GREEN+"OK"+Style.RESET_ALL+"]")
            radky = csv.reader(csvfile, delimiter=',', quotechar='"')

            print("Zpracovavam subor s linkami linky.txt...                              ",end="")
            for i,radek in enumerate(radky):
                try:
                    try:
                        linky[int(radek[0])]
                    except:
                        linky[int(radek[0])] = {}

                    linky[int(radek[0])]["typ"] = typAutobusu[radek[3]]
                    if radek[13] != "":
                        platnostGVDod = radek[13]
                        zadaneOd = True
                    if radek[14] != "":
                        platnostGVDdo = radek[14]
                        zadaneDo = True
                    linky[int(radek[0])]["dopravce"] = radek[15]
                    linky[int(radek[0])]["spoje"] = {}

                    if not int(radek[15]) in set(dopravcovia):
                        dopravcovia.append(int(radek[15]))

                except:
                    chyba = i
                    break

            try:
                chyba
            except:
                print(" ["+Fore.GREEN+"OK"+Style.RESET_ALL+"]")
            else:
                print(" ["+Fore.RED+"CHYBA"+Style.RESET_ALL+"]")
                print(Fore.RED+"Na riadku {} v subore linky.txt je chyba, overte integritu dat!".format(chyba)+Style.RESET_ALL)
                return()
    except:
        print(" ["+Fore.RED+"CHYBA"+Style.RESET_ALL+"]")
        print(Fore.RED+"Nepodarilo sa otvorit subor linky.txt!"+Style.RESET_ALL)
        return()

    ################### CASKODY.txt ###################
    print("Nacitam subor s datumovymi poznamkami casKody.txt...                  ",end="")
    datumovePoznamky = {}

    # day_of_year = datetime.now().timetuple().tm_yday

    try:
        with open(cestaKSuboru+'CIS/caskody.txt', newline='') as csvfile:
            print(" ["+Fore.GREEN+"OK"+Style.RESET_ALL+"]")
            radky = csv.reader(csvfile, delimiter=',', quotechar='"')

            while not zadaneOd:
                print(Fore.CYAN+'Zadajte pociatok platnosti GAD,\nalebo "koniec" pre ukoncenie a potvrdte Enterom:'+Style.RESET_ALL,end="")
                platnostGVDod = input()
                if platnostGVDod == "koniec":
                    return()
                else:
                    try:
                        datetime.strptime(platnostGVDod,"%d.%m.%Y")
                    except:
                        print(Fore.RED+'"'+platnostGVDod+'" nieje platne datum vo formate DD.MM.YYYY!'+Style.RESET_ALL)
                    else:
                        zadaneOd = True

            while not zadaneDo:
                print(Fore.CYAN+'Zadajte koniec platnosti GAD,\nalebo "koniec" pre ukoncenie a potvrdte Enterom:'+Style.RESET_ALL,end="")
                platnostGVDdo = input()
                if platnostGVDdo == "koniec":
                    return()
                else:
                    try:
                        datetime.strptime(platnostGVDdo,"%d.%m.%Y")
                    except:
                        print(Fore.RED+'"'+platnostGVDdo+'" nieje platne datum vo formate DD.MM.YYYY!'+Style.RESET_ALL)
                    else:
                        zadaneDo = True

            print("Zpracovavam subor s datumovymi poznamkami casKody.txt...              ",end="")
            for i,radek in enumerate(radky):
                try:
                    try:
                        int(radek[3])
                    except:
                        pass
                    else:
                        if int(radek[3]) >= 10 and int(radek[3]) <= 79:
                            try:
                                datumovePoznamky[int(radek[3])]
                            except:
                                datumovePoznamky[int(radek[3])] = {}

                            try:
                                datumovePoznamky[int(radek[3])]["jedeJenVLichychTydnech"]
                            except:
                                datumovePoznamky[int(radek[3])]["jedeJenVLichychTydnech"] = 0
                            
                            try:
                                datumovePoznamky[int(radek[3])]["jedeJenVSudychTydnech"]
                            except:
                                datumovePoznamky[int(radek[3])]["jedeJenVSudychTydnech"] = 0

                            try:
                                linky[int(radek[0])]["spoje"][int(radek[1])]
                            except:
                                try:
                                    linky[int(radek[0])]
                                except:
                                    chyba = i
                                    chybaPopis = "Nedefinovana linka "+str(int(radek[0]))+" nelze pokracovat!"
                                    break

                                linky[int(radek[0])]["spoje"][int(radek[1])] = {}
                                linky[int(radek[0])]["spoje"][int(radek[1])]["casKody"] = []
                                linky[int(radek[0])]["spoje"][int(radek[1])]["obecnaPlatnost"] = []
                            if not int(radek[3]) in linky[int(radek[0])]["spoje"][int(radek[1])]["casKody"]:
                                linky[int(radek[0])]["spoje"][int(radek[1])]["casKody"].append(int(radek[3]))

                            typPoznamky = int(radek[4])
                            # jede
                            if typPoznamky == 1:
                                if radek[6] != "":
                                    od = datetime.strptime(radek[5],"%d%m%Y")
                                    do = datetime.strptime(radek[6],"%d%m%Y")
                                    interval = do - od
                                    intervalPole = []
                                    for i in range(interval.days + 1):
                                        intervalPole.append((od + timedelta(days=i)).strftime("%d%m%Y"))

                                    #pokial este neexistuje pole "jedeVRozsahu"
                                    try:
                                        datumovePoznamky[int(radek[3])]["jedeVRozsahu"]
                                    except:
                                        datumovePoznamky[int(radek[3])]["jedeVRozsahu"] = []

                                    # pridej interval do "jedeVRozsahu"
                                    datumovePoznamky[int(radek[3])]["jedeVRozsahu"].extend(intervalPole)
                                    # vymaz duplicity
                                    datumovePoznamky[int(radek[3])]["jedeVRozsahu"] = list(set(datumovePoznamky[int(radek[3])]["jedeVRozsahu"]))
                                
                                else:
                                    intervalPole = [radek[5]]
                                    #pokial este neexistuje pole "jedeVRozsahu", tak ho vytvor
                                    try:
                                        datumovePoznamky[int(radek[3])]["jedeVRozsahu"]
                                    except:
                                        datumovePoznamky[int(radek[3])]["jedeVRozsahu"] = []

                                    # pridej interval do "jedeVRozsahu"
                                    datumovePoznamky[int(radek[3])]["jedeVRozsahu"].extend(intervalPole)
                                    # vymaz duplicity
                                    datumovePoznamky[int(radek[3])]["jedeVRozsahu"] = list(set(datumovePoznamky[int(radek[3])]["jedeVRozsahu"]))

                            # jede take
                            elif typPoznamky == 2:
                                    intervalPole = [radek[5]]
                                    #pokial este neexistuje pole "jedeTake", tak ho vytvor
                                    try:
                                        datumovePoznamky[int(radek[3])]["jedeTake"]
                                    except:
                                        datumovePoznamky[int(radek[3])]["jedeTake"] = []

                                    # pridej interval do "jedeTake"
                                    datumovePoznamky[int(radek[3])]["jedeTake"].extend(intervalPole)
                                    # vymaz duplicity
                                    datumovePoznamky[int(radek[3])]["jedeTake"] = list(set(datumovePoznamky[int(radek[3])]["jedeTake"]))
                            
                            # jede jen
                            elif typPoznamky == 3:
                                datumovePoznamky[int(radek[3])]["jedeTake"] = [radek[5]]

                            # nejede
                            elif typPoznamky == 4:
                                if radek[6] != "":
                                    od = datetime.strptime(radek[5],"%d%m%Y")
                                    do = datetime.strptime(radek[6],"%d%m%Y")
                                    interval = do - od
                                    intervalPole = []
                                    for i in range(interval.days + 1):
                                        intervalPole.append((od + timedelta(days=i)).strftime("%d%m%Y"))

                                    #pokial este neexistuje pole "nejede", tak ho vytvor
                                    try:
                                        datumovePoznamky[int(radek[3])]["nejede"]
                                    except:
                                        datumovePoznamky[int(radek[3])]["nejede"] = []

                                    # pridej interval do "nejede"
                                    datumovePoznamky[int(radek[3])]["nejede"].extend(intervalPole)
                                    # vymaz duplicity
                                    datumovePoznamky[int(radek[3])]["nejede"] = list(set(datumovePoznamky[int(radek[3])]["nejede"]))
                                
                                else:
                                    intervalPole = [radek[5]]
                                    #pokial este neexistuje pole "nejede", tak ho vytvor
                                    try:
                                        datumovePoznamky[int(radek[3])]["nejede"]
                                    except:
                                        datumovePoznamky[int(radek[3])]["nejede"] = []

                                    # pridej interval do "nejede"
                                    datumovePoznamky[int(radek[3])]["nejede"].extend(intervalPole)
                                    # vymaz duplicity
                                    datumovePoznamky[int(radek[3])]["nejede"] = list(set(datumovePoznamky[int(radek[3])]["nejede"]))

                            # jede jen v lichych tydnech
                            elif typPoznamky == 5:
                                datumovePoznamky[int(radek[3])]["jedeJenVLichychTydnech"] = 1
                                datumovePoznamky[int(radek[3])]["jedeJenVLichychTydnechOd"] = platnostGVDod
                                datumovePoznamky[int(radek[3])]["jedeJenVLichychTydnechDo"] = platnostGVDdo
                            
                            # jede jen v sudych tydnech
                            elif typPoznamky == 6:
                                datumovePoznamky[int(radek[3])]["jedeJenVSudychTydnech"] = 1
                                datumovePoznamky[int(radek[3])]["jedeJenVSudychTydnechOd"] = platnostGVDod
                                datumovePoznamky[int(radek[3])]["jedeJenVSudychTydnechDo"] = platnostGVDdo

                            # jede jen v lichych tydnech od do
                            elif typPoznamky == 7:
                                datumovePoznamky[int(radek[3])]["jedeJenVLichychTydnech"] = 1
                                datumovePoznamky[int(radek[3])]["jedeJenVLichychTydnechOd"] = radek[5]
                                datumovePoznamky[int(radek[3])]["jedeJenVLichychTydnechDo"] = radek[6]

                            # jede jen v sudych tydnech od do
                            elif typPoznamky == 8:
                                datumovePoznamky[int(radek[3])]["jedeJenVSudychTydnech"] = 1
                                datumovePoznamky[int(radek[3])]["jedeJenVSudychTydnechOd"] = radek[5]
                                datumovePoznamky[int(radek[3])]["jedeJenVSudychTydnechDo"] = radek[6]

                except Exception as e:
                    chyba = i
                    chybaPopis = e
                    break

            try:
                chyba
            except:
                print(" ["+Fore.GREEN+"OK"+Style.RESET_ALL+"]")
            else:
                print(" ["+Fore.RED+"CHYBA"+Style.RESET_ALL+"]")
                print(Fore.RED+"Na riadku {} v subore casKody.txt je chyba, overte integritu dat!".format(chyba)+Style.RESET_ALL)
                print(chybaPopis)
                return()
    except:
        print(" ["+Fore.RED+"CHYBA"+Style.RESET_ALL+"]")
        print(Fore.RED+"Nepodarilo sa otvorit subor casKody.txt!"+Style.RESET_ALL)
        return()

    ################### PEVNYKOD.txt ###################
    print("Nacitam subor s pevnymi kodmi pevnyKod.txt...                         ",end="")
    try:
        with open(cestaKSuboru+'CIS/pevnyKod.txt', newline='') as csvfile:
            print(" ["+Fore.GREEN+"OK"+Style.RESET_ALL+"]")
            pevneKody = {}
            radky = csv.reader(csvfile, delimiter=',', quotechar='"')
            print("Zpracovavam subor s pevnymi kodmi pevnyKod.txt...                     ",end="")
            for i,radek in enumerate(radky):
                try:
                    if radek[1] == "X" or radek[1] == "+" or radek[1] == "1" or radek[1] == "2" or radek[1] == "3" or radek[1] == "4" or radek[1] == "5" or radek[1] == "6" or radek[1] == "7":
                        try:
                            pevneKody[int(radek[0])] = int(radek[1])
                        except:
                            pevneKody[int(radek[0])] = radek[1]
                except:
                    chyba = i
                    break

            try:
                chyba
            except:
                print(" ["+Fore.GREEN+"OK"+Style.RESET_ALL+"]")
            else:
                print(" ["+Fore.RED+"CHYBA"+Style.RESET_ALL+"]")
                print(Fore.RED+"Na riadku {} v subore pevnyKod.txt je chyba, overte integritu dat!".format(chyba)+Style.RESET_ALL)
                return()
    except:
        print(" ["+Fore.RED+"CHYBA"+Style.RESET_ALL+"]")
        print(Fore.RED+"Nepodarilo sa otvorit subor pevnyKod.txt!"+Style.RESET_ALL)
        return()   
    
    ################### ZASTAVKY.txt ###################
    print("Nacitam subor s databazi zastavek zastavky.txt...                     ",end="")
    try:
        with open(cestaKSuboru+'CIS/zastavky.txt', newline='') as csvfile:
            print(" ["+Fore.GREEN+"OK"+Style.RESET_ALL+"]")
            zastavky = {}
            radky = csv.reader(csvfile, delimiter=',', quotechar='"')
            print("Zpracovavam subor s databazi zastavek zastavky.txt...                 ",end="")
            for i,radek in enumerate(radky):
                try:
                    zastavky[int(radek[0])] = radek[1]+","+radek[2]+","+radek[3]
                except:
                    chyba = i
                    break

            try:
                chyba
            except:
                print(" ["+Fore.GREEN+"OK"+Style.RESET_ALL+"]")
            else:
                print(" ["+Fore.RED+"CHYBA"+Style.RESET_ALL+"]")
                print(Fore.RED+"Na riadku {} v subore zastavky.txt je chyba, overte integritu dat!".format(chyba)+Style.RESET_ALL)
                return()
    except:
        print(" ["+Fore.RED+"CHYBA"+Style.RESET_ALL+"]")
        print(Fore.RED+"Nepodarilo sa otvorit subor zastavky.txt!"+Style.RESET_ALL)
        return()
    
    ################### SPOJE.txt ###################
    print("Nacitam subor se spoji spoje.txt...                                   ",end="")
    try:
        with open(cestaKSuboru+'CIS/spoje.txt', newline='') as csvfile:
            print(" ["+Fore.GREEN+"OK"+Style.RESET_ALL+"]")
            radky = csv.reader(csvfile, delimiter=',', quotechar='"')

            print("Zpracovavam subor se spoji spoje.txt...                               ",end="")
            for i,radek in enumerate(radky):
                try:
                    for a, obsah in enumerate(radek):
                        try:
                            linky[int(radek[0])]
                        except:
                            print("nedefinovana linka "+str(radek[0]))
                            linky[int(radek[0])] = {}
                            linky[int(radek[0])]["spoje"] = {}
                            linky[int(radek[0])]["dopravce"] = ""
                            linky[int(radek[0])]["typ"] = "PBus"

                        if a >= 2 and a <= 11:
                            try:
                                obsah = pevneKody[int(obsah)]
                            except:
                                if a == 2 and obsah == "":
                                    try:
                                        linky[int(radek[0])]["spoje"][int(radek[1])]
                                    except:
                                        chyba = i
                                        chybaPopis = "Nedefinovana linka "+str(int(radek[0]))+" nelze pokracovat!"
                                        break

                                    linky[int(radek[0])]["spoje"][int(radek[1])]["obecnaPlatnost"] = [1,2,3,4,5,6,7,8]
                                if obsah == "":
                                    break
                            else:
                                try:
                                    obsah = [int(obsah)]
                                except:
                                    if obsah == "x":
                                        obsah = [1,2,3,4,5]
                                    elif obsah == "+":
                                        obsah = [7,8]
                                    else:
                                        obsah = ""
                                try:
                                    linky[int(radek[0])]["spoje"][int(radek[1])]
                                except:
                                    linky[int(radek[0])]["spoje"][int(radek[1])] = {}
                                    linky[int(radek[0])]["spoje"][int(radek[1])]["casKody"] = []
                                    linky[int(radek[0])]["spoje"][int(radek[1])]["obecnaPlatnost"] = []

                                linky[int(radek[0])]["spoje"][int(radek[1])]["obecnaPlatnost"].extend(obsah)

                except:
                    chyba = i
                    break

            try:
                chyba
            except:
                print(" ["+Fore.GREEN+"OK"+Style.RESET_ALL+"]")
            else:
                print(" ["+Fore.RED+"CHYBA"+Style.RESET_ALL+"]")
                print(Fore.RED+"Na riadku {} v subore spoje.txt je chyba, overte integritu dat!".format(chyba)+Style.RESET_ALL)
                return()
    except:
        print(" ["+Fore.RED+"CHYBA"+Style.RESET_ALL+"]")
        print(Fore.RED+"Nepodarilo sa otvorit subor spoje.txt!"+Style.RESET_ALL)
        return()

    # definicia pro kteru zastavku importujeme spoje
    zadaneCIS = False
    while not zadaneCIS:
        print(Fore.CYAN+"Zvolte pro ktoru stanicu maji byt CIS data importovane [cislo CIS]:"+Style.RESET_ALL,end="")
        cisloCIS = input()
        try:
            importovanaZastavka = zastavky[int(cisloCIS)]
        except:
            print(Fore.RED+"Pre zadane cislo "+cisloCIS+" nebola nalezena ziadna zastavka v databazii."+Style.RESET_ALL)
        else:
            print(Fore.CYAN+"Zvolit zastavku "+importovanaZastavka+" jako stanicu, pre ktoru generovat DB?"+Style.RESET_ALL)
            if not yesno("",default="no"):
                zadaneCIS = True

    ################### ZASSPOJE.txt ###################
    print("Nacitam subor s databazi zastavek na spoji zasSpoje.txt...            ",end="")
    # try:
    with open(cestaKSuboru+'CIS/zasSpoje.txt', newline='') as csvfile:
        print(" ["+Fore.GREEN+"OK"+Style.RESET_ALL+"]")
        radky = csv.reader(csvfile, delimiter=',', quotechar='"')
        print("Zpracovavam subor s databazi zastavek na spoji zasSpoje.txt...        ",end="")
        aktualniLinkoSpoj = None
        minulaLinka = None
        minulySpoj = None
        bylaZvolena = False
        trasy = []
        trasaPrichod = []
        trasaOdchod = []
        for i, (posledni, radek) in enumerate(isLast(radky)):
            shodaPrichod = False
            shodaOdchod = False
            nastupiste = 0
            IDtrasaPrichod = ""
            IDtrasaOdchod = ""
            try:
                # prace so suborom
                try:
                    linky[int(radek[0])]["spoje"][int(radek[1])]["trasaPrichod"]
                    linky[int(radek[0])]["spoje"][int(radek[1])]["trasaOdchod"]
                    linky[int(radek[0])]["spoje"][int(radek[1])]["casPrichod"]
                    linky[int(radek[0])]["spoje"][int(radek[1])]["casOdchod"]
                except:
                    linky[int(radek[0])]["spoje"][int(radek[1])]["trasaPrichod"] = 0
                    linky[int(radek[0])]["spoje"][int(radek[1])]["trasaOdchod"] = 0
                    linky[int(radek[0])]["spoje"][int(radek[1])]["casPrichod"] = 0
                    linky[int(radek[0])]["spoje"][int(radek[1])]["casOdchod"] = 0
                
                if aktualniLinkoSpoj == None or aktualniLinkoSpoj != radek[0]+radek[1]:
                    aktualniLinkoSpoj = radek[0]+radek[1]
                    if minulaLinka != None:
                        for idTrasy,trasa in enumerate(trasy):
                            if trasa == trasaPrichod:
                                IDtrasaPrichod = idTrasy
                                shodaPrichod = True
                            if trasa == trasaOdchod:
                                IDtrasaOdchod = idTrasy
                                shodaOdchod = True

                        if not shodaPrichod:
                            if len(trasaPrichod) > 0:
                                trasy.append(trasaPrichod)
                                IDtrasaPrichod = len(trasy)-1
                            else:
                                IDtrasaPrichod = ""
                        
                        if not shodaOdchod:
                            if len(trasaOdchod) > 0:
                                trasy.append(trasaOdchod)
                                IDtrasaOdchod = len(trasy)-1
                            else:
                                IDtrasaOdchod = ""
                        
                        linky[minulaLinka]["spoje"][minulySpoj]["trasaPrichod"] = IDtrasaPrichod
                        linky[minulaLinka]["spoje"][minulySpoj]["trasaOdchod"] = IDtrasaOdchod

                        if not bylaZvolena:
                            linky[minulaLinka]["spoje"].pop(minulySpoj)
                            if len(linky[minulaLinka]["spoje"]) == 0:
                                linky.pop(minulaLinka)

                    bylaZvolena = False
                    trasaPrichod = []
                    trasaOdchod = []

                if not bylaZvolena:
                    if int(cisloCIS) == int(radek[3]):
                        bylaZvolena = True
                        nastupiste = radek[5]
                        linky[int(radek[0])]["spoje"][int(radek[1])]["nastupiste"] = nastupiste
                        if radek[10] != "":
                            linky[int(radek[0])]["spoje"][int(radek[1])]["casPrichod"] = radek[10]
                        if radek[11] != "":
                            linky[int(radek[0])]["spoje"][int(radek[1])]["casOdchod"] = radek[11]
                    else:
                        trasaPrichod.append(int(radek[3]))
                else:
                    trasaOdchod.append(int(radek[3]))

                minulaLinka = int(radek[0])
                minulySpoj = int(radek[1])

                if posledni:
                    if minulaLinka != None:
                        for idTrasy,trasa in enumerate(trasy):
                            if trasa == trasaPrichod:
                                IDtrasaPrichod = idTrasy
                                shodaPrichod = True

                        if not shodaPrichod:
                            if len(trasaPrichod) > 0:
                                trasy.append(trasaPrichod)
                                IDtrasaPrichod = len(trasy)-1
                            else:
                                IDtrasaPrichod = ""
                        
                        for idTrasy,trasa in enumerate(trasy):
                            if trasa == trasaOdchod:
                                IDtrasaOdchod = idTrasy
                                shodaOdchod = True

                        if not shodaOdchod:
                            if len(trasaOdchod) > 0:
                                trasy.append(trasaOdchod)
                                IDtrasaOdchod = len(trasy)-1
                            else:
                                IDtrasaOdchod = ""
                        
                        linky[int(radek[0])]["spoje"][int(radek[1])]["trasaPrichod"] = IDtrasaPrichod
                        linky[int(radek[0])]["spoje"][int(radek[1])]["trasaOdchod"] = IDtrasaOdchod

                        if not bylaZvolena:
                            linky[minulaLinka]["spoje"].pop(minulySpoj)
                            if len(linky[minulaLinka]["spoje"]) == 0:
                                linky.pop(minulaLinka)

                    bylaZvolena = False
                    trasaPrichod = []
                    trasaOdchod = []
            except:
                chyba = i
                break

        try:
            chyba
        except:
            print(" ["+Fore.GREEN+"OK"+Style.RESET_ALL+"]")
        else:
            print(" ["+Fore.RED+"CHYBA"+Style.RESET_ALL+"]")
            print(Fore.RED+"Na riadku {} v subore zasSpoje.txt je chyba, overte integritu dat!".format(chyba)+Style.RESET_ALL)
            return()
    # except:
    #     print(" ["+Fore.RED+"CHYBA"+Style.RESET_ALL+"]")
    #     print(Fore.RED+"Nepodarilo sa otvorit subor zasSpoje.txt!"+Style.RESET_ALL)
    #     return()

    ################### IMPORT DO DATABAZE ###################

    # kolizia dat
    print(Fore.CYAN+"Ako sa zachovat k existujucim zaznamum "+Style.RESET_ALL+"[ponechat|aktualizovat|vymazat]"+Fore.CYAN+"?"+Style.RESET_ALL,end="")
    volbaKolize = None
    while volbaKolize == None:
        volba = input()
        if volba == "ponechat":
            volbaKolize = "ponechat"
        elif volba == "vymazat":
            volbaKolize = "vymazat"
        else:
            print(Fore.RED+"Chybna volba, opakujte zadani!"+Style.RESET_ALL)
    
    # hlasenie zastavok
    print(Fore.CYAN+"Naimportovat do databaze aj subory k hlaseniam?"+Style.RESET_ALL,end="")
    if yesno(""):
        print(Fore.CYAN+"Naimportovat hlasenie pod cislem zastavky [cisloCIS.wav]? Ak nie, bude pouzity nazev!"+Style.RESET_ALL,end="")
        while not yesno(""):
            print(Fore.RED+"Nieje este implementovane!"+Style.RESET_ALL)
            print(Fore.CYAN+"Naimportovat hlasenie pod cislem zastavky [cisloCIS.wav]?"+Style.RESET_ALL,end="")

        print("Importuji soubory hlasenia do databazie...                            ",end="")
        try:
            dbHlasenie = sqlite3.connect("hlasenie_SK.dat")
        except sqlite3.OperationalError:
            print(" ["+Fore.RED+"CHYBA"+Style.RESET_ALL+"]")
            print(Fore.RED+"Chyba citanie modulu hlasenie_SK.dat"+Style.RESET_ALL)
            input()
            return()
        else:
            SQLdbHlasenie = dbHlasenie.cursor()
            for zastavka in zastavky:
                try:
                    SQLdbHlasenie.execute("insert into `stanice` (`IDstanice`,`cestaKSuboru`) values ("+str(zastavka)+",'hlas/SK/stanice/"+str(zastavka)+".wav')")
                except Exception as e:
                    if str(e).find("UNIQUE constraint failed: stanice.IDstanice") != -1:
                        if volbaKolize == "vymazat":
                            SQLdbHlasenie.execute("update `stanice` set `cestaKSuboru` = 'hlas/SK/stanice/"+str(zastavka)+".wav' where `IDstanice` = "+str(zastavka))
                            try:
                                importZasChyba.append(Fore.YELLOW+"Hlasenie zastavky "+str(zastavka)+" uz v databazii existuje, prepisuji!"+Style.RESET_ALL)
                            except:
                                importZasChyba = []
                                importZasChyba.append(Fore.YELLOW+"Hlasenie zastavky "+str(zastavka)+" uz v databazii existuje, prepisuji!"+Style.RESET_ALL)
                        else:
                            try:
                                importZasChyba.append(Fore.YELLOW+"Hlasenie zastavky "+str(zastavka)+" uz v databazii existuje, preskakuji!"+Style.RESET_ALL)
                            except:
                                importZasChyba = []
                                importZasChyba.append(Fore.YELLOW+"Hlasenie zastavky "+str(zastavka)+" uz v databazii existuje, preskakuji!"+Style.RESET_ALL)

            dbHlasenie.commit()
            dbHlasenie.close()
            try:
                importZasChyba
            except:
                print(" ["+Fore.GREEN+"OK"+Style.RESET_ALL+"]")
            else:
                print(" ["+Fore.YELLOW+"POZOR"+Style.RESET_ALL+"]")
                for chyba in importZasChyba:
                    print(chyba)

    print("Importuji zastavky do databazie...                            ",end="")
    try:
        dbHlasenie = sqlite3.connect("zastavky.dat")
    except sqlite3.OperationalError:
        print(" ["+Fore.RED+"CHYBA"+Style.RESET_ALL+"]")
        print(Fore.RED+"Chyba citanie modulu zastavky.dat"+Style.RESET_ALL)
        input()
        return()
    else:
        SQLdbHlasenie = dbHlasenie.cursor()
        for zastavka in zastavky:
            try:
                SQLdbHlasenie.execute("insert into `zastavkyMena` (`IDzastavky`,`TextZastavky`) values ("+str(zastavka)+",'"+str(zastavky[zastavka])+"')")
            except Exception as e:
                if str(e).find("UNIQUE constraint failed: zastavkyMena.IDstanice") != -1:
                    if volbaKolize == "vymazat":
                        SQLdbHlasenie.execute("update `zastavkyMena` set `IDzastavky` = "+str(zastavka)+",`TextZastavky` = '"+str(zastavky[zastavka])+"' where `IDstanice` = "+str(zastavka)+")")
                        try:
                            importZasChyba.append(Fore.YELLOW+"Zastavka "+str(zastavka)+" uz v databazii existuje, prepisuji!"+Style.RESET_ALL)
                        except:
                            importZasChyba = []
                            importZasChyba.append(Fore.YELLOW+"Zastavka "+str(zastavka)+" uz v databazii existuje, prepisuji!"+Style.RESET_ALL)
                    else:
                        try:
                            importZasChyba.append(Fore.YELLOW+"Zastavka "+str(zastavka)+" uz v databazii existuje, preskakuji!"+Style.RESET_ALL)
                        except:
                            importZasChyba = []
                            importZasChyba.append(Fore.YELLOW+"Zastavka "+str(zastavka)+" uz v databazii existuje, preskakuji!"+Style.RESET_ALL)

        dbHlasenie.commit()
        dbHlasenie.close()
        try:
            importZasChyba
        except:
            print(" ["+Fore.GREEN+"OK"+Style.RESET_ALL+"]")
        else:
            print(" ["+Fore.YELLOW+"POZOR"+Style.RESET_ALL+"]")
            for chyba in importZasChyba:
                print(chyba)

    # hlasenie dopravcov
    print(Fore.CYAN+"Naimportovat do databaze aj hlasenie spolocnosti?"+Style.RESET_ALL,end="")
    if yesno(""):
        print(Fore.CYAN+"Naimportovat hlasenie spolocnosti pod cislem [cisloSPOL.wav]? Ak nie, bude pouzity nazev!"+Style.RESET_ALL,end="")
        while not yesno(""):
            print(Fore.RED+"Nieje este implementovane!"+Style.RESET_ALL)
            print(Fore.CYAN+"Naimportovat hlasenie spolocnosti pod cislem [cisloSPOL.wav]?"+Style.RESET_ALL,end="")
        print("Importuji soubory hlasenia spolocnosti do databazie...                ",end="")
        try:
            dbHlasenie = sqlite3.connect("hlasenie_SK.dat")
        except sqlite3.OperationalError:
            print(" ["+Fore.RED+"CHYBA"+Style.RESET_ALL+"]")
            print(Fore.RED+"Chyba citanie modulu hlasenie_SK.dat"+Style.RESET_ALL)
            input()
            return()
        else:
            SQLdbHlasenie = dbHlasenie.cursor()
            for dopravca in dopravcovia:
                try:
                    SQLdbHlasenie.execute("insert into `dopravcia` (`dopravca`,`cestaKSuboru`) values ("+str(dopravca)+",'hlas/SK/dopravcia/"+str(dopravca)+".wav')")
                except Exception as e:
                    if str(e).find("UNIQUE constraint failed: dopravcia.ID") != -1:
                        if volbaKolize == "vymazat":
                            SQLdbHlasenie.execute("update `dopravcia` set `cestaKSuboru` = 'hlas/SK/stanice/"+str(dopravca)+".wav' where `dopravca` = "+str(dopravca))
                            try:
                                importDopChyba.append(Fore.YELLOW+"Dopravca "+str(dopravca)+" uz v databazii existuje, prepisuji!"+Style.RESET_ALL)
                            except:
                                importDopChyba = []
                                importDopChyba.append(Fore.YELLOW+"Dopravca "+str(dopravca)+" uz v databazii existuje, prepisuji!"+Style.RESET_ALL)
                        else:
                            try:
                                importDopChyba.append(Fore.YELLOW+"Dopravca "+str(dopravca)+" uz v databazii existuje, preskakuji!"+Style.RESET_ALL)
                            except:
                                importDopChyba = []
                                importDopChyba.append(Fore.YELLOW+"Dopravca "+str(dopravca)+" uz v databazii existuje, preskakuji!"+Style.RESET_ALL)

            dbHlasenie.commit()
            dbHlasenie.close()
            try:
                importDopChyba
            except:
                print(" ["+Fore.GREEN+"OK"+Style.RESET_ALL+"]")
            else:
                print(" ["+Fore.YELLOW+"POZOR"+Style.RESET_ALL+"]")
                for chyba in importDopChyba:
                    print(chyba)
    
    # trasy
    print(Fore.CYAN+"Naimportovat do databaze aj trasy?"+Style.RESET_ALL,end="")
    if yesno(""):
        print("Importuji trasy do databazie...                                       ",end="")
        try:
            os.remove(cestaKSuboru+"trasy.dat")
            dbTrasy = sqlite3.connect("trasy.dat")
        except sqlite3.OperationalError:
            print(" ["+Fore.RED+"CHYBA"+Style.RESET_ALL+"]")
            print(Fore.RED+"Chyba citanie modulu trasy.dat"+Style.RESET_ALL)
            input()
            return()
        else:
            SQLdbTrasy = dbTrasy.cursor()
            SQLdbTrasy.execute('CREATE TABLE "seznamTras" ( `IDtrasy` INTEGER, PRIMARY KEY(`IDtrasy`) )')
            for i,trasa in enumerate(trasy):
                try:
                    SQLdbTrasy.execute("insert into `seznamTras` (`IDtrasy`) values ("+str(i+1)+")")
                except Exception as e:
                    if str(e).find("UNIQUE constraint failed: seznamTras.IDtrasy") != -1:
                        if volbaKolize == "vymazat":
                            SQLdbTrasy.execute("drop table `"+str(i+1)+"`")
                            SQLdbTrasy.execute("CREATE TABLE `"+str(i+1)+"` ( `ID` INTEGER, `zastavkaID` INTEGER, PRIMARY KEY(`ID`) )")
                            for zastavka in trasa:
                                SQLdbTrasy.execute("insert into `"+str(i+1)+"` (`zastavkaID`) values ("+str(zastavka)+")")
                            try:
                                importTrasyChyba.append(Fore.YELLOW+"Trasa "+str(trasa)+" uz v databazii existuje, prepisuji!"+Style.RESET_ALL)
                            except:
                                importTrasyChyba = []
                                importTrasyChyba.append(Fore.YELLOW+"Trasa "+str(trasa)+" uz v databazii existuje, prepisuji!"+Style.RESET_ALL)
                        else:
                            try:
                                importTrasyChyba.append(Fore.YELLOW+"Trasa "+str(trasa)+" uz v databazii existuje, preskakuji!"+Style.RESET_ALL)
                            except:
                                importTrasyChyba = []
                                importTrasyChyba.append(Fore.YELLOW+"Trasa "+str(trasa)+" uz v databazii existuje, preskakuji!"+Style.RESET_ALL)
                else:
                    SQLdbTrasy.execute("CREATE TABLE `"+str(i+1)+"` ( `ID` INTEGER, `zastavkaID` INTEGER, PRIMARY KEY(`ID`) )")
                    for zastavka in trasa:
                        SQLdbTrasy.execute("insert into `"+str(i+1)+"` (`zastavkaID`) values ("+str(zastavka)+")")

            dbTrasy.commit()
            dbTrasy.close()
            try:
                importTrasyChyba
            except:
                print(" ["+Fore.GREEN+"OK"+Style.RESET_ALL+"]")
            else:
                print(" ["+Fore.YELLOW+"POZOR"+Style.RESET_ALL+"]")
                for chyba in importTrasyChyba:
                    print(chyba)

    # spoje
    print(Fore.CYAN+"Naimportovat do databaze aj spoje?"+Style.RESET_ALL,end="")
    if yesno(""):
        print("Importuji spoje do databazie...                                       ",end="")
        try:
            dbTrasy = sqlite3.connect("spoje.dat")
        except sqlite3.OperationalError:
            print(" ["+Fore.RED+"CHYBA"+Style.RESET_ALL+"]")
            print(Fore.RED+"Chyba citanie modulu spoje.dat"+Style.RESET_ALL)
            input()
            return()
        else:
            chyba = False
            SQLdbTrasy = dbTrasy.cursor()
            SQLdbTrasy.execute("delete from `spoje`")
            for linka in linky:
                typ = linky[linka]["typ"]
                dopravca = linky[linka]["dopravce"]
                for spoj in linky[linka]["spoje"]:
                    cisloSpoje = spoj
                    spoj = linky[linka]["spoje"][spoj]
                    nastupiste = spoj["nastupiste"]
                    if nastupiste == '':
                        if not chyba:
                            print(" ["+Fore.YELLOW+"POZOR"+Style.RESET_ALL+"]")
                            chyba = True
                        print(Fore.RED+"Pro spoj "+str(cisloSpoje)+",linky "+str(linka)+" nieje uvedene nastupiste,"+Fore.CYAN+" zadajte ho teraz:"+Style.RESET_ALL)
                        nastupiste = input()
                        try:
                            int(nastupiste)
                        except:
                            zadaneNast = False
                        else:
                            zadaneNast = True

                        while not zadaneNast:
                            print(Fore.RED+'"'+str(nastupiste)+'" neni platna hodnota nastupiste. Zkuste to znovu!'+Style.RESET_ALL)
                            nastupiste = input()
                            try:
                                int(nastupiste)
                            except:
                                zadaneNast = False
                            else:
                                zadaneNast = True

                    if spoj["trasaPrichod"] == '' or spoj["trasaPrichod"] == 0:
                        zacina = 1
                        spoj["trasaPrichod"] = 0
                    else:
                        zacina = 0

                    if spoj["trasaOdchod"] == '' or spoj["trasaOdchod"] == 0:
                        konci = 1
                        spoj["trasaOdchod"] = 0
                    else:
                        konci = 0

                    stringPoznamky = ""
                    for i,poznamka in enumerate(spoj["casKody"]):
                        if i > 0:
                            stringPoznamky = stringPoznamky+","+poznamka
                        else:
                            stringPoznamky = poznamka

                    if spoj["casPrichod"] != 0:
                        casPrichod = spoj["casPrichod"][:2]+":"+spoj["casPrichod"][2:]
                    else:
                        casPrichod = 0

                    if spoj["casOdchod"] != 0:
                        casOdchod = spoj["casOdchod"][:2]+":"+spoj["casOdchod"][2:]
                    else:
                        casOdchod = 0

                    obecnaPlatnost = ""
                    if spoj["obecnaPlatnost"] != []:
                        for i,den in enumerate(spoj["obecnaPlatnost"]):
                            obecnaPlatnost = obecnaPlatnost+str(den)
                            if i < len(spoj["obecnaPlatnost"])-1:
                                obecnaPlatnost = obecnaPlatnost+","
                    else:
                        obecnaPlatnost = "1,2,3,4,5,6,7,8"

                    # print("insert into `spoje` (`IDplatnosti`,`SK`,`ENG`,`IDtrasyPrichod`,`IDtrasyOdchod`,`casPrichod`,`casOdchod`,`konci`,`zacina`,`dopravca`,`linka`,`nastupiste`,`typ`) values ('"+
                    #     str(stringPoznamky)+
                    #     "',1,0,"+
                    #     str(spoj["trasaPrichod"])+","+
                    #     str(spoj["trasaOdchod"])+",'"+
                    #     str(casPrichod)+"','"+
                    #     str(casOdchod)+"',"+
                    #     str(konci)+","+
                    #     str(zacina)+","+
                    #     str(dopravca)+","+
                    #     str(linka)+","+
                    #     str(spoj["nastupiste"])+",'"+
                    #     str(typ)+"')")

                    SQLdbTrasy.execute("insert into `spoje` (`IDplatnosti`,`SK`,`ENG`,`IDtrasyPrichod`,`IDtrasyOdchod`,`casPrichod`,`casOdchod`,`konci`,`zacina`,`dopravca`,`linka`,`nastupiste`,`typ`,`obecnaPlatnost`) values ('"+
                        str(stringPoznamky)+
                        "',1,0,"+
                        str(spoj["trasaPrichod"])+","+
                        str(spoj["trasaOdchod"])+",'"+
                        str(casPrichod)+"','"+
                        str(casOdchod)+"',"+
                        str(konci)+","+
                        str(zacina)+","+
                        str(dopravca)+","+
                        str(linka)+","+
                        str(nastupiste)+",'"+
                        str(typ)+"','"+
                        str(obecnaPlatnost)+"')")

            dbTrasy.commit()
            dbTrasy.close()
            if not chyba:
                print(" ["+Fore.GREEN+"OK"+Style.RESET_ALL+"]")
            else:
                print("Importuji spoje do databazie...                                       ",end="")
                print(" ["+Fore.GREEN+"OK"+Style.RESET_ALL+"]")

    with open("data/verziaDat.txt","w") as file:
        file.write(str(verzeDatCIS))
    
    # datumove poznamky
    print(Fore.CYAN+"Naimportovat do databaze aj datumove poznamky?"+Style.RESET_ALL,end="")
    if yesno(""):
        print("Importuji datumove poznamky do databazie...                           ",end="")
        try:
            dbDatumy = sqlite3.connect("datumy.dat")
        except sqlite3.OperationalError:
            print(" ["+Fore.RED+"CHYBA"+Style.RESET_ALL+"]")
            print(Fore.RED+"Chyba citanie modulu datumy.dat"+Style.RESET_ALL)
            input()
            return()
        else:
            SQLdbDatumy = dbDatumy.cursor()
            SQLdbDatumy.execute("delete from `datumy`")
            for ID in datumovePoznamky:
                datumovaPoznamka = datumovePoznamky[ID]

                jedeTake = ""
                try:
                    for i,datum in enumerate(datumovaPoznamka["jedeTake"]):
                        jedeTake = jedeTake+datum
                        if i < len(datumovaPoznamka["jedeTake"])-1:
                            jedeTake = jedeTake+","
                except:
                    pass

                nejede = ""
                try:
                    for i,datum in enumerate(datumovaPoznamka["nejede"]):
                        nejede = nejede+datum
                        if i < len(datumovaPoznamka["nejede"])-1:
                            nejede = nejede+","
                except:
                    pass

                jedeLiche = datumovaPoznamka["jedeJenVLichychTydnech"]
                jedeSude = datumovaPoznamka["jedeJenVSudychTydnech"]

                jede = ""
                try:
                    for i,datum in enumerate(datumovaPoznamka["jedeVRozsahu"]):
                        jede = jede+datum
                        if i < len(datumovaPoznamka["jedeVRozsahu"])-1:
                            jede = jede+","
                except:
                    pass

                SQLdbDatumy.execute("insert into `datumy` (`ID`,`jede`,`jedeTake`,`nejede`,`jedeJenVLichychTydnech`,`jedeJenVSudychTydnech`) values ("+
                str(ID)+",'"+
                str(jede)+"','"+
                str(jedeTake)+"','"+
                str(nejede)+"',"+
                str(jedeLiche)+","+
                str(jedeSude)+")")

            dbDatumy.commit()
            dbDatumy.close()

            print(" ["+Fore.GREEN+"OK"+Style.RESET_ALL+"]")    
            
# def ziskejVsetkyZadaneDniVRoce(year,day):
#    d = date(year, 1, 1)                    # January 1st
#    d += timedelta(days = day - d.weekday())  # First Sunday
#    while d.year == year:
#       yield d
#       d += timedelta(days = 7)

# def prevedDatumovePrepinaceNaObecnou(datumovePrepinace, rok):
#     for i, prepinac in enumerate(datumovePrepinace):
#         datum = datetime(rok, 1, 1) + timedelta(i)
#         print(datum, prepinac)
try:
    nacti()
except KeyboardInterrupt:
    print()
    print(Back.RED+"                                                                           "+Style.RESET_ALL)
    print(Back.RED+Fore.BLACK+"      Predcasne ukoncenie programu. Overte celistvost zapsanych dat!       "+Style.RESET_ALL)
    print(Back.RED+"                                                                           "+Style.RESET_ALL)
print(Back.GREEN+Fore.BLACK+"*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*"+Style.RESET_ALL)
print(Back.GREEN+Fore.BLACK+"                             KONEC IMPORTU                                 "+Style.RESET_ALL)
print(Back.GREEN+Fore.BLACK+"                           Prijemny zbytok dna                             "+Style.RESET_ALL)
print(Back.GREEN+Fore.BLACK+"                                                                           "+Style.RESET_ALL)
print(Back.GREEN+Fore.BLACK+"              Aplikaciu ukoncite stisknutim lubovolnej klavesy...          "+Style.RESET_ALL)
print(Back.GREEN+Fore.BLACK+"*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*"+Style.RESET_ALL)
input()
