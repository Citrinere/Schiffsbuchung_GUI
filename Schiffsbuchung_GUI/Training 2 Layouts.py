import sys
from PyQt5.QtWidgets import *   # alles importieren
from PyQt5.QtGui import *       # alles importieren
from PyQt5.QtCore import *      # alles importieren

class Fenster(QWidget):
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        #upvote = QPushButton("Upvote Me")
        #abo = QPushButton("Sub Me")
        links = QPushButton("<")
        rechts = QPushButton(">")
        h = QHBoxLayout()
        #h.addWidget(upvote)
        h.addWidget(links)
        h.addStretch(1)
        #h.addWidget(abo)
        h.addWidget(rechts)




        self.setLayout(h)
        self.setGeometry(50, 50, 1000, 500)
        self.setWindowTitle("Layout-Training")
        self.setWindowIcon(QIcon("SchiffIcon.png"))
        self.show()

app = QApplication(sys.argv)
w = Fenster()                   # Fenster aufbauen != Fenster anzeigen
sys.exit(app.exec_())           # Python Programm stoppt wenn Fenster geschlossen wird