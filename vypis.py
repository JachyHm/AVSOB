import time
import win32evtlogutil
import win32evtlog
import servicemanager
from colorama import init, Fore, Style
init()

class Vypis():
    def nastavVypis(self,level):
        self.levelVypis = level

    def vypis(self,zprava,level=1,konec=False,start=False):
        if level <= self.levelVypis:
            log = open("AVSOB.log","a")
            levelSlovnik = {1:"INFO: ",2:"DEBUG: ",0:"ERROR: "}
            if start:
                print(Fore.GREEN+"-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-")
                print("-*-*-*-*-*-*-START APLIKACE AVSOB-*-*-*-*-*-*-*-*-*")
                print("-*-*-*-*-*-*-VERZE "+zprava)
                print(time.strftime("%H:%M:%S ")+"ZAHAJENI INICIALIZACE!"+Style.RESET_ALL)
                log.write("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-\n")
                log.write("-*-*-*-*-*-*-START APLIKACE AVSOB-*-*-*-*-*-*-*-*-*\n")
                log.write("-*-*-*-*-*-*-VERZE "+zprava+"\n")
                log.write(time.strftime("%H:%M:%S ")+"ZAHAJENI INICIALIZACE!\n")
            # elif not konec:
            else:
                # win32evtlogutil.ReportEvent(
                #                             "AVSOB", # Application name
                #                             win32evtlog.EVENTLOG_INFORMATION_TYPE, # Event ID
                #                             0, # Event category
                #                             win32evtlog.EVENTLOG_INFORMATION_TYPE,
                #                             ("AVSOB", time.strftime("%H:%M:%S ")+levelSlovnik[level]+str(zprava)))

                if level == 0:
                    print(Fore.RED+time.strftime("%H:%M:%S ")+levelSlovnik[level]+str(zprava)+Style.RESET_ALL)
                elif level == 1:
                    print(Fore.YELLOW+time.strftime("%H:%M:%S ")+levelSlovnik[level]+str(zprava)+Style.RESET_ALL)
                else:
                    print(Fore.CYAN+time.strftime("%H:%M:%S ")+levelSlovnik[level]+str(zprava)+Style.RESET_ALL)

                log.write(time.strftime("%H:%M:%S ")+levelSlovnik[level]+str(zprava)+"\n")
            # else:
            #     print(time.strftime("%H:%M:%S ")+levelSlovnik[level]+str(zprava))
            #     log.write(time.strftime("%H:%M:%S ")+levelSlovnik[level]+str(zprava)+"\n")
            log.close()