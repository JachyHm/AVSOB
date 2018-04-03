import soundAPI

def main():
    soundAPIobj = soundAPI.soundAPI()
    soundAPIobj.pridejHlaseni([["wav_sk/K/MBus.wav","wav_sk/D/dpmk.wav","wav_sk/S/pp.wav","wav_sk/H/1.wav","wav_sk/M2/13.wav","wav_sk/S/prich.wav","wav_sk/Kol/naka30.wav","wav_sk/S/vtjkv.wav"],2])
    soundAPIobj.pridejHlaseni([["wav_sk/D/Wagon Slovakia.WAV","wav_sk/S/pp.wav","wav_sk/H/11.wav","wav_sk/M2/6.wav","wav_sk/S/prich.wav","wav_sk/Kol/naka21.wav","wav_sk/S/vtjkv.wav"],1])
    soundAPIobj.pridejHlaseni([["wav_sk/K/bus.WAV","wav_sk/D/dpmk.wav","wav_sk/S/pp.wav","wav_sk/H/19.wav","wav_sk/M2/27.wav","wav_sk/S/prich.wav","wav_sk/Kol/naka39.wav","wav_sk/S/vtjkv.wav"],4])
    soundAPIobj.pridejHlaseni([["wav_sk/K/RBus.WAV","wav_sk/D/dpmk.wav","wav_sk/S/pp.wav","wav_sk/H/21.wav","wav_sk/M2/19.wav","wav_sk/S/prich.wav","wav_sk/Kol/naka18.wav","wav_sk/S/vtjkv.wav"],3])

if __name__ == "__main__": main()