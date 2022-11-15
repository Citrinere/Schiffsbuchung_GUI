import sys
from PyQt5 import QtCore
#from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip
#from PyQt5.QtGui import QIcon, QFont
#from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import *   # alles importieren
from PyQt5.QtGui import *       # alles importieren
from PyQt5.QtCore import *      # alles importieren


class EigenerEvent(QObject):
    SchliessmichEvent = pyqtSignal()

class MyButton(QPushButton):    # Button ersetzen
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:    # hat nur auf widget, nicht auf Fenster auswirkung
            self.close()

class Fenster(QWidget):
    def __init__(self):  # Konstruktor
        super().__init__()
        self.initMe()  # Aufrufung einer Initialisierungsmethode fuer das Fenster

    def initMe(self):
        self.sig = EigenerEvent()
        self.sig.SchliessmichEvent.connect(self.close)  # wann das Event aktiv werden soll
        QToolTip.setFont(QFont('Times New Roman', 14))
        button = QPushButton('Drueck mich', self)
        button.move(50, 50)
        button.setToolTip('This is my <b>Button<b>')
        #button.clicked.connect(QtCore.QCoreApplication.instance().quit) # Vorgegebebe funktion aufrufen, hier: fenster schliessen
        button.clicked.connect(self.gedrueckt)  # Eigene Funktion aufrufen
        # "button.clicked.connect" = " auf welchem objekt . welche funktion . (connect immer vorhanden) "
        #self.setToolTip('Hollllllaaaaa')
        self.setGeometry(300, 100, 1000, 700)  # (horizontale position, vertikale position, breite des Fensters, hoehe des Fensters)
        self.setWindowTitle("Schiffsbuchung")  # Fenstertitel setzen
        self.setWindowIcon(QIcon("Schifficon.png"))  # Pictogram/Favicon setzen
        self.show()  # Fenster anzeigen

    def gedrueckt(self):
        sender = self.sender()
        sender.move(100, 100)
        print(sender.text() + ' Button gedrueckt')

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            #self.close()
            self.sig.SchliessmichEvent.emit()


app = QApplication(sys.argv)
w = Fenster()  # Fenster aufbauen != Fenster anzeigen
sys.exit(app.exec_())  # Python Programm stoppt wenn Fenster geschlossen wird

