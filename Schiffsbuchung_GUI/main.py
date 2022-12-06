# Python Project - Schiffsbuchung_GUI
# Fuer das Modul Programmieren Graphischer Oberflaechen WS 2022
# Projektmitglieder: Florian Czech, Alexander Teichmann, Alexander Schweizer

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, Qt

import sys
import pandas   #"pandas" und "openpyxl" installieren

#Dateipfade
IMGPATH = r'Bilder\Schiffstypen' #Schiffstypen Bilder
TABLEPATH = r'Schiffreisen.xlsx' #Excel Tabelle

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
Filter
"""
class Filter(QVBoxLayout):
    def __init__(self):
        #super(Filter, self).__init__()
        QVBoxLayout.__init__(self)
        self.filterLayout = QVBoxLayout()
        self.filterLayout.addWidget(QPushButton("PushButton"))
        self.filterLayout.addWidget(QCheckBox("Checkbox"))

        #self.setLayout(self.filterLayout)

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
        horHeaders = ["Reisenummer", "Meerart", "Übernachtungen", "Besuchte Städte", "Schiffstyp", "Preise Innenkabine", "Preise Außenkabine", "Preise Balkonkabine"]  #Headerliste. Vielleicht aus Excel lesen?

        for row_number, row_data in enumerate(self.data):   #Schleife, die alle Tabellenelemente durchgeht
            for column_number, column_data in enumerate(row_data):
                if column_number == 4:  #In Column 4 (Schiffstyp) Text durch Bilder ersetzen
                    imagePath = IMGPATH + "\Schiffstyp " + str(column_data) + ".jpg"
                    item = self.getImageLabel(imagePath)
                    self.setCellWidget(row_number, column_number, item)

                newItem = QTableWidgetItem(str(column_data))
                self.setItem(row_number, column_number, newItem)
                self.show()

        self.setHorizontalHeaderLabels(horHeaders)  #Header setzen

    def getImageLabel(self, image):
        imageLabel = ImageCruiseShip(image)
        return imageLabel

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 100, 1400, 700)
        self.setWindowTitle("Schiffsbuchung")
        self.setWindowIcon(QIcon("Schifficon.png"))

        outerLayout = QVBoxLayout()     #Layout Anker für alle andern Layouts

        """
        self.filter = Filter()
        filterLayout = QVBoxLayout()       #TopBar für Filter
        filterLayout.addLayout(self.filter)
        """

        filterLayout = QGridLayout()

        filterOceanLabel = QLabel()
        filterOceanLabel.setText("Meeresart")
        filterLayout.addWidget(filterOceanLabel, 0, 0)

        oceanCheckbox1 = QCheckBox("Mittelmeer")
        filterLayout.addWidget(oceanCheckbox1, 1, 0)

        oceanCheckbox2 = QCheckBox("Ostsee")
        oceanCheckbox2.setChecked(True)
        oceanCheckbox2.stateChanged.connect(lambda:self.filterState(oceanCheckbox3))
        filterLayout.addWidget(oceanCheckbox2, 2, 0)

        oceanCheckbox3 = QCheckBox("Nordsee")
        oceanCheckbox3.setChecked(True)
        oceanCheckbox3.stateChanged.connect(lambda:self.filterState(oceanCheckbox3))
        filterLayout.addWidget(oceanCheckbox3, 3, 0)

        self.table_view = TableView(getTable(), len(getTable()), 8)
        tableLayout = QVBoxLayout()     #Tabellen Layout
        tableLayout.addWidget(self.table_view)

        outerLayout.addLayout(filterLayout)    #UnterLayouts zum Main Layout hinzufügen
        outerLayout.addLayout(tableLayout)
        self.setLayout(outerLayout)


        for x in range(len(getTable())):  # Row-Höhe festlegen
            self.table_view.setRowHeight(x, 128)

        self.table_view.setColumnWidth(4, 256)  # Schiffstypen größer machen für Bilder
        # table.setColumnHidden(4, True)   #Schiffstypen ausblenden, später durch Button einblenden lassen
        """
        for x in range(25):  # Test um spezifische Reihen anhand von Keywords auszublenden
            #print("Ausgabe table.item(): " + str(self.table_view.item(x, 1)))  # Debug/Testprint
            checkItem = self.table_view.item(x, 1)
            #print("Ausgabe des Textes in table.item(): " + checkItem.text())  # Debug/Testprint
            if checkItem.text() == "Ostsee":
                self.table_view.hideRow(x)
        """

    def filterState(self, button):
        print("Check Filter State")
        print(button.text)
        if button.text() == "Ostsee":
            print("Ostsee")
            if button.isChecked() == True:
                for x in range(25):  # Test um spezifische Reihen anhand von Keywords auszublenden
                    # print("Ausgabe table.item(): " + str(self.table_view.item(x, 1)))  # Debug/Testprint
                    checkItem = self.table_view.item(x, 1)
                    # print("Ausgabe des Textes in table.item(): " + checkItem.text())  # Debug/Testprint
                    if checkItem.text() == "Ostsee":
                        self.table_view.showRow(x)
            else:
                for x in range(25):  # Test um spezifische Reihen anhand von Keywords auszublenden
                    # print("Ausgabe table.item(): " + str(self.table_view.item(x, 1)))  # Debug/Testprint
                    checkItem = self.table_view.item(x, 1)
                    # print("Ausgabe des Textes in table.item(): " + checkItem.text())  # Debug/Testprint
                    if checkItem.text() == "Ostsee":
                        self.table_view.hideRow(x)
"""
def main(args):
    app = QApplication(args)

    filter = QGridLayout()
    filter.addWidget(QPushButton("Button at (0, 0)"), 0, 0)
    filter.addWidget(QPushButton("Button at (0, 1)"), 0, 1)
    filter.addWidget(QPushButton("Button Spans two Cols"), 1, 0, 1, 2)



    table = TableView(getTable(), len(getTable()), 8)    #Tabellenfenster generieren
    table.setGeometry(300, 100, 1400, 700)  # (horizontale position, vertikale position, breite des Fensters, hoehe des Fensters)
    table.setWindowTitle("Schiffsbuchung")
    table.setWindowIcon(QIcon("Schifficon.png"))

    for x in range(len(getTable())):     #Row-Höhe festlegen
        table.setRowHeight(x, 128)

    table.setColumnWidth(4, 256)    #Schiffstypen größer machen für Bilder
    #table.setColumnHidden(4, True)   #Schiffstypen ausblenden, später durch Button einblenden lassen
    
    for x in range(25):     #Test um spezifische Reihen anhand von Keywords auszublenden
        print("Ausgabe table.item(): " + str(table.item(x,1)))      #Debug/Testprint
        checkItem = table.item(x, 1)
        print("Ausgabe des Textes in table.item(): " + checkItem.text())    #Debug/Testprint
        if checkItem.text() == "Ostsee":
            table.hideRow(x)
    
    table.show()
    sys.exit(app.exec_())

"""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())