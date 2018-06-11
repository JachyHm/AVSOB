import time
import win32evtlogutil
import win32evtlog
import servicemanager

class Vypis():
    def nastavVypis(self,level):
        self.levelVypis = level

    def vypis(self,zprava,level=1,konec=False):
        if level <= self.levelVypis:
            levelSlovnik = {1:"INFO: ",2:"DEBUG: "}
            if not konec:
                win32evtlogutil.ReportEvent(
                                            "AVSOB", # Application name
                                            win32evtlog.EVENTLOG_INFORMATION_TYPE, # Event ID
                                            0, # Event category
                                            win32evtlog.EVENTLOG_INFORMATION_TYPE,
                                            ("AVSOB", time.strftime("%H:%M:%S ")+levelSlovnik[level]+str(zprava)))
                                            
                print(time.strftime("%H:%M:%S ")+levelSlovnik[level]+str(zprava))
            else:
                input(time.strftime("%H:%M:%S ")+levelSlovnik[level]+str(zprava))