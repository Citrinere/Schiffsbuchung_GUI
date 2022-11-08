# Python Project - Schiffsbuchung_GUI
# Fuer das Modul Programmieren Graphischer Oberflaechen WS 2022
# Projektmitglieder: Florian Czech, Alexander Teichmann, Alexander Schweizer

import sys
from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)

w = QWidget()   #Fenster aufbauen != Fenster anzeigen

w.show()    #Fenster anzeigen

sys.exit(app.exec_())   #Python Programm stoppt wenn Fenster geschlossen wird


