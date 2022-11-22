# Python Project - Schiffsbuchung_GUI
# Fuer das Modul Programmieren Graphischer Oberflaechen WS 2022
# Projektmitglieder: Florian Czech, Alexander Teichmann, Alexander Schweizer

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, Qt

import sys
import pandas   #"pandas" und "openpyxl" installieren

#Dateipfade
IMGPATH = r'Aufgabe 2 Reiseportal\Schiffstypen' #Schiffstypen Bilder C:\Users\Alex Laptop\Desktop\GUI - Schiffsreisen\
TABLEPATH = r"Aufgabe 2 Reiseportal\Schiffreisen.xlsx" #Excel Tabelle C:\Users\Alex Laptop\Desktop\GUI - Schiffsreisen\

#Funktion um Exceltabelle in Liste umzuwandeln
def getTable():
    df = pandas.read_excel(TABLEPATH, header=3, usecols=lambda x: 'Unnamed' not in x)
    dfList = df.values.tolist()
    #print(dfList)
    return dfList

"""
Klasse zum Anzeigen von Schiffstyp Bildern mit pixmap
https://www.geeksforgeeks.org/pyqt5-how-to-add-image-in-window/
https://doc.qt.io/qt-6/qwidget.html
https://doc.qt.io/qtforpython-5/PySide2/QtGui/QPixmap.html

Aufbau: QWidget -> QLabel -> QPixmap
"""
class ImageCruiseShip(QWidget):

    def __init__(self, image):
        super(ImageCruiseShip, self).__init__()

        self.label = QLabel(self)
        self.pixmap = QPixmap(image)
        self.pixmap = self.pixmap.scaledToHeight(128) #Bild auf 128px Höhe anpassen

        self.label.setPixmap(self.pixmap)

"""
QTableWidget für die Tabelle
https://pythonbasics.org/pyqt-table/
https://doc.qt.io/qt-6/qtablewidget.html
"""
class TableView(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()


    def setData(self):  #
        horHeaders = ["Reisenummer","Meerart","Übernachtungen","Besuchte Städte", "Schiffstyp", "Preise Innenkabine", "Preise Außenkabine", "Preise Balkonkabine"]  #Headerliste. Vielleicht aus Excel lesen?

        for row_number, row_data in enumerate(self.data):   #Schleife, die alle Tabellenelemente durchgeht
            for column_number, column_data in enumerate(row_data):
                if column_number == 4:  #In Column 4 (Schiffstyp) Text durch Bilder ersetzen
                    imagePath = IMGPATH + "\Schiffstyp " + str(column_data) + ".jpg"
                    item = self.getImageLabel(imagePath)
                    self.setCellWidget(row_number, column_number, item)

                newitem = QTableWidgetItem(str(column_data))
                self.setItem(row_number, column_number, newitem)

        self.setHorizontalHeaderLabels(horHeaders)  #Header setzen

    def getImageLabel(self, image):
        imageLabel = ImageCruiseShip(image)
        return imageLabel

def main(args):
    app = QApplication(args)

    table = TableView(getTable(),len(getTable()),8)    #Tabellenfenster generieren
    table.setGeometry(300, 100, 1400, 700)  # (horizontale position, vertikale position, breite des Fensters, hoehe des Fensters)
    table.setWindowTitle("Schiffsbuchung")
    table.setWindowIcon(QIcon("Schifficon.png"))

    for x in range(len(getTable())):     #Row-Höhe festlegen
        table.setRowHeight(x, 128)

    table.setColumnWidth(4, 256)    #Schiffstypen größer machen für Bilder
    table.setColumnHidden(4,True)   #Schiffstypen ausblenden, später durch Button einblenden lassen

    for x in range(25):     #Test um spezifische Reihen anhand von Keywords auszublenden
        print("Ausgabe table.item(): " + str(table.item(x,1)))      #Debug/Testprint
        checkItem = table.item(x,1)
        print("Ausgabe des Textes in table.item(): " + checkItem.text())    #Debug/Testprint
        #if checkItem.text() == "Ostsee":
         #   table.hideRow(x)

    table.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv)