import sys
from PyQt5.QtWidgets import *   # alles importieren
from PyQt5.QtGui import *       # alles importieren
from PyQt5.QtCore import *      # alles importieren




#------------------------------------Haupt Fenster---------------------------------------------------------------------#
class uberFenster(QTabWidget):
    def __init__(self):  # Konstruktor
        super().__init__()  # Erlaubt zugriff auf Methoden und Eigenschaften von Eltern- und Geschwister-Klassen
        self.initMe()  # Aufrufung einer Initialisierungsmethode fuer das Fenster

    def initMe(self):
        self.tab1 = Hauptmenu()
        self.tab2 = NachAuswahlTab()
        self.tab3 = AllAuswahlTab()

        self.addTab(self.tab1, "Hauptmenu.py")
        self.addTab(self.tab2, "Diashow Auswahl")
        self.addTab(self.tab3, "Gallerie Auswahl")

        self.setGeometry(300, 100, 1000, 700)  # (horizontale position, vertikale position, breite des Fensters, hoehe des Fensters)
        self.setWindowTitle("Schiffsbuchung")  # Fenstertitel setzen
        self.setWindowIcon(QIcon("Schifficon.png"))  # Pictogram/Favicon setzen
        self.show()  # Fenster anzeigen


#------------------------------------Haupt Menu---------------------------------------------------------------------#
class Hauptmenu(QWidget):
    def __init__(self):
        super().__init__()  #Erlaubt zugriff auf Methoden und Eigenschaften von Eltern- und Geschwister-Klassen
        self.initMe()       #Aufrufung einer Initialisierungsmethode fuer das Fenster
        self.TextInput()

    def initMe(self):
        box = QVBoxLayout(self)                         #Vertikales BoxLayout...
        self.setLayout(box)                             #...erzeugen

        scroll = QScrollArea(self)                      #Scrollbereich...
        box.addWidget(scroll)                           #...erstellen
        #scroll.setWidgetResizable(True)                #Erlaubt das Skalieren der ScrollArea (und des Contents)
        scrollContent = QWidget(scroll)                 #Inhalt im Scrollbereich
        scrollLayout = QVBoxLayout(scrollContent)       #Vertikales (V) Layout fuer ScrollContent in ScrollArea
        scrollContent.setLayout(scrollLayout)           #Layout Setzen
        for i in range(1, 51):                          #Anzahl der Items setzen
            scrollLayout.addWidget(QPushButton(str(i)))
        scroll.setWidget(scrollContent)

    #--Text Input Feld--#
    def TextInput(self):
        self.w = QLineEdit(self)                    #
        self.w.move(450, 50)                         #Position des Textfeldes
        self.w.setMinimumSize(50, 0)
        self.w.textChanged.connect(self.clicked)    #
        #self.w.setValidator(CharValidator())       #Nur Buchstaben Erlauben

    def clicked(self, text):        #Text kann auch an anderen stellen (z.B. in Events) abgefragt oder aufgerufen werden
        print(self.w.text())

    #def CharValidator(self, text):  #Eigenen Validator um nur Buchstaben bei der Suche zu zu lassen


#------------------------------------Auswahl Nacheinander Tab------------------------------------------------------#
class NachAuswahlTab(QWidget):  # Tab um Staedte nacheinander auszuwaehlen
    def __init__(Auswahl):  # Konstruktor
        super().__init__()  # Erlaubt zugriff auf Methoden und Eigenschaften von Eltern- und Geschwister-Klassen
        Auswahl.initMeAuswahl()   # Aufrufung einer Initialisierungsmethode fuer das Fenster

    def initMeAuswahl(Auswahl):
        h = QHBoxLayout()             # horizontales Box Layout
        weiter = QPushButton(">")
        weiter.setToolTip("Naechste Auswahl")
        zuruck = QPushButton("<")
        zuruck.setToolTip("Vorherige Auswahl")
        h.addWidget(zuruck)          # anordnung von "addwidget" und...
        h.addStretch(1)             # "addstretch" spielen eine wichtige rolle im Box Layout
        h.addWidget(weiter)

        Auswahl.setLayout(h)       # Layout Anwenden als main-layout fuer das ganze Fenster
        Auswahl.setGeometry(300, 100, 1000, 700)       # (horizontale position, vertikale position, breite des Fensters, hoehe des Fensters)
        Auswahl.setWindowTitle("Schiffsbuchung")       # Fenstertitel setzen
        Auswahl.setWindowIcon(QIcon("Schifficon.png")) # Pictogram/Favicon setzen
        Auswahl.show()    #Fenster anzeigen (!= Fenster aufbauen)


#------------------------------------Auswahl Auf Einmal Fenster------------------------------------------------------#
class AllAuswahlTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        grid = QGridLayout()
        namen = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        posis = [(i, j) for i in range(100) for j in range(3)]  # hoehe (i) mal breite (j)
        for pos, name in zip(posis, namen):  # zip = zusammenpacken
            button = QPushButton(name)
            grid.addWidget(button, *pos)  # *pos = auspacken

        self.setLayout(grid)
        self.setGeometry(50, 50, 1000, 500)
        self.setWindowTitle("Layout-Training")
        self.setWindowIcon(QIcon("SchiffIcon.png"))
        self.show()

app = QApplication(sys.argv)
w = uberFenster()  # Fenster aufbauen != Fenster anzeigen
sys.exit(app.exec_())  # Python Programm stoppt wenn Fenster geschlossen wird







#--------------------------------------Code Kurzspeicher(Pastebin)--------------------------------------#

#---ScrollArea---#
#         box = QVBoxLayout(self)
#         self.setLayout(box)
#
#         scroll = QScrollArea(self)                  #Scrollbereich erstellen
#         box.addWidget(scroll)                       #Scrollbereich zuweisen
#         scroll.setWidgetResizable(True)             #Erlaubt das Skalieren der ScrollArea
#         scrollContent = QWidget(scroll)             #Inhalt im Scrollbereich
#         scrollLayout = QVBoxLayout(scrollContent)   #Vertikales (V) Layout fuer ScrollContent in ScrollArea
#         scrollContent.setLayout(scrollLayout)
#         for i in range(0, 100):
#             scrollLayout.addWidget(QPushButton(str(i)))
