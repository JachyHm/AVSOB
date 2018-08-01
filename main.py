import data
import soundAPI
import win32serviceutil, win32service
import win32event
import win32evtlogutil
import win32evtlog
import win32api, win32gui
import win32con, winerror
import servicemanager
import sys
import vypis
import signal
import time
import os
from datetime import datetime
import Pyro4
import socket
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request

typPriorita = {"uziv":1,"Mbus":2,"Rbus":3,"Pbus":4}
stanica = "Košice AS"
vyhlasXminPred = 15
vyhlasXminPredDruhy = 7
prichadzaVyhlasXminPred = 3
hnedOdideLimit = 0
data = data.Data()
vypis = vypis.Vypis()
vypis.nastavVypis(2)

def DatumovaPlatnost(IDpodminky,obecnaPlatnost,denVTydnu):
    datumObj = datetime.now()
    datum = datumObj.strftime("%d%m%Y")
    cisloTydne = int(datumObj.strftime("%V"))
    if cisloTydne%2 == 0:
        sudy = True
        lichy = False
    else:
        sudy = False
        lichy = True

    jede = False

    if IDpodminky != "":
        #pokud je zadany rozsah platnosti
        if data.datumy[IDpodminky]["jede"] != "":
            #pokud je datum v rozsahu, anebo jede take
            if datum in data.datumy[IDpodminky]["jede"] or datum in data.datumy[IDpodminky]["jedeTake"]:
                #pokud neni svatek
                if not datum in data.svatky:
                    #pokud je splnena obecna platnost
                    if denVTydnu in obecnaPlatnost:
                        #pokud jede jen liche tydny a neni lichy
                        if data.datumy[IDpodminky]["jedeLiche"] == 1 and not lichy:
                            jede = False
                        #jinak pokud jede jen sude a neni sudy
                        elif data.datumy[IDpodminky]["jedeSude"] == 1 and not sudy:
                            jede = False
                        #jinak
                        else:
                            jede = True
                    #nebo pokud je splnena podminka jede take
                    elif datum in data.datumy[IDpodminky]["jedeTake"]:
                        #pokud jede jen liche tydny a neni lichy
                        if data.datumy[IDpodminky]["jedeLiche"] == 1 and not lichy:
                            jede = False
                        #jinak pokud jede jen sude a neni sudy
                        elif data.datumy[IDpodminky]["jedeSude"] == 1 and not sudy:
                            jede = False
                        #jinak
                        else:
                            jede = True

                #pokud je svatek
                else:
                    #pokud je obecna platnost ve svatek, nebo jede take
                    if "8" in obecnaPlatnost or datum in data.datumy[IDpodminky]["jedeTake"]:
                        #pokud jede jen liche tydny a neni lichy
                        if data.datumy[IDpodminky]["jedeLiche"] == 1 and not lichy:
                            jede = False
                        #jinak pokud jede jen sude a neni sudy
                        elif data.datumy[IDpodminky]["jedeSude"] == 1 and not sudy:
                            jede = False
                        #jinak
                        else:
                            jede = True

        #jinak pokud neni zadany rozsah platnosti
        else:
            #pokud neni svatek
            if not datum in data.svatky:
                #pokud je splnena obecna platnost
                if denVTydnu in obecnaPlatnost:
                    #pokud jede jen liche tydny a neni lichy
                    if data.datumy[IDpodminky]["jedeLiche"] == 1 and not lichy:
                        jede = False
                    #jinak pokud jede jen sude a neni sudy
                    elif data.datumy[IDpodminky]["jedeSude"] == 1 and not sudy:
                        jede = False
                    #jinak
                    else:
                        jede = True
                #nebo pokud je splnena podminka jede take
                elif datum in data.datumy[IDpodminky]["jedeTake"]:
                    #pokud jede jen liche tydny a neni lichy
                    if data.datumy[IDpodminky]["jedeLiche"] == 1 and not lichy:
                        jede = False
                    #jinak pokud jede jen sude a neni sudy
                    elif data.datumy[IDpodminky]["jedeSude"] == 1 and not sudy:
                        jede = False
                    #jinak
                    else:
                        jede = True

            #pokud je svatek
            else:
                #pokud je obecna platnost ve svatek, nebo jede take
                if "8" in obecnaPlatnost or datum in data.datumy[IDpodminky]["jedeTake"]:
                    #pokud jede jen liche tydny a neni lichy
                    if data.datumy[IDpodminky]["jedeLiche"] == 1 and not lichy:
                        jede = False
                    #jinak pokud jede jen sude a neni sudy
                    elif data.datumy[IDpodminky]["jedeSude"] == 1 and not sudy:
                        jede = False
                    #jinak
                    else:
                        jede = True

        #nejede pokud je datum v nejede
        if datum in data.datumy[IDpodminky]["nejede"]:
            jede = False
    else:
        jede = True

    return jede

class MainWindow():
    def __init__(self):
        msg_TaskbarRestart = win32gui.RegisterWindowMessage("TaskbarCreated")
        message_map = {
                msg_TaskbarRestart: self.OnRestart,
                win32con.WM_DESTROY: self.OnDestroy,
                win32con.WM_COMMAND: self.OnCommand,
                win32con.WM_USER+20 : self.OnTaskbarNotify,
        }
        # Register the Window class.
        wc = win32gui.WNDCLASS()
        hinst = wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = "AVSOB_server"
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        wc.hCursor = win32api.LoadCursor( 0, win32con.IDC_ARROW )
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = message_map # could also specify a wndproc.

        # Don't blow up if class already registered to make testing easier
        try:
            _ = win32gui.RegisterClass(wc)
        except win32gui.error as err_info:
            if err_info.winerror!=winerror.ERROR_CLASS_ALREADY_EXISTS:
                raise

        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow( wc.lpszClassName, "AVSOB server", style, \
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                0, 0, hinst, None)
        win32gui.UpdateWindow(self.hwnd)
        self._DoCreateIcons()
    def _DoCreateIcons(self):
        # Try and find a custom icon
        hinst =  win32api.GetModuleHandle(None)
        iconPathName = os.path.abspath(os.path.join( os.path.split(os.path.abspath(__file__))[0], "icon.ico" ))
        if not os.path.isfile(iconPathName):
            # Look in DLLs dir, a-la py 2.5
            iconPathName = os.path.abspath(os.path.join( os.path.split(os.path.abspath(__file__))[0], "DLLs", "icon.ico" ))
        if not os.path.isfile(iconPathName):
            # Look in the source tree.
            iconPathName = os.path.abspath(os.path.join( os.path.split(os.path.abspath(__file__))[0], "..\\PC\\icon.ico" ))
        if os.path.isfile(iconPathName):
            icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            hicon = win32gui.LoadImage(hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
        else:
            print("Ikona programu nebola nalezena!")
            hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)

        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "AVSOB server")
        try:
            win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
        except win32gui.error:
            # This is common when windows is starting, and this code is hit
            # before the taskbar has been created.
            print("Nepodarilo sa priradit ikonu exploreru, bezi vobec?")
            # but keep running anyway - when explorer starts, we get the
            # TaskbarCreated message.

    def OnRestart(self, hwnd, msg, wparam, lparam):
        self._DoCreateIcons()

    def OnDestroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0) # Terminate the app.

    def OnTaskbarNotify(self, hwnd, msg, wparam, lparam):
        if lparam==win32con.WM_LBUTTONUP:
            pass #left click
        elif lparam==win32con.WM_LBUTTONDBLCLK:
            pass #double left click
        elif lparam==win32con.WM_RBUTTONUP:
            #right click
            menu = win32gui.CreatePopupMenu()
            win32gui.AppendMenu( menu, win32con.MF_STRING, 1023, "Obnov hlasenie")
            win32gui.AppendMenu( menu, win32con.MF_STRING, 1024, "Zastav hlasenie")
            win32gui.AppendMenu( menu, win32con.MF_STRING, 1025, "Ukonci aplikaciu" )
            pos = win32gui.GetCursorPos()
            # See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winui/menus_0hdi.asp
            win32gui.SetForegroundWindow(self.hwnd)
            win32gui.TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, self.hwnd, None)
            win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
        return 1

    def OnCommand(self, hwnd, msg, wparam, lparam):
        id = win32api.LOWORD(wparam)
        if id == 1023:
            # import win32gui_dialog
            # win32gui_dialog.DemoModal()
            M.soundAPI.obnovHlasenie()
        elif id == 1024:
            M.soundAPI.zastavHlasenie()
        elif id == 1025:
            vypis.vypis("Ukoncuji vlakno hlasenie!")
            vypis.vypis(M.soundAPI.zastavHlasenie())
            vypis.vypis(M.server.forceStop())
            M.stop = True
            win32gui.DestroyWindow(self.hwnd)
        else:
            print("Unknown command -", id)

class Main():
    def __init__(self):
        self.soundAPI = soundAPI.soundAPI(data)
        self.vyhlas = Vyhlas()
        vypis.vypis('Inicializacia aplikacie!',1)
        self.server = HTTP_handler()
        # self.soundAPI.vyhlas(["hlas/SK/start.wav",data.poleHlasenie["SK"]["stanice_umisteni"]])
        hostname = socket.gethostname()
        self.ip = socket.gethostbyname(hostname)
        vypis.vypis('Server bezi na adrese '+self.ip+':8081!',1)
        self.stop = False

    def beh(self, 
            # objektSluzby
            ):
        self.vyhlas.BudePristaveny(self,"Mbus","Eurobus",9,"14:06",13,False)
        # self.vyhlas.BudePristaveny(self,"Mbus",2,19,"19:43",13,False,True)
        # self.vyhlas.Stoji(self,"Mbus",2,1,19,"19:43",13,False)
        self.vyhlas.Stoji(self,"Pbus","Eurobus",1,9,"19:43",13,False,True)
        # self.vyhlas.OdidePriNast(self,"Mbus",2,19,"19:43",13,False)
        self.vyhlas.OdidePriNast(self,"Pbus","Eurobus",9,"14:06",13,False,True)
        self.vyhlas.PrideTranzitny(self,"Mbus","Eurobus",1,19,"19:41","19:43",13,False)
        # self.vyhlas.PrideTranzitny(self,"Mbus","Eurobus",1,9,"19:41","19:43",13,False,True)
        # self.vyhlas.PrichadzaTranzitny(self,"Rbus","Eurobus",1,9,"14:06","14:08",13,False)
        # self.vyhlas.PrichadzaTranzitny(self,"Mbus",2,1,19,"19:41","19:43",13,False,True)
        # self.vyhlas.PrisielTranzitny(self,"Mbus",2,1,19,"19:41","19:43",13,False,False,False)
        # self.vyhlas.PrisielTranzitny(self,"Mbus",2,1,19,"19:41","19:43",13,False,True,False)
        # self.vyhlas.PrisielTranzitny(self,"Mbus",2,1,19,"19:41","19:43",13,False,False,True)
        # self.vyhlas.PrisielTranzitny(self,"Mbus",2,1,19,"19:41","19:43",13,False,True,True)
        # self.vyhlas.PrideKonciaci(self,"Rbus","Eurobus",1,"14:06",13,False)
        # self.vyhlas.PrideKonciaci(self,"Mbus",2,1,"19:43",13,False,True)
        # self.vyhlas.PrichadzaKonciaci(self,"Mbus",2,1,13,False)
        # self.vyhlas.PrichadzaKonciaci(self,"Mbus",2,1,13,False,True)
        # self.vyhlas.PrisielKonciaci(self,"Mbus","Eurobus",1,"14:06",13,False)
        # self.vyhlas.PrisielKonciaci(self,"Mbus",2,1,"19:41",13,False,True)
        while not self.stop:
            #----------CASY---------
                #aktualny cas
                localtime = time.localtime(time.time())
                denVTydnu = str(localtime.tm_wday)

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
                vyhlasPrich = data.spojeDlaCasuPrichPride.pop(casPride,[])

                #pocetSpojuKVyhlaseni
                pocetSpojuPrich = len(vyhlasPrich)

                #vyhlasovani prichozich spoju
                for spoj in vyhlasPrich:
                    spoj = data.spoje[spoj]

                    #zisti, ci dnes spoj ide
                    jedeDnes = DatumovaPlatnost(spoj["IDplatnosti"],spoj["obecnaPlatnost"],denVTydnu)

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
                vyhlasPrichDruhy = data.spojeDlaCasuPrichPrideDruhy.pop(casPrideDruhy,[])

                #vyhlasovani prichozich spoju podruhe
                for spoj in vyhlasPrichDruhy:
                    spoj = data.spoje[spoj]
                    zkracene = True

                    #zisti, ci dnes spoj ide
                    jedeDnes = DatumovaPlatnost(spoj["IDplatnosti"],spoj["obecnaPlatnost"],denVTydnu)

                    #pokial ano,
                    if jedeDnes:

                        #pokial konci hlas konciaci
                        if spoj["konci"]:
                            self.vyhlas.PrideKonciaci(self,spoj["typ"],spoj["IDdopravca"],spoj["IDtrasyPrichod"],spoj["casPrichodu"],spoj["nastupiste"],spoj["hlasEN"],zkracene)
                        #pokial nekonci
                        else:
                            self.vyhlas.PrideTranzitny(self,spoj["typ"],spoj["IDdopravca"],spoj["IDtrasyPrichod"],spoj["IDtrasyOdchod"],spoj["casPrichodu"],spoj["casOdchodu"],spoj["nastupiste"],spoj["hlasEN"],zkracene)


                #pole prichadza spoju k vyhlaseni
                vyhlasPrichadza = data.spojeDlaCasuPrichPrichadza.pop(casPrichadza,[])

                #pocetSpojuKVyhlaseni
                pocetSpojuPrichadza = len(vyhlasPrichadza)

                #vyhlasovani prichadza spoju
                for spoj in vyhlasPrichadza:
                    spoj = data.spoje[spoj]

                    #zisti, ci dnes spoj ide
                    jedeDnes = DatumovaPlatnost(spoj["IDplatnosti"],spoj["obecnaPlatnost"],denVTydnu)

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
                vyhlasPrisel = data.spojeDlaCasuPrichPrisiel.pop(cas,[])

                #pocetSpojuKVyhlaseni
                pocetSpojuPrisel = len(vyhlasPrisel)

                #vyhlasovani prisiel spoju
                for spoj in vyhlasPrisel:
                    spoj = data.spoje[spoj]

                    #zisti, ci dnes spoj ide
                    jedeDnes = DatumovaPlatnost(spoj["IDplatnosti"],spoj["obecnaPlatnost"],denVTydnu)

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
                vyhlasBudePristaveny = data.spojeDlaCasuOdchBudePristaveny.pop(casPride,[])

                #pocetSpojuKVyhlaseni
                pocetSpojuBudePristaveny = len(vyhlasBudePristaveny)

                #vyhlasovani pristavovanych spoju
                for spoj in vyhlasBudePristaveny:
                    spoj = data.spoje[spoj]

                    #zisti, ci dnes spoj ide
                    jedeDnes = DatumovaPlatnost(spoj["IDplatnosti"],spoj["obecnaPlatnost"],denVTydnu)

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
                vyhlasBudePristavenyDruhy = data.spojeDlaCasuOdchBudePristavenyDruhe.pop(casPrideDruhy,[])

                #vyhlasovani pristavovanych spoju podruhe
                for spoj in vyhlasBudePristavenyDruhy:
                    spoj = data.spoje[spoj]
                    zkracene = True

                    #zisti, ci dnes spoj ide
                    jedeDnes = DatumovaPlatnost(spoj["IDplatnosti"],spoj["obecnaPlatnost"],denVTydnu)

                    #pokial ano, vyhlas
                    if jedeDnes:
                        self.vyhlas.BudePristaveny(self,spoj["typ"],spoj["IDdopravca"],spoj["IDtrasyOdchod"],spoj["casOdchodu"],spoj["nastupiste"],spoj["hlasEN"],zkracene)
            

    def vratPoleZastavok(self,trasaID,zkraceny=False,prichodova=False):
        if zkraceny:
            if prichodova:
                return([data.trasy[trasaID][0]])
            else:
                return([data.trasy[trasaID][-1]])            
        else:
            poleZastavok = []
            for zastavka in data.trasy[trasaID]:
                poleZastavok.append(zastavka)
            return poleZastavok

class Vyhlas():
    def BudePristaveny(self,objektMain,typ,spolocnost,trasa,odchod,nastupiste,vAJ,zkraceny=False):
        zahlasSubory = []

        zahlasSubory.append(data.poleHlasenie["SK"]["typ"][typ])
        # typ autobusu

        zahlasSubory.append(data.poleHlasenie["SK"]["dopravcia"][str(spolocnost)])
        # spolocnost

        zahlasSubory.append(data.poleHlasenie["SK"]["slova"]["smer"])
        # smer

        poleZastavok = objektMain.vratPoleZastavok(trasa,zkraceny)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["pravidelnyOdchod"])
        # pravidelny odchod

        hodiny,minuty = odchod.split(":")
        zahlasSubory.append(data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        zahlasSubory.append(data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # cas odchodu

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["budePristaveny"])
        # bude pristaveny

        zahlasSubory.append(data.poleHlasenie["SK"]["nastupiste"]["k"+str(nastupiste)])
        # nastupiste

        objektMain.soundAPI.pridejHlaseni([zahlasSubory,typPriorita[typ]])

    def Stoji(self,objektMain,typ,spolocnost,trasaPrichod,trasaOdchod,odchod,nastupiste,vAJ,zkraceny=False):
        zahlasSubory = []

        zahlasSubory.append(data.poleHlasenie["SK"]["typ"][typ])
        # typ autobusu

        zahlasSubory.append(data.poleHlasenie["SK"]["dopravcia"][str(spolocnost)])
        # spolocnost

        zahlasSubory.append(data.poleHlasenie["SK"]["slova"]["smer"])
        # smer

        poleZastavok = objektMain.vratPoleZastavok(trasaPrichod,zkraceny)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky odchod

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["pravidelnyOdchod"])
        # pravidelny odchod

        hodiny,minuty = odchod.split(":")
        zahlasSubory.append(data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        zahlasSubory.append(data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # cas odchodu

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["budePristaveny"])
        # bude pristaveny

        zahlasSubory.append(data.poleHlasenie["SK"]["nastupiste"]["k"+str(nastupiste)])
        # nastupiste

        objektMain.soundAPI.pridejHlaseni([zahlasSubory,typPriorita[typ]])

    def OdidePriNast(self,objektMain,typ,spolocnost,trasa,odchod,nastupiste,vAJ,zkraceny=False):
        zahlasSubory = []

        zahlasSubory.append(data.poleHlasenie["SK"]["typ"][typ])
        # typ autobusu

        zahlasSubory.append(data.poleHlasenie["SK"]["dopravcia"][str(spolocnost)])
        # spolocnost

        zahlasSubory.append(data.poleHlasenie["SK"]["slova"]["smer"])
        # smer

        poleZastavok = objektMain.vratPoleZastavok(trasa,zkraceny)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["pravidelnyOdchod"])
        # pravidelny odchod

        hodiny,minuty = odchod.split(":")
        zahlasSubory.append(data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        zahlasSubory.append(data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # cas odchodu

        zahlasSubory.append(data.poleHlasenie["SK"]["slova"]["stoji"])
        # "stoji"

        zahlasSubory.append(data.poleHlasenie["SK"]["nastupiste"]["na"+str(nastupiste)])
        # nastupiste

        zahlasSubory.append(data.poleHlasenie["SK"]["typ"]["Pbus"])
        # "autobus"

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["pripravenyOdchod"])
        # "je pripraveny na odchod"

        objektMain.soundAPI.pridejHlaseni([zahlasSubory,typPriorita[typ]])

    def PrideTranzitny(self,objektMain,typ,spolocnost,trasaPrichod,trasaOdchod,prichod,odchod,nastupiste,vAJ,zkraceny=False):
        zahlasSubory = []

        zahlasSubory.append(data.poleHlasenie["SK"]["typ"][typ])
        # typ autobusu

        zahlasSubory.append(data.poleHlasenie["SK"]["dopravcia"][str(spolocnost)])
        # spolocnost

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["zoSmeru"])
        # zo smeru

        poleZastavok = objektMain.vratPoleZastavok(trasaPrichod,zkraceny,True)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["pravidelnyPrichod"])
        # pravidelny prichod

        hodiny,minuty = prichod.split(":")
        zahlasSubory.append(data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        zahlasSubory.append(data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # cas prichodu

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["ktoryDalejPokracuje"])
        # ktory dalej pokracuje smer

        poleZastavok = objektMain.vratPoleZastavok(trasaOdchod,zkraceny)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["pravidelnyOdchod"])
        # pravidelny odchod

        hodiny,minuty = odchod.split(":")
        zahlasSubory.append(data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        zahlasSubory.append(data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # cas odchodu

        zahlasSubory.append(data.poleHlasenie["SK"]["slova"]["pride"])
        # "pride"

        zahlasSubory.append(data.poleHlasenie["SK"]["nastupiste"]["k"+str(nastupiste)])
        # nastupiste

        objektMain.soundAPI.pridejHlaseni([zahlasSubory,typPriorita[typ]])

    def PrichadzaTranzitny(self,objektMain,typ,spolocnost,trasaPrichod,trasaOdchod,prichod,odchod,nastupiste,vAJ,zkraceny=False):
        zahlasSubory = []

        zahlasSubory.append(data.poleHlasenie["SK"]["typ"][typ])
        # typ autobusu

        zahlasSubory.append(data.poleHlasenie["SK"]["dopravcia"][str(spolocnost)])
        # spolocnost

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["zoSmeru"])
        # zo smeru

        poleZastavok = objektMain.vratPoleZastavok(trasaPrichod,zkraceny,True)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["pravidelnyPrichod"])
        # pravidelny prichod

        hodiny,minuty = prichod.split(":")
        zahlasSubory.append(data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        zahlasSubory.append(data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # cas prichodu

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["ktoryDalejPokracuje"])
        # ktory dalej pokracuje smer

        poleZastavok = objektMain.vratPoleZastavok(trasaOdchod,zkraceny)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky

        # zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["pravidelnyOdchod"])
        # # pravidelny odchod

        # hodiny,minuty = odchod.split(":")
        # zahlasSubory.append(data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        # zahlasSubory.append(data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # # cas odchodu

        zahlasSubory.append(data.poleHlasenie["SK"]["slova"]["prichadza"])
        # "prichadza"

        zahlasSubory.append(data.poleHlasenie["SK"]["nastupiste"]["k"+str(nastupiste)])
        # nastupiste

        objektMain.soundAPI.pridejHlaseni([zahlasSubory,typPriorita[typ]])

    def PrisielTranzitny(self,objektMain,typ,spolocnost,trasaPrichod,trasaOdchod,prichod,odchod,nastupiste,vAJ,zkraceny=False,hnedOdide=False):
        zahlasSubory = []

        zahlasSubory.append(data.poleHlasenie["SK"]["stanice_umisteni"])
        #stanice

        zahlasSubory.append(data.poleHlasenie["SK"]["typ"][typ])
        # typ autobusu

        zahlasSubory.append(data.poleHlasenie["SK"]["dopravcia"][str(spolocnost)])
        # spolocnost

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["zoSmeru"])
        # zo smeru

        poleZastavok = objektMain.vratPoleZastavok(trasaPrichod,zkraceny,True)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky

        zahlasSubory.append(data.poleHlasenie["SK"]["slova"]["prisiel"])
        # "prisiel"

        zahlasSubory.append(data.poleHlasenie["SK"]["nastupiste"]["k"+str(nastupiste)])
        # nastupiste

        zahlasSubory.append(data.poleHlasenie["SK"]["typ"]["Pbus"])
        # "autobus"

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["dalejPokracuje"])
        # dalej pokracuje smer

        poleZastavok = objektMain.vratPoleZastavok(trasaOdchod,zkraceny)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["pravidelnyOdchod"])
        # pravidelny odchod

        hodiny,minuty = odchod.split(":")
        zahlasSubory.append(data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        zahlasSubory.append(data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # cas odchodu

        zahlasSubory.append(data.poleHlasenie["SK"]["nastupiste"]["na"+str(nastupiste)])
        # nastupiste

        if hnedOdide:
            zahlasSubory.append(data.poleHlasenie["SK"]["typ"]["Pbus"])
            # "autobus"

            zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["pripravenyOdchod"])
            # "je pripraveny na odchod"

        objektMain.soundAPI.pridejHlaseni([zahlasSubory,typPriorita[typ]])

    def PrideKonciaci(self,objektMain,typ,spolocnost,trasaPrichod,prichod,nastupiste,vAJ,zkraceny=False):
        zahlasSubory = []

        zahlasSubory.append(data.poleHlasenie["SK"]["typ"][typ])
        # typ autobusu

        zahlasSubory.append(data.poleHlasenie["SK"]["dopravcia"][str(spolocnost)])
        # spolocnost

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["zoSmeru"])
        # zo smeru

        poleZastavok = objektMain.vratPoleZastavok(trasaPrichod,zkraceny,True)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["pravidelnyPrichod"])
        # pravidelny prichod

        hodiny,minuty = prichod.split(":")
        zahlasSubory.append(data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        zahlasSubory.append(data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # cas prichodu

        zahlasSubory.append(data.poleHlasenie["SK"]["slova"]["pride"])
        # "pride"

        zahlasSubory.append(data.poleHlasenie["SK"]["nastupiste"]["k"+str(nastupiste)])
        # nastupiste

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["autobusKonci"])
        # "autobus tu jazdu konci"

        objektMain.soundAPI.pridejHlaseni([zahlasSubory,typPriorita[typ]])

    def PrichadzaKonciaci(self,objektMain,typ,spolocnost,trasaPrichod,nastupiste,vAJ,zkraceny=False):
        zahlasSubory = []

        zahlasSubory.append(data.poleHlasenie["SK"]["typ"][typ])
        # typ autobusu

        zahlasSubory.append(data.poleHlasenie["SK"]["dopravcia"][str(spolocnost)])
        # spolocnost

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["zoSmeru"])
        # zo smeru

        poleZastavok = objektMain.vratPoleZastavok(trasaPrichod,zkraceny,True)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky

        # zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["pravidelnyPrichod"])
        # # pravidelny prichod

        # hodiny,minuty = prichod.split(":")
        # zahlasSubory.append(data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        # zahlasSubory.append(data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # # cas prichodu

        # zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["ktoryDalejPokracuje"])
        # # ktory dalej pokracuje smer

        # zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["pravidelnyOdchod"])
        # # pravidelny odchod

        # hodiny,minuty = odchod.split(":")
        # zahlasSubory.append(data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        # zahlasSubory.append(data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # # cas odchodu

        zahlasSubory.append(data.poleHlasenie["SK"]["slova"]["prichadza"])
        # "prichadza"

        zahlasSubory.append(data.poleHlasenie["SK"]["nastupiste"]["k"+str(nastupiste)])
        # nastupiste

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["autobusKonci"])
        # "autobus tu jazdu konci"

    def PrisielKonciaci(self,objektMain,typ,spolocnost,trasaPrichod,prichod,nastupiste,vAJ,zkraceny=False):
        zahlasSubory = []

        zahlasSubory.append(data.poleHlasenie["SK"]["stanice_umisteni"])
        #stanice

        zahlasSubory.append(data.poleHlasenie["SK"]["typ"][typ])
        # typ autobusu

        zahlasSubory.append(data.poleHlasenie["SK"]["dopravcia"][str(spolocnost)])
        # spolocnost

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["zoSmeru"])
        # zo smeru

        poleZastavok = objektMain.vratPoleZastavok(trasaPrichod,zkraceny,True)
        lastZastavkaID = len(poleZastavok)-1

        for i, zastavka in enumerate(poleZastavok):
            if i == lastZastavkaID and i != 0:
                zahlasSubory.append(data.poleHlasenie["SK"]["slova"]["a"])
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
            else:
                zahlasSubory.append(data.poleHlasenie["SK"]["stanice"][zastavka])
        # zastavky

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["pravidelnyPrichod"])
        # pravidelny prichod

        hodiny,minuty = prichod.split(":")
        while len(minuty) < 2:
            minuty = "0"+minuty
            
        zahlasSubory.append(data.poleHlasenie["SK"]["hodiny"][int(hodiny)])
        zahlasSubory.append(data.poleHlasenie["SK"]["minuty"][str(minuty)])
        # cas prichodu

        zahlasSubory.append(data.poleHlasenie["SK"]["slova"]["prisiel"])
        # "prisiel"

        zahlasSubory.append(data.poleHlasenie["SK"]["nastupiste"]["k"+str(nastupiste)])
        # nastupiste

        zahlasSubory.append(data.poleHlasenie["SK"]["vety"]["autobusKonciVystupte"])
        # "autobus tu jazdu konci"

        objektMain.soundAPI.pridejHlaseni([zahlasSubory,typPriorita[typ]])

class HTTP_handler():
    def __init__(self):
        self.stop = False
        adresa = ('127.0.0.1', 8081)
        self.server = HTTPServer(adresa, WebServerClass)
        self.vlaknoHTTP = Thread(target=self.serve)
        self.vlaknoHTTP.start()

    def serve(self):
        while not self.stop:
            self.server.handle_request()
        raise SystemExit

    def forceStop(self):
        self.stop = True
        vypis.vypis('Ukoncuji beh HTTP serveru!',1)
        urllib.request.urlopen("http://127.0.0.1:8081")
        return("WEBSERVER EXITED!")

class WebServerClass(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            subor, koncovka = os.path.splitext(self.path)
            subor = subor.replace("/", "")
        except:
            subor = ""
            koncovka = ""

        if subor == "":
            #Odosli odpoved 200 - success
            self.send_response(200)

            #Odosli head zobrazovane stranky
            self.send_header('Content-type','text/html')
            self.end_headers()

            stringSpoje = ""
            spojePocet = 0

            localtime = time.localtime(time.time())
            denVTydnu = str(localtime.tm_wday)

            casMM = str(localtime.tm_min)
            while len(casMM) < 2:
                casMM = "0"+casMM

            casHH = str(localtime.tm_hour)
            while len(casHH) < 2:
                casHH = "0"+casHH
                
            cas = int(casHH+casMM)

            for spoj in data.spojeSerazene:
                spoj = data.spoje[spoj]
                
                stringPrichod = ""
                trasaPrichod = spoj["IDtrasyPrichod"]
                stringOdchod = ""
                trasaOdchod = spoj["IDtrasyOdchod"]

                if trasaPrichod != 0:
                    trasaPrichod = data.trasy[trasaPrichod]
                    stringPrichod = " - ".join(str(data.zastavky[v]) for v in trasaPrichod)
                else:
                    trasaPrichod = {}

                if trasaOdchod != 0:
                    trasaOdchod = data.trasy[trasaOdchod]
                    stringOdchod = " - ".join(str(data.zastavky[v]) for v in trasaOdchod)
                else:
                    trasaOdchod = {}

                if spoj["casOdchodu"] == 0:
                    if int(str(spoj['casPrichodu']).replace(":", "")) < cas:
                        continue
                elif int(str(spoj['casOdchodu']).replace(":", "")) < cas:
                    continue
                elif not DatumovaPlatnost(spoj["IDplatnosti"],spoj["obecnaPlatnost"],denVTydnu):
                    continue
                
                spojePocet = spojePocet + 1
                if spojePocet > 10:
                    break

                if spoj["casPrichodu"] == 0:
                    stringSpoje = stringSpoje + '''<tr>
                                                    <td>'''+str(spoj["linka"])+'''</td>
                                                    <td></td>
                                                    <td></td>
                                                    <td><marquee>'''+stringOdchod+'''</marquee></td>
                                                    <td>'''+str(spoj["casOdchodu"])+'''</td>
                                                    <td>'''+str(spoj["nastupiste"])+'''</td>
                                                    <td>*</td>
                                                </tr>'''
                elif spoj["casOdchodu"] == 0:
                    stringSpoje = stringSpoje + '''<tr>
                                                    <td>'''+str(spoj["linka"])+'''</td>
                                                    <td><marquee>'''+stringPrichod+'''</marquee></td>
                                                    <td>'''+str(spoj["casPrichodu"])+'''</td>
                                                    <td></td>
                                                    <td></td>
                                                    <td>'''+str(spoj["nastupiste"])+'''</td>
                                                    <td>*</td>
                                                </tr>'''
                else:
                    stringSpoje = stringSpoje + '''<tr>
                                                    <td>'''+str(spoj["linka"])+'''</td>
                                                    <td><marquee>'''+stringOdchod+'''</marquee></td>
                                                    <td>'''+str(spoj["casPrichodu"])+'''</td>
                                                    <td><marquee>'''+stringOdchod+'''</marquee></td>
                                                    <td>'''+str(spoj["casOdchodu"])+'''</td>
                                                    <td>'''+str(spoj["nastupiste"])+'''</td>
                                                    <td>*</td>
                                                </tr>'''                            
            if spojePocet < 10:
                localtime = time.localtime(time.time()+24*60*60)
                denVTydnu = str(localtime.tm_wday)
                for spoj in data.spojeSerazene:
                    spoj = data.spoje[spoj]
                    
                    stringPrichod = ""
                    trasaPrichod = spoj["IDtrasyPrichod"]
                    stringOdchod = ""
                    trasaOdchod = spoj["IDtrasyOdchod"]

                    if not DatumovaPlatnost(spoj["IDplatnosti"],spoj["obecnaPlatnost"],denVTydnu):
                        continue

                    if trasaPrichod != 0:
                        trasaPrichod = data.trasy[trasaPrichod]
                        stringPrichod = " - ".join(str(data.zastavky[v]) for v in trasaPrichod)
                    else:
                        trasaPrichod = {}

                    if trasaOdchod != 0:
                        trasaOdchod = data.trasy[trasaOdchod]
                        stringOdchod = " - ".join(str(data.zastavky[v]) for v in trasaOdchod)
                    else:
                        trasaOdchod = {}
                    
                    spojePocet = spojePocet + 1
                    if spojePocet > 10:
                        break

                    if spoj["casPrichodu"] == 0:
                        stringSpoje = stringSpoje + '''<tr>
                                                        <td>'''+str(spoj["linka"])+'''</td>
                                                        <td></td>
                                                        <td></td>
                                                        <td><marquee>'''+stringOdchod+'''</marquee></td>
                                                        <td>'''+str(spoj["casOdchodu"])+'''</td>
                                                        <td>'''+str(spoj["nastupiste"])+'''</td>
                                                        <td>*</td>
                                                    </tr>'''
                    elif spoj["casOdchodu"] == 0:
                        stringSpoje = stringSpoje + '''<tr>
                                                        <td>'''+str(spoj["linka"])+'''</td>
                                                        <td><marquee>'''+stringPrichod+'''</marquee></td>
                                                        <td>'''+str(spoj["casPrichodu"])+'''</td>
                                                        <td></td>
                                                        <td></td>
                                                        <td>'''+str(spoj["nastupiste"])+'''</td>
                                                        <td>*</td>
                                                    </tr>'''
                    else:
                        stringSpoje = stringSpoje + '''<tr>
                                                        <td>'''+str(spoj["linka"])+'''</td>
                                                        <td><marquee>'''+stringOdchod+'''</marquee></td>
                                                        <td>'''+str(spoj["casPrichodu"])+'''</td>
                                                        <td><marquee>'''+stringOdchod+'''</marquee></td>
                                                        <td>'''+str(spoj["casOdchodu"])+'''</td>
                                                        <td>'''+str(spoj["nastupiste"])+'''</td>
                                                        <td>*</td>
                                                    </tr>'''    

            #Odosli telo zpravy
            message = '''<!DOCTYPE html>
                <html lang="cs">
                    <head>
                        <title>AVSOB</title>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <meta name="Description" CONTENT="Web rozhraní aplikace AVSOB.">
                        <script type="text/javascript" src="jquery-3.3.1.min.js"></script>
                        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
                        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
                        <script src="moment.js"></script>
                        <script>
                            $(document).ready(function() {
                                console.log("Stránka načtená!");
                                document.getElementById("page_content").style.width="100%";
                                setTimeout(blikej, 1000);
                                setTimeout(function(){location.reload()}, 60000);
                            });
                        </script>
                        <style>
                            .bg-hlavicka { 
                                background-color: #ffffff;
                                color: #575757;
                            }
                            .prichody {
                                text-align: left;
                            }
                            h1 {
                                font-size: 72px;
                            }
                            .table-hover {
                                font-size: 30px;
                            }
                            .blink{
                                animation: blink 1s infinite;
                            }
                            @keyframes blink{
                                0%{opacity: 1;}
                                75%{opacity: 1;}
                                76%{ opacity: 0;}
                                100%{opacity: 0;}
                            }
                        </style>
                    </head>
                    <body>
                        <div id="page_content" class="container-fluid text-center" style="width: 70%;">
                            <div id="hlavicka" class="container-fluid bg-hlavicka">
                                <div class="container-fluid">
                                    <h1>
                                        <div id="nadpis">Stanice TEST</div>
                                    </h1>
                                </div>
                            </div>
                            <div id="prichody" class="prichody">
                                <div class="table-responsive">
                                    <table id="tabulkaAutobusy" class="table table-hover">
                                        <thead class="thead-dark">
                                            <tr>
                                                <th scope="col">Linka</th>
                                                <th scope="col">Zo smeru</th>
                                                <th scope="col">Príchod</th>
                                                <th scope="col">Smer</th>
                                                <th scope="col">Odchod</th>
                                                <th scope="col">Nástupiste</th>
                                                <th scope="col">Meskanie</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            '''+stringSpoje+'''
                                            <tr>
                                                <td></td>
                                                <td></td>
                                                <td></td>
                                                <td></td>
                                                <td></td>
                                                <td></td>
                                                <td></td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                            <script>
                                function blikej() {
                                    var table = document.getElementById("tabulkaAutobusy");
                                    var rows = table.getElementsByTagName("tr");
                                    for (i = 0; i < rows.length; i++) {
                                        var currentRow = rows[i];
                                        var cell = currentRow.getElementsByTagName("td")[4];
                                        if (cell && cell.innerHTML != "") {
                                            var casOdjezd = moment(cell.innerHTML, "hh:mm");
                                            if (casOdjezd <= moment()) {
                                                cell.className = "blink";
                                            }
                                        }
                                    }
                                }
                            </script>
                            <div id="footer" class="navbar navbar-fixed-bottom">
                                <big>Informačný systém AVSOB&copy; | Made by URBANO 2018</big>
                            </div>
                        </div>
                    </body>
                </html>'''
        else:
            try:
                with open(subor+koncovka, 'r') as f:
                    #Odosli odpoved 200 - success
                    self.send_response(200)

                    message = f.read()

                    #Odosli head zobrazovane stranky
                    try:
                        self.send_header('Content-type',self.extensions_map[koncovka.lower])
                    except:
                        self.send_header('Content-type','')

                    self.end_headers()
            except:
                #Odosli odpoved 404 - not found
                self.send_response(404)
                return

        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
            
        return

def guiThreadFnc():
    w = MainWindow()
    win32gui.PumpMessages()

if __name__ == '__main__':
    M = Main()
    guiThread = Thread(target=guiThreadFnc)
    guiThread.start()
    M.beh()
