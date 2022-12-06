import sys
from PyQt5.QtWidgets import *   # alles importieren
from PyQt5.QtGui import *       # alles importieren
from PyQt5.QtCore import *      # alles importieren


class Fenster(QWidget):
    def __init__(self):  # Konstruktor
        super().__init__()
        self.initMe()  # Aufrufung einer Initialisierungsmethode fuer das Fenster

    def initMe(self):
        self.setGeometry(300, 100, 1000, 700)  # (horizontale position, vertikale position, breite des Fensters, hoehe des Fensters)
        self.setWindowTitle("Schiffsbuchung")  # Fenstertitel setzen
        self.setWindowIcon(QIcon("Schifficon.png"))  # Pictogram/Favicon setzen
        self.show()  # Fenster anzeigen


app = QApplication(sys.argv)
w = Fenster()  # Fenster aufbauen != Fenster anzeigen
sys.exit(app.exec_())  # Python Programm stoppt wenn Fenster geschlossen wird

