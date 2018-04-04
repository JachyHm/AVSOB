import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gio
from gi.repository import Gtk

MENU = """
<ui>
    <menubar name='hMenu'>
        <menu action='SuborMenu'>
            <menuitem action='SuborOtvorZlozku' />
            <separator />
            <menuitem action='Ukonci' />
        </menu>
        <menu action='Editory'>
            <menu action='EditorHlaseni'>
                <menuitem action='EditorHlaseniaDopravcia'/>
                <menuitem action='EditorHlaseniaHodiny'/>
                <menuitem action='EditorHlaseniaMeskanie'/>
                <menuitem action='EditorHlaseniaMeskanieTyp'/>
                <menuitem action='EditorHlaseniaMinuty'/>
                <menuitem action='EditorHlaseniaNastupiste'/>
                <menuitem action='EditorHlaseniaSlova'/>
                <menuitem action='EditorHlaseniaStanice'/>
                <menuitem action='EditorHlaseniaTyp'/>
                <menuitem action='EditorHlaseniaVety'/>
                <menuitem action='EditorHlaseniaZnelky'/>
            </menu>
            <menuitem action='EditorZastavek' />
            <menuitem action='EditorDatumov' />
            <menuitem action='EditorVychodzichTras' />
            <menuitem action='EditorSpojov' />
        </menu>
        <menu action='Funkcie'>
            <menuitem action='ChoiceOne'/>
            <menuitem action='ChoiceTwo'/>
            <separator />
            <menuitem action='ChoiceThree'/>
        </menu>
    </menubar>
    <popup name='PopupMenu'>
        <menuitem action='EditCopy' />
        <menuitem action='EditPaste' />
        <menuitem action='EditSomething' />
    </popup>
</ui>
"""

class Aplikacia(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id="JaHu.AVSOB.GEDAVSOB",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
    def do_activate(self):
        window = Gtk.ApplicationWindow(application=self)
        window.show()

    # def okno(self):
    #     Gtk.Window.__init__(self, title="Editor súborov aplikácie AVSOB")
    #     #vytvorí sa okno s titulkom "Editor súborov aplikácie AVSOB"
    #     self.set_size_request(650, 100)
    #     #definuej jeho velkost na 650*100px
    #     mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
    #     #definuje tabulku mainBox, která rozdělí obrazovku vertikálně na 2 části (HMENU a zbytek okna)
    #     hMenuBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
    #     #definuje tabulku hMenuBox, která rozdělí obrazovku horizontálně na 5 částí
    #     mainBox.pack_start(hMenuBox, True, True, 0)

    #     akce = Gtk.ActionGroup("oknoMain")

    # def VytvorMenuSubor (self, akce):
    #     action_filemenu = Gtk.Action("FileMenu", "File", None, None)
    #     akce.add_action(action_filemenu)

    #     action_filenewmenu = Gtk.Action("FileNew", None, None, Gtk.STOCK_NEW)
    #     akce.add_action(action_filenewmenu)

    #     action_new = Gtk.Action("FileNewStandard", "_New",
    #         "Create a new file", Gtk.STOCK_NEW)
    #     action_new.connect("activate", self.on_menu_file_new_generic)
    #     akce.add_action_with_accel(action_new, None)

    #     akce.add_actions([
    #         ("FileNewFoo", None, "New Foo", None, "Create new foo",
    #          self.on_menu_file_new_generic),
    #         ("FileNewGoo", None, "_New Goo", None, "Create new goo",
    #          self.on_menu_file_new_generic),
    #     ])

    #     action_filequit = Gtk.Action("FileQuit", None, None, Gtk.STOCK_QUIT)
    #     action_filequit.connect("activate", self.on_menu_file_quit)
    #     akce.add_action(action_filequit)

if __name__ == '__main__':
    app = Aplikacia()
    app.run(sys.argv)