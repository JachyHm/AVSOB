"""API hlasenie pre AVSOB"""

import pyaudio
import wave
import sys
import time
import vypis
from threading import Thread
from operator import itemgetter

# definicia dlzky chunku. Nesmie v zadnom pripade prekrocit 1024 bytes!
CHUNK = 1024

class soundAPI():
    def __init__(self):
        # inicializacia API pre hlasenie
        self.vypis = vypis.Vypis()
        self.tabulkaHlasenia = []
        self.vypis.nastavVypis(2)
        self.byloPrve = False
        #docasne cesty k znelkam
        self.startHlasenie = "wav_sk/start.wav"
        self.konecHlasenia = "wav_sk/end.wav"
        self.medziHlasenimi = "wav_sk/between.wav"
        self.vlaknoHlaseni = Thread(target=self.cyklusHlaseni)
        self.vlaknoHlaseni.start()

    def cyklusHlaseni(self):
        while (len(self.tabulkaHlasenia) > 0):
            if self.byloPrve:
                self.byloPrve = False
                self.vypis.vypis("Toto je prvé hlásenie vo fronte, prehravam znelku štart!",2)
                self.vyhlas(self, [self.startHlasenie])
            self.vypis.vypis('Hlásenie priotity '+str(self.tabulkaHlasenia[0][1]),1)
            self.vyhlas(self, self.tabulkaHlasenia.pop(0)[0])
            if len(self.tabulkaHlasenia) > 0:
                self.vypis.vypis("Vo fronte sa nachádza dalšie hlásenie, prehrávám znelku medzi!",2)
                self.vyhlas(self, [self.medziHlasenimi])
            else:
                self.vypis.vypis("Nieje dalšie hlásenie vo fronte, prehrávám znelku koniec!",2)
                self.vyhlas(self, [self.konecHlasenia])
            self.vypis.vypis("Konec hlásenia!",1)

    def pridejHlaseni(self, poleHlaseni):
        # prida hlasenie do fronty
        # hlasenie je vo formate <pole_hlasenia>[<cesty k suborom>[<cesta1>,<cesta2>..<cestan>], <typ hlasenia>]
        self.tabulkaHlasenia.append(poleHlaseni)
        self.tabulkaHlasenia = sorted(self.tabulkaHlasenia,key=itemgetter(1))
        self.vypis.vypis("Prijaté hlásenie s prioritou "+str(poleHlaseni[1])+" je "+str(self.tabulkaHlasenia.index(poleHlaseni)+1)+". vo fronte!",2)
        if not self.vlaknoHlaseni.is_alive():
            self.vlaknoHlaseni = Thread(target=self.cyklusHlaseni)
            self.vlaknoHlaseni.start()
            self.byloPrve = True
        
    @staticmethod
    def vyhlas(self,poleHlaseni):
        # vytvor objekt PyAudio
        p = pyaudio.PyAudio()

        for soubor in poleHlaseni:
            self.vypis.vypis('Hlásím "'+soubor+'"',1)
            wf = wave.open(soubor, 'rb')
            # otvor stream
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)

            # nacti prvy chunk
            data = wf.readframes(CHUNK)

            # prehravaj chunk dokial nieje nulovej dlzky
            while len(data) > 0:
                stream.write(data)
                data = wf.readframes(CHUNK)

            # ukonci stream
            stream.stop_stream()
            stream.close()

        # zatvor objekt PyAudia
        p.terminate()