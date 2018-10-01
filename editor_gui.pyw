import sys
import Pyro4
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

class MainWindow():
    def __init__(self):
        self.prihlasenyServis = False
        self.Window()

    def CloseApplication(self):
        sys.exit(0)

    def OpenFolder(self):
        print("Otvor zlozku!")

    def HlaseniaDopravcia(self):
        print("Editor hlasenia dopravci!")

    def HlaseniaHodiny(self):
        print("Editor hlasenia hodiny!")

    def HlaseniaMeskanie(self):
        print("Editor hlasenia meskanie!")

    def HlaseniaMeskanieTyp(self):
        print("Editor hlasenia meskanie typ!")

    def HlaseniaMinuty(self):
        print("Editor hlasenia minuty!")

    def HlaseniaNastupiste(self):
        print("Editor hlasenia nastupiste!")

    def HlaseniaSlova(self):
        print("Editor hlasenia slova!")

    def HlaseniaStanice(self):
        print("Editor hlasenia stanice!")

    def HlaseniaTyp(self):
        print("Editor hlasenia typ!")

    def HlaseniaVety(self):
        print("Editor hlasenia vety!")

    def HlaseniaZnelky(self):
        print("Editor hlasenia znelky!")

    def ServisTriggered(self):
        self.mainMenuServisChBoxValue.set(False)
        if not self.prihlasenyServis:
            self.loginDialog = Toplevel(self.mainWindow)
            self.loginDialog.resizable(FALSE,FALSE)
            self.loginDialog.title("Zadajte heslo správca!")

            loginDialogFrame = ttk.Frame(self.loginDialog, padding="3 3 12 12")
            loginDialogFrame.grid(column=0, row=0, sticky=(N, W, E, S))
            loginDialogFrame.columnconfigure(0, weight=1)
            loginDialogFrame.rowconfigure(0, weight=1)

            labelZadejteHeslo = ttk.Label(loginDialogFrame, text="Zadajte heslo správca:")
            labelZadejteHeslo.grid(column=1, row=1, sticky=(W,E))

            self.hesloEntry = ttk.Entry(loginDialogFrame, show="*")
            self.hesloEntry.grid(column=1, columnspan=2, row=2, sticky=(W,E))

            confirmButton = ttk.Button(loginDialogFrame, text="Potvrď", command=self.CheckPassword)
            confirmButton.grid(column=1, row=3, sticky=(W,E))

            self.loginDialog.bind("<Return>", self.CheckPassword)
            self.hesloEntry.focus()
        else:
            self.prihlasenyServis = False
            self.LoadMenu(self.prihlasenyServis)
            messagebox.showinfo(title="Odhlásenie", message="Správca bol odhlásený!")

    def CheckPassword(self, * args):
        if self.hesloEntry.get() == "1937":
            self.prihlasenyServis = True
            self.loginDialog.destroy()
            self.LoadMenu(self.prihlasenyServis)
            messagebox.showinfo(title="Prihlásenie", message="Jste prihlásený ako správca!")
        else:
            self.prihlasenyServis = False
            self.hesloEntry.delete(0,"end")

    def SetServerIP(self):
        print("Set server IP")

    def LoadMenu(self, servis=False):
        if not servis:
            # Definicia hlavneho ovladacieho menu
            self.mainMenu = Menu(self.mainWindow)

            self.mainMenuSubor = Menu(self.mainMenu)
            self.mainMenuEditory = Menu(self.mainMenu)
            self.mainMenuFunkcie = Menu(self.mainMenu)
            self.mainMenuServis = Menu(self.mainMenu)

            self.mainMenuSubor.add_command(label="Otvor zložku", command=self.OpenFolder)
            self.mainMenuSubor.add_command(label="Ukonči aplikáciu", command=self.CloseApplication)

            self.mainMenuEditorHlasenia = Menu(self.mainMenuEditory)
            self.mainMenuEditory.add_cascade(menu=self.mainMenuEditorHlasenia, label="Editor hlásenia")
            self.mainMenuEditorHlasenia.add_command(label="Dopravcia", command=self.HlaseniaDopravcia)
            self.mainMenuEditorHlasenia.add_command(label="Hodiny", command=self.HlaseniaHodiny)
            self.mainMenuEditorHlasenia.add_command(label="Meškanie", command=self.HlaseniaMeskanie)
            self.mainMenuEditorHlasenia.add_command(label="Typy meškanie", command=self.HlaseniaMeskanieTyp)
            self.mainMenuEditorHlasenia.add_command(label="Minuty", command=self.HlaseniaMinuty)
            self.mainMenuEditorHlasenia.add_command(label="Nástupiště", command=self.HlaseniaNastupiste)
            self.mainMenuEditorHlasenia.add_command(label="Slova", command=self.HlaseniaSlova)
            self.mainMenuEditorHlasenia.add_command(label="Stanice", command=self.HlaseniaStanice)
            self.mainMenuEditorHlasenia.add_command(label="Typy", command=self.HlaseniaTyp)
            self.mainMenuEditorHlasenia.add_command(label="Vety", command=self.HlaseniaVety)
            self.mainMenuEditorHlasenia.add_command(label="Znelky", command=self.HlaseniaZnelky)

            self.mainMenuServisChBoxValue = BooleanVar()
            self.mainMenuServis.add_checkbutton(label="Prihlásiť", command=self.ServisTriggered, variable=self.mainMenuServisChBoxValue)

            self.mainMenu.add_cascade(menu=self.mainMenuSubor, label="Subor")
            self.mainMenu.add_cascade(menu=self.mainMenuEditory, label="Editory")
            self.mainMenu.add_cascade(menu=self.mainMenuFunkcie, label="Funkcie")
            self.mainMenu.add_cascade(menu=self.mainMenuServis, label="Servis")

            self.mainWindow["menu"] = self.mainMenu
        else:
            # Definicia hlavneho ovladacieho menu
            self.mainMenu = Menu(self.mainWindow)

            self.mainMenuSubor = Menu(self.mainMenu)
            self.mainMenuEditory = Menu(self.mainMenu)
            self.mainMenuFunkcie = Menu(self.mainMenu)
            self.mainMenuServis = Menu(self.mainMenu)

            self.mainMenuSubor.add_command(label="Otvor zložku", command=self.OpenFolder)
            self.mainMenuSubor.add_command(label="Ukonči aplikáciu", command=self.CloseApplication)

            self.mainMenuEditorHlasenia = Menu(self.mainMenuEditory)
            self.mainMenuEditory.add_cascade(menu=self.mainMenuEditorHlasenia, label="Editor hlásenia")
            self.mainMenuEditorHlasenia.add_command(label="Dopravcia", command=self.HlaseniaDopravcia)
            self.mainMenuEditorHlasenia.add_command(label="Hodiny", command=self.HlaseniaHodiny)
            self.mainMenuEditorHlasenia.add_command(label="Meškanie", command=self.HlaseniaMeskanie)
            self.mainMenuEditorHlasenia.add_command(label="Typy meškanie", command=self.HlaseniaMeskanieTyp)
            self.mainMenuEditorHlasenia.add_command(label="Minuty", command=self.HlaseniaMinuty)
            self.mainMenuEditorHlasenia.add_command(label="Nástupiště", command=self.HlaseniaNastupiste)
            self.mainMenuEditorHlasenia.add_command(label="Slova", command=self.HlaseniaSlova)
            self.mainMenuEditorHlasenia.add_command(label="Stanice", command=self.HlaseniaStanice)
            self.mainMenuEditorHlasenia.add_command(label="Typy", command=self.HlaseniaTyp)
            self.mainMenuEditorHlasenia.add_command(label="Vety", command=self.HlaseniaVety)
            self.mainMenuEditorHlasenia.add_command(label="Znelky", command=self.HlaseniaZnelky)

            self.mainMenuServisNastavenie = Menu(self.mainMenuServis)
            self.mainMenuServisNastavenie.add_command(label="Nastavenie IP adresy serveru", command=self.SetServerIP)

            self.mainMenuServisChBoxValue = BooleanVar()
            self.mainMenuServis.add_checkbutton(label="Odhlásiť", command=self.ServisTriggered, variable=self.mainMenuServisChBoxValue)
            self.mainMenuServis.add_cascade(menu=self.mainMenuServisNastavenie, label="Nastavenie")

            self.mainMenu.add_cascade(menu=self.mainMenuSubor, label="Subor")
            self.mainMenu.add_cascade(menu=self.mainMenuEditory, label="Editory")
            self.mainMenu.add_cascade(menu=self.mainMenuFunkcie, label="Funkcie")
            self.mainMenu.add_cascade(menu=self.mainMenuServis, label="Servis")

            self.mainWindow["menu"] = self.mainMenu

    def Window(self):
        # Definicia okna
        self.mainWindow = Tk()
        self.mainWindow.option_add('*tearOff', FALSE)
        self.mainWindow.title("AVSOB dispečerské rozhranie")
        self.mainWindow.minsize(1280,700)

        self.LoadMenu(self.prihlasenyServis)

        self.mainWindow.mainloop()
if __name__ == '__main__':
    m = MainWindow()