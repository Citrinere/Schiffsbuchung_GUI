# Python Project - Schiffsbuchung_GUI
# Fuer das Modul Programmieren Graphischer Oberflaechen WS 2022
# Projektmitglieder: Florian Czech, Alexander Teichmann, Alexander Schweizer

import sys
#import os
from PyQt5.QtWidgets import *   # alles importen von QtWidgets
from PyQt5.QtGui import *       # alles importen von QtGui
from PyQt5.QtCore import *       # alles importen von QtCore
#os.system("pyuic6 -o Testerinozeros.py ..\QT-Windows\Nacheinander_Fenster.ui") # ui datei in py datei umwandeln (geht aber nicht)

class Fenster(QWidget): #
    def __init__(self):  # Konstruktor
        super().__init__()
        self.initMe()   # Aufrufung einer Initialisierungsmethode fuer das Fenster

#------------------------------------Nacheinander Fenster--------------------------------------------------------------#
    def initMe(self):
        h = QHBoxLayout()             # horizontales Box Layout
        weiter = QPushButton(">")
        weiter.setToolTip("Naechste Auswahl")
        zuruck = QPushButton("<")
        zuruck.setToolTip("Vorherige Auswahl")
        h.addWidget(zuruck)          # anordnung von "addwidget" und...
        h.addStretch(1)             # "addstretch" spielen eine wichtige rolle im Layout
        h.addWidget(weiter)

        self.setLayout(h)       # Layout Anwenden als main-layout fuer das ganze Fenster
        self.setGeometry(300, 100, 1000, 700)       # (horizontale position, vertikale position, breite des Fensters, hoehe des Fensters)
        self.setWindowTitle("Schiffsbuchung")       # Fenstertitel setzen
        self.setWindowIcon(QIcon("Schifficon.png")) # Pictogram/Favicon setzen
        self.show()    #Fenster anzeigen (!= Fenster aufbauen)
#------------------------------------Nacheinander Fenster--------------------------------------------------------------#

app = QApplication(sys.argv)
w = Fenster()           #Fenster aufbauen (!= Fenster anzeigen)
sys.exit(app.exec_())   #Python Programm stoppt wenn Fenster geschlossen wird

#w = QWidget()   #Fenster aufbauen != Fenster anzeigen
#w.setGeometry(300,100,1000,700)  #(horizontale position, vertikale position, breite des Fensters, hoehe des Fensters)
#w.setWindowTitle("Schiffsbuchung")  #Fenstertitel setzen
#w.setWindowIcon(QIcon("Schifficon.png"))  #Pictogram/Favicon setzen
#w.show()    #Fenster anzeigen


