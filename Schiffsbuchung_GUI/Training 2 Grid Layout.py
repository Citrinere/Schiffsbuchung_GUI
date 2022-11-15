import sys
from PyQt5.QtWidgets import *   # alles importieren
from PyQt5.QtGui import *       # alles importieren
from PyQt5.QtCore import *      # alles importieren

class Fenster(QWidget):
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        grid = QGridLayout()
        namen = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        #namen = ['<', '>']
        posis = [(i, j) for i in range (5) for j in range (3)]      # hoehe (i) mal breite (j)
        for pos, name in zip(posis, namen):                         # zip = zusammenpacken
            button = QPushButton(name)
            grid.addWidget(button, *pos)                            # *pos = auspacken




        self.setLayout(grid)
        self.setGeometry(50, 50, 1000, 500)
        self.setWindowTitle("Layout-Training")
        self.setWindowIcon(QIcon("SchiffIcon.png"))
        self.show()

app = QApplication(sys.argv)
w = Fenster()                   # Fenster aufbauen != Fenster anzeigen
sys.exit(app.exec_())           # Python Programm stoppt wenn Fenster geschlossen wird