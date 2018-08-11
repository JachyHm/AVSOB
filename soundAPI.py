"""API hlasenie pre AVSOB"""

import pyaudio
import wave
import sys
import time
import vypis
import threading
import socket
from operator import itemgetter
import signal

# definicia dlzky chunku. Nesmie v zadnom pripade prekrocit 1024 bytes!
CHUNK = 4096
frames = []

class VOIP():
    def __init__(self):
        self.FORMAT = pyaudio.paInt16
        self.CHUNK = 1024
        self.CHANNELS = 2
        self.RATE = 44100
        self.stop = False
        self.pVOIP = pyaudio.PyAudio()

    def start(self):
        self.stop = False
        Ts = threading.Thread(target = self.udpStream)
        Ts.start()
        Tp = threading.Thread(target = self.play)
        Tp.start()

    def udpStream(self):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.bind(("127.0.0.1", 46099))

        while not self.stop:
            soundData, addr = udp.recvfrom(self.CHUNK * self.CHANNELS * 2)
            frames.append(soundData)

        udp.close()
    
    def play(self):
        self.BUFFER = 10
        while not self.stop:
            if len(frames) == self.BUFFER:
                # M.soundAPI.zastavHlasenie()
                streamVOIP = self.pVOIP.open(format=self.FORMAT,
                                channels = self.CHANNELS,
                                rate = self.RATE,
                                output = True,
                                frames_per_buffer = self.CHUNK,
                                )
                while len(frames) > 0:
                    streamVOIP.write(frames.pop(0), self.CHUNK)
                streamVOIP.stop_stream()
                streamVOIP.close()
                # M.soundAPI.obnovHlasenie()

class soundAPI():
    def __init__(self, objektData, prvy=True):
        # inicializacia API pre hlasenie
        self.vypis = vypis.Vypis()
        self.vypis.nastavVypis(2)
        if prvy:
            self.tabulkaHlasenia = []
        self.byloPrve = False
        self.stop = False
        #docasne cesty k znelkam
        self.objektData = objektData
        self.startHlasenie = objektData.poleHlasenie["SK"]["znelky"]["start"]
        self.konecHlasenia = objektData.poleHlasenie["SK"]["znelky"]["koniec"]
        self.medziHlasenimi = objektData.poleHlasenie["SK"]["znelky"]["medzi"]
        self.vlaknoHlaseni = threading.Thread(target=self.cyklusHlaseni)
        self.vlaknoHlaseni.start()
    
    def cyklusHlaseni(self):
        while (len(self.tabulkaHlasenia) > 0 and not self.stop):
            if self.byloPrve:
                self.byloPrve = False
                # self.vypis.vypis("Toto je prvé hlásenie vo fronte, prehravam znelku štart!",2)
                self.vyhlas([self.startHlasenie])
            # self.vypis.vypis('Hlásenie priotity '+str(self.tabulkaHlasenia[0][1]),1)
            self.vyhlas(self.tabulkaHlasenia.pop(0)[0])
            if len(self.tabulkaHlasenia) > 0:
                # self.vypis.vypis("Vo fronte sa nachádza dalšie hlásenie, prehrávám znelku medzi!",2)
                self.vyhlas([self.medziHlasenimi])
            else:
                # self.vypis.vypis("Nieje dalšie hlásenie vo fronte, prehrávám znelku koniec!",2)
                self.vyhlas([self.konecHlasenia])
            # self.vypis.vypis("Konec hlásenia!",1)
        if self.stop:
            raise SystemExit

    def pridejHlaseni(self, poleHlaseni):
        # prida hlasenie do fronty
        # hlasenie je vo formate <pole_hlasenia>[<cesty k suborom>[<cesta1>,<cesta2>..<cestan>], <typ hlasenia>]
        self.tabulkaHlasenia.append(poleHlaseni)
        self.tabulkaHlasenia = sorted(self.tabulkaHlasenia,key=itemgetter(1))
        # self.vypis.vypis("Prijaté hlásenie s prioritou "+str(poleHlaseni[1])+" je "+str(self.tabulkaHlasenia.index(poleHlaseni)+1)+". vo fronte!",2)
        if not self.vlaknoHlaseni.is_alive():
            self.byloPrve = True
            self.vlaknoHlaseni = threading.Thread(target=self.cyklusHlaseni)
            self.vlaknoHlaseni.start()
    
    def vratFrontuHlaseni(self):
        return len(self.tabulkaHlasenia)

    def zastavHlasenie(self):
        self.stop = True
        return("Vlakno hlasenie ukoncene!")

    def obnovHlasenie(self):
        self.stop = False
        self.__init__(self.objektData,False)
        
    def vyhlas(self,poleHlaseni):
        p = pyaudio.PyAudio()
        # vytvor objekt PyAudio

        for soubor in poleHlaseni:
            soubor = self.objektData.poleHlasenie["SK"]["cestaKSuborum"]+soubor
            self.vypis.vypis('Hlasim "'+soubor+'"',1)
            try:
                wf = wave.open(soubor, 'rb')
            except:
                self.vypis.vypis('Subor "'+soubor+'" nebol nalezeny!',0)
            else:

                # otvor stream
                stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                channels=wf.getnchannels(),
                                rate=wf.getframerate(),
                                output=True)

                # nacti prvy chunk
                data = wf.readframes(CHUNK)

                # prehravaj chunk dokial nieje nulovej dlzky
                while len(data) > 0:
                    if self.stop:
                        break
                    else:
                        stream.write(data)
                        data = wf.readframes(CHUNK)

                # ukonci stream
                stream.stop_stream()
                stream.close()

                if self.stop:
                    break

        # zatvor objekt PyAudia
        p.terminate()