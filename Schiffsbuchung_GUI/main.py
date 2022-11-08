# Python Project - Schiffsbuchung_GUI
# Fuer das Modul Programmieren Graphischer Oberflaechen WS 2022
# Projektmitglieder: Florian Czech, Alexander Teichmann, Alexander Schweizer

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

app = QApplication(sys.argv)

w = QWidget()   #Fenster aufbauen != Fenster anzeigen
w.setGeometry(300,100,1000,700)  #(horizontale position, vertikale position, breite des Fensters, hoehe des Fensters)
w.setWindowTitle("Schiffsbuchung")  #Fenstertitel setzen
w.setWindowIcon(QIcon("Schifficon.png"))  #Pictogram/Favicon setzen

w.show()    #Fenster anzeigen

sys.exit(app.exec_())   #Python Programm stoppt wenn Fenster geschlossen wird


