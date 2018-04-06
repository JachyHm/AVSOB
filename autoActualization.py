import urllib.request
import shutil
import os, zipfile
import time
import sqlite3
import subprocess
try:
    dbHlasenie = sqlite3.connect(os.path.dirname(os.path.abspath(__file__))+"/data/hlasenie_SK.dat")
except sqlite3.OperationalError:
    pass
    # input("Chyba čítanie modulu hlasenie_"+jazyk+".dat")
else:
    SQLdbHlasenie = dbHlasenie.cursor()
    
SQLdbHlasenie.execute('select * from `stanice_umisteni`')
for stanica in SQLdbHlasenie.fetchall():
    IDstanice = stanica[0]

url = 'http://jachyhm.cz/AVSOB/'+str(IDstanice)+'/data.zip'
print(url)
# Download the file from `url`, save it in a temporary directory and get the
# path to it (e.g. '/tmp/tmpb48zma.txt') in the `file_name` variable:
if not os.path.exists("data/!old/"):
    os.makedirs("data/!old/")

print("Zalohovanie suborov databazie...")
try:
    shutil.move("data/datumy.dat","data/!old/datumy.dat")
    shutil.move("data/hlasenie_SK.dat","data/!old/hlasenie_SK.dat")
    shutil.move("data/spoje.dat","data/!old/spoje.dat")
    shutil.move("data/trasy.dat","data/!old/trasy.dat")
    shutil.move("data/zastavky.dat","data/!old/zastavky.dat")
except:
    pass
else:
    print("Zaloha uspesna")
print("Pripajanie k "+url)
print("Stahovanie suborov databazie...")
try:
    file_name, headers = urllib.request.urlretrieve(url)
except Exception as e:
    print(e)
    input("Pre ukoncenie zmacknite lubovolnu klavesu")
else:
    zip_ref = zipfile.ZipFile(os.path.abspath(file_name), 'r')
    print("Uspesne stazeno "+str(os.path.getsize(file_name))+" bytes")
    print("Extrahovanie suborov databazie...")
    zip_ref.extractall(os.path.join(os.path.dirname(os.path.abspath(__file__)),"data"))
    zip_ref.close()
    print("Extrahovanie dokoncene")
    print("Mazanie docasnych suborov...")
    os.remove(os.path.abspath(file_name))
    print("Mazanie kompletne")
    # time.sleep(3)

    print("Zalohovanie suborov hlasenia...")
    try:
        source = os.path.join(os.path.dirname(os.path.abspath(__file__)),"hlas","SK/")
        dest1 = os.path.join(os.path.dirname(os.path.abspath(__file__)),"hlas","SK","!old/")

        files = os.listdir(source)
        for f in files:
            shutil.move(source+f, dest1)
    except:
        pass
    else:
        print("Zaloha uspesna")
    url = 'http://jachyhm.cz/AVSOB/'+str(IDstanice)+'/hlas.zip'
    print("Pripajanie k "+url)
    print("Stahovanie suborov hlasenia...")
    try:
        file_name, headers = urllib.request.urlretrieve(url)
    except Exception as e:
        print(e)
        input("Pre ukoncenie zmacknite lubovolnu klavesu")
    else:
        zip_ref = zipfile.ZipFile(os.path.abspath(file_name), 'r')
        print("Uspesne stazeno "+str(os.path.getsize(file_name))+" bytes")
        print("Extrahovanie suborov hlasenia...")
        zip_ref.extractall(os.path.join(os.path.dirname(os.path.abspath(__file__))))
        zip_ref.close()
        print("Extrahovanie dokoncene")
        print("Mazanie docasnych suborov...")
        os.remove(os.path.abspath(file_name))
        print("Mazanie kompletne")
        for i in range(10,0,-1):
            time.sleep(1)
            print("Aktualizacia kompletna, znovu zavadim program za "+str(i)+'...')
        subprocess.call(['main install'])
        