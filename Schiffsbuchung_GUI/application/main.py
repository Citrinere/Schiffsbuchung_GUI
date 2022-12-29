import random

from PyQt5 import QtCore
#from PyQt5.QtWidgets import QApplication, QComboBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox, QLabel
from PyQt5.QtWidgets import *
#from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QSpinBox
from PyQt5.QtGui import QStandardItemModel, QIcon
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from os.path import exists as file_exists
import sys
import pandas


IMGPATH = r'data\images\Schiffstypen' #Schiffstypen Bilder
TABLEPATH = r'data\Schiffreisen.xlsx' #Excel Tabelle

#Funktion um Exceltabelle in Liste umzuwandeln
def getTable():
    df = pandas.read_excel(TABLEPATH, header=3, usecols=lambda x: 'Unnamed' not in x, skiprows=range(25,29))
    dfList = df.values.tolist()

    return dfList


#Funktion zur Abfrage der Städte an einer bestimmten Meeresart
def getCityList(regiontype="all"): # Bsp.: getCityList("Nordsee")

    FullList = getTable()
    cityList = []

    for row_number, row_data in enumerate(FullList):  # Schleife, die alle Tabellenelemente durchgeht
        for column_number, column_data in enumerate(row_data):
            if column_number == 3:
                if row_data[1] == regiontype or regiontype == "all":
                    cityBuff = column_data.split()
                    for city_num, city_data in enumerate(cityBuff):
                        cityBuff[city_num] = city_data.replace(",","")
                        if cityBuff[city_num] not in cityList:
                            cityList.append(cityBuff[city_num])
    cityList.sort()
    return cityList

class PersonalDataDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Persönliche Daten")
        self.setWindowIcon(QIcon("data\images\SchiffIcon.png"))
        #self.setGeometry(150, 150, 300, 600)
        self.setFixedWidth(300)
        self.setFixedHeight(440)

        self.PersonalDataLayout = QGridLayout()
        self.PersonalDataLayout.addWidget(self.createDialog("Name",["Nachname", "Vorname"]), 0, 0)
        self.PersonalDataLayout.addWidget(self.createDialog("Adresse", ["Postleitzahl", "Ort", "Straße, Hausnummer"]), 1, 0)
        self.PersonalDataLayout.addWidget(self.createDialog("Bankdaten", ["IBAN"]), 2, 0)

        self.saveButton = QPushButton("Abspeichern", self)
        self.PersonalDataLayout.addWidget(self.saveButton)
        self.saveButton.clicked.connect(self.saveData)

        self.setLayout(self.PersonalDataLayout)

        """
        self.VLabelLayout = QVBoxLayout()

        self.labelSurname = QLabel("Familienname:")
        self.VLabelLayout.addWidget(self.labelSurname)
        self.labelFirstName = QLabel("Vorname:")
        self.VLabelLayout.addWidget(self.labelFirstName)

        self.labelZipCode = QLabel("Postleitzahl:")
        self.VLabelLayout.addWidget(self.labelZipCode)
        self.labelCity = QLabel("Ort:")
        self.VLabelLayout.addWidget(self.labelCity)
        self.labelStreet = QLabel("Straße:")
        self.VLabelLayout.addWidget(self.labelStreet)
        self.labelHouseNumber = QLabel("Hausnummer:")
        self.VLabelLayout.addWidget(self.labelHouseNumber)

        self.labelIBAN = QLabel("IBAN:")
        self.VLabelLayout.addWidget(self.labelIBAN)

        PersonalDataLayout.addLayout(self.VLabelLayout, 0, 0)

        self.setLayout(PersonalDataLayout)
        """
    def createDialog(self, groupType, groupElements):
        groupBox = QGroupBox(groupType)
        groupBox.setStyleSheet('QGroupBox {'
                               '    font-size: 11pt;'
                               '    padding: 10 10px;}')
        vLayout = QVBoxLayout()

        for element_num, element in enumerate(groupElements):
            self.labelElement = QLabel(element)
            self.editElement = QLineEdit(self)
            self.editElement.resize(280,20)

            vLayout.addWidget(self.labelElement)
            vLayout.addWidget(self.editElement)
        #vLayout.addStretch(1)
        groupBox.setLayout(vLayout)

        return groupBox

    def saveData(self):
        print("...")
        textboxValue = []
        for i in range(0,3):
            groupWidget = self.PersonalDataLayout.itemAtPosition(i, 0)
            print(str(groupWidget.widget()))
            for textWidget in groupWidget.widget().children():
                if isinstance(textWidget, QLineEdit):
                    print("     " + textWidget.text())
                    textboxValue.append(textWidget.text())

        print("_______________________________")
        print(textboxValue)

    def displayDialog(self):
        self.show()

class OrderWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.personalDataDialog = PersonalDataDialog()
        self.cruiseData = []
        self.setWindowTitle('Bestellung')
        self.setWindowIcon(QIcon("data\images\SchiffIcon.png"))
        self.setGeometry(150, 150, 560, 760)
        self.setFixedWidth(760)
        self.setFixedHeight(560)
        self.setStyleSheet("""
            QLabel{
                font-size: 14px
            }
            QRadioButton{
                font-size: 14px
            }
            QPushButton{
                font-size: 17px
            }
            """)

        # Create Base Layout
        BestellGridLayout = QGridLayout()

        # Create Child Layouts and Widgets
            # Layout fuer Schiffstyp(Vorschau), Region, Uebernachtungen, Buchungsnummer
        self.VerticalLayoutLO = QVBoxLayout()
        self.SchiffstypLayout = QVBoxLayout()
        self.SchiffsTypVorschau = QGraphicsView()
        self.SchiffsTyp = QLabel("Schiffstyp: ")
        self.SchiffsTyp.setAlignment(QtCore.Qt.AlignCenter)
        self.SchiffstypLayout.addWidget(self.SchiffsTypVorschau)
        self.SchiffstypLayout.addWidget(self.SchiffsTyp)
        self.VerticalLayoutLO.addLayout(self.SchiffstypLayout)
        self.VerticalLayoutLO.addStretch()
        self.LaRegion = QLabel("Region: ")
        self.VerticalLayoutLO.addWidget(self.LaRegion)
        self.LaUebernachtungen = QLabel("Uebernachtungen: ")
        self.VerticalLayoutLO.addWidget(self.LaUebernachtungen)
        self.LaBuchungsnummer = QLabel()
        self.VerticalLayoutLO.addWidget(self.LaBuchungsnummer)
        self.VerticalLayoutLO.addStretch()
        BestellGridLayout.addLayout(self.VerticalLayoutLO, 0, 0)       # (self.layout, reihe, spalte)

            # Layout fuer Kabinen-Preise und Vorschau
        self.hKabinenLayout = QHBoxLayout()
        BestellGridLayout.addLayout(self.hKabinenLayout, 0, 1)
        self.vKabinenPreisLayout = QVBoxLayout()
        self.InnenPreis = QRadioButton("Innenkabine\nPreis: ")
        self.vKabinenPreisLayout.addWidget(self.InnenPreis)
        self.AussenPreis = QRadioButton("Aussenkabine\nPreis: ")
        self.vKabinenPreisLayout.addWidget(self.AussenPreis)
        self.BalkonPreis = QRadioButton("Balkonkabine\nPreis: ")
        self.vKabinenPreisLayout.addWidget(self.BalkonPreis)
        self.hKabinenLayout.addLayout(self.vKabinenPreisLayout)
        self.vKabinenVorschauLayout = QVBoxLayout()
        self.InnenVorschau = QGraphicsView()
        self.vKabinenVorschauLayout.addWidget(self.InnenVorschau)
        self.AussenVorschau = QGraphicsView()
        self.vKabinenVorschauLayout.addWidget(self.AussenVorschau)
        self.BalkonVorschau = QGraphicsView()
        self.vKabinenVorschauLayout.addWidget(self.BalkonVorschau)
        self.hKabinenLayout.addLayout(self.vKabinenVorschauLayout)

        self.input1 = QLabel()
        BestellGridLayout.addWidget(self.input1, 1, 0)      # (self.widget, reihe, spalte)
        # self.LaStadt = QLabel()
        # BestellGridLayout.addWidget(self.LaStadt, 1, 0)     # (self.widget, reihe, spalte)

        self.vBestaetigungsLayout = QVBoxLayout()
        self.LaGesamtpreis = QLabel("Summe: ...€")
        self.LaGesamtpreis.setAlignment(QtCore.Qt.AlignCenter)
        self.vBestaetigungsLayout.addWidget(self.LaGesamtpreis)
        self.ConfirmButton = QPushButton('Buchen')
        self.ConfirmButton.clicked.connect(self.confirmOrder)
        self.vBestaetigungsLayout.addWidget(self.ConfirmButton)
        #BestellGridLayout.addWidget(self.ConfirmButton, 1, 1)
        BestellGridLayout.addLayout(self.vBestaetigungsLayout, 1, 1)

        self.setLayout(BestellGridLayout)

    def confirmOrder(self):
        self.personalDataDialog.displayDialog()
        self.close()

    def displayWindow(self):

        self.LaRegion.setText("Region: " + self.cruiseData[0])
        self.LaUebernachtungen.setText("Uebernachtungen: " + self.cruiseData[1])
        #self.orderWindow.LaStadt.setText("Staedte: " + data[2])
        self.LaBuchungsnummer.setText("Buchungsnummer: " + str(random.randrange(2, 999999, 2)))
        self.InnenPreis.setText("Innenkabine\nPreis: " + self.cruiseData[4])
        self.AussenPreis.setText("Aussenkabine\nPreis: " + self.cruiseData[5])
        self.BalkonPreis.setText("Balkonkabine \nPreis: " + self.cruiseData[6])

        self.show()


# class OrderWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('Bestellung')
#         self.setFixedWidth(1000)
#         self.setStyleSheet("""
#             QLineEdit{
#                 font-size: 14px
#             }
#             QPushButton{
#                 font-size: 30px
#             }
#             """)
#         mainLayout = QVBoxLayout()
#
#         self.input1 = QLineEdit()
#         mainLayout.addWidget(self.input1)
#
#
#         self.closeButton = QPushButton('Close')
#         self.closeButton.clicked.connect(self.close)
#         mainLayout.addWidget(self.closeButton)
#
#         self.setLayout(mainLayout)
#
#     def displayInfo(self):
#         self.show()
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

# creating checkable combo box class
# class CheckableComboBox(QComboBox):
#     def __init__(self):
#         super(CheckableComboBox, self).__init__()
#         self.view().pressed.connect(self.handle_item_pressed)
#         self.setModel(QStandardItemModel(self))
#
#     # when any item get pressed
#     def handle_item_pressed(self, index):
#
#         # getting which item is pressed
#         item = self.model().itemFromIndex(index)
#
#         # make it check if unchecked and vice-versa
#         if item.checkState() == Qt.Checked:
#             item.setCheckState(Qt.Unchecked)
#         else:
#             item.setCheckState(Qt.Checked)
#
#         # calling method
#         self.check_items()
#
#     # method called by check_items
#     def item_checked(self, index):
#
#         # getting item at index
#         item = self.model().item(index, 0)
#
#         # return true if checked else false
#         return item.checkState() == Qt.Checked
#
#     # calling method
#     def check_items(self):
#         # blank list
#         checkedItems = []
#
#         # traversing the items
#         for i in range(self.count()):
#
#             # if item is checked add it to the list
#             if self.item_checked(i):
#                 checkedItems.append(i)
#
#         # call this method
#         self.update_labels(checkedItems)
#
#     # method to update the label
#     def update_labels(self, item_list):
#
#         n = ''
#         count = 0
#
#         # traversing the list
#         for i in item_list:
#
#             # if count value is 0 don't add comma
#             if count == 0:
#                 n += ' % s' % i
#             # else value is greater then 0
#             # add comma
#             else:
#                 n += ', % s' % i
#
#             # increment count
#             count += 1
#
#         # loop
#         for i in range(self.count()):
#
#             # getting label
#             text_label = self.model().item(i, 0).text()
#
#             # default state
#             if text_label.find('-') >= 0:
#                 text_label = text_label.split('-')[0]
#
#             # shows the selected items
#             item_new_text_label = text_label + ' - selected index: ' + n
#
#             # setting text to StadtComboBox
#             #self.setItemText(i, item_new_text_label)
#
#     # flush
#     sys.stdout.flush()

class CheckableComboBox(QComboBox):     # creating checkable combo box class which will stay open after a selection
    def __init__(self, parent=None):
        super(CheckableComboBox, self).__init__(parent)
        self.view().pressed.connect(self.handleItemPressed)
        self._changed = False

    def handleItemPressed(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)
        else:
            item.setCheckState(QtCore.Qt.Checked)
        self._changed = True

    def hidePopup(self):
        if not self._changed:
            super(CheckableComboBox, self).hidePopup()
        self._changed = False   # verhindert, dass wenn die combobox geoeffnett ist, man nichts anderes anklicken kann

    def itemChecked(self, index):
        item = self.model().item(index, self.modelColumn())
        return item.checkState() == QtCore.Qt.Checked

    def setItemChecked(self, index, checked=True):
        item = self.model().item(index, self.modelColumn())
        if checked:
            item.setCheckState(QtCore.Qt.Checked)
        else:
            item.setCheckState(QtCore.Qt.Unchecked)

#Tabelle
class TableView(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setData()

        self.setStyleSheet("font-size: 12pt; background-color: rgba(255, 255, 255, 0.6); selection-background-color: rgba(156,222,255, 0.8); selection-color: black;")
        self.setSelectionBehavior(QAbstractItemView.SelectRows)     # Whole Row will be marked on click
        self.setSelectionMode(QAbstractItemView.SingleSelection)    # Only one Row can be selected at any time
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)      # Data cant be edited
        self.resizeColumnsToContents()
        self.resizeRowsToContents()




    def setData(self):
        horHeaders = ["Reisenummer", "Meeresart", "Anzahl\nÜbernachtungen", "Besuchte Städte", "Schiffstyp", "Preis\nInnenkabine", "Preis\nAußenkabine", "Preis\nBalkonkabine"]  #Headerliste. Vielleicht aus Excel lesen?

        for row_number, row_data in enumerate(self.data):   #Schleife, die alle Tabellenelemente durchgeht
            for column_number, column_data in enumerate(row_data):
                if column_number == 3:
                    count = 0
                    for char_count, char in enumerate(column_data):
                        if char == ",":
                            count += 1
                        if count >= 4:
                            column_data = column_data[:char_count+2] + '\n' + column_data[char_count+2:]
                            count = 0

                if column_number == 4:  # In Column 4 (Schiffstyp) Text durch Bilder ersetzen
                    imagePath = IMGPATH + "\Schiffstyp " + str(column_data) + ".jpg"
                    item = self.getImageLabel(imagePath)
                    self.setCellWidget(row_number, column_number, item)

                if 5 <= column_number <= 7: # Preis Formatting
                    if column_data != "nicht vorhanden":
                        newItem = QTableWidgetItem(str(column_data) + " €")
                    else:
                        newItem = QTableWidgetItem(str(column_data))
                else:
                    newItem = QTableWidgetItem(str(column_data))
                newItem.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_number, column_number, newItem)
                self.show()


        """
        for row_number, row_data in enumerate(self.data):
            self.selectionButton = QPushButton("Bestellen")
            self.setCellWidget(row_number, 8, self.selectionButton)

            self.selectionButton.pressed.connect(lambda: self.sendData(self.sender().parent().row()))
            self.show()
        """
        self.setHorizontalHeaderLabels(horHeaders)  #Header setzen



    def getImageLabel(self, image):
        imageLabel = ImageCruiseShip(image)
        return imageLabel



class Window(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.orderWindow = OrderWindow()
        # Stylesheet
        self.setStyleSheet("QMainWindow{background-image: url(data/images/background/Cruise Background 3_4.jpg) no-repeat center center fixed; background-size: cover;}")

        # creating a widget object
        myQWidget = QWidget()

        #Layout Creation
        ApplicationVerticalLayout = QVBoxLayout()
        myQWidget.setLayout(ApplicationVerticalLayout)

        FilterGridLayout = QGridLayout()
        ApplicationVerticalLayout.addLayout(FilterGridLayout)

        self.table_view = TableView(getTable(), len(getTable()), 8)
        tableLayout = QVBoxLayout()  # Tabellen Layout
        tableLayout.addWidget(self.table_view)
        tableLayout.minimumSize()
        ApplicationVerticalLayout.addLayout(tableLayout)

        self.sendSelectionButton = QPushButton("Auswahl bestellen", self)
        ApplicationVerticalLayout.addWidget(self.sendSelectionButton)


        """
        # Layout
        myVLayout = QVBoxLayout()           # Vertikales BoxLayout
        #myHLayout = QHBoxLayout()           # Horizontales BoxLayout
        myGridLayout = QGridLayout()        # Grid Layout
        myQWidget.setLayout(myVLayout)      # Horizontales Layout als Basis setzen
        #myHLayout.addLayout(myVLayout)      # Vertikales Layout in das horizontale einfügen
        myVLayout.addLayout(myGridLayout)   # Grid Layout in Vertikales Layout einfügen

        #Tabelle ins Hauptlayout einfügen
        self.table_view = TableView(getTable(), len(getTable()), 9)
        tableLayout = QVBoxLayout()  # Tabellen Layout
        tableLayout.addWidget(self.table_view)
        tableLayout.addStretch(0)
        myVLayout.addLayout(tableLayout)
        """
        # central widget
        self.setCentralWidget(myQWidget)

        # creating widgets and their details
        # main window
        self.setObjectName("MainWindow>")
        self.setWindowTitle("Kreuzfahrt-Buchung")
        self.setGeometry(100, 50, 1400, 720)       # x, y, width, height
        self.setWindowIcon(QIcon("data\images\SchiffIcon.png"))

        # Region Auswahl
        self.RegionLabel = QLabel()
        self.RegionLabelErgebnis = QLabel()         # Label zum Anzeigen der Auswahl
            #self.RegionLabelErgebnis.setStyleSheet("background-color: white;")
        self.RegionLabel.setText("Region")
        self.RegionLabel.setStyleSheet("background-color: white;")
        self.RegionComboBox = CheckableComboBox()

        # Uebernachtungen Anzahl
        self.NachtLabel = QLabel()
        self.NachtLabelErgebnis = QLabel()          # Label zum Anzeigen der Auswahl
            #self.NachtLabelErgebnis.setStyleSheet("background-color: white; border-color: black;")
        self.NachtLabel.setText("Uebernachtungen")
        self.NachtLabel.setStyleSheet("background-color: white; border-color: black;")
        self.NachtSpinBox = QSpinBox()
        self.NachtSpinBox.setMinimum(7)
        self.NachtSpinBox.setMaximum(21)

        # Zu besuchende Staedte
        self.StadtLabel = QLabel()
        self.StadtLabelErgebnis = QLabel()          # Label zum Anzeigen der Auswahl
            #self.StadtLabelErgebnis.setStyleSheet("background-color: white;")
        self.StadtLabel.setText("Staedte")
        self.StadtLabel.setStyleSheet("background-color: white;")
        self.StadtComboBox = CheckableComboBox()
            #self.StadtComboBox.setGeometry(QtCore.QRect(310, 70, 200, 41))

        # Schiffstyp Auswahl
        self.SchiffsTypLabel = QLabel()
        self.SchiffsTypLabelErgebnis = QLabel()     # Label zum Anzeigen der Auswahl
            #self.SchiffsTypLabelErgebnis.setStyleSheet("background-color: white;")
        self.SchiffsTypLabel.setText("Schiffstyp")
        self.SchiffsTypLabel.setStyleSheet("background-color: white;")
        self.SchiffsTypComboBox = CheckableComboBox()

        # Such Knopf
        self.SearchButton = QPushButton()
        self.SearchButton.setText("Search")
        #self.SearchButton.setGeometry(730, 20, 61, 41)
        self.SearchButton.setAutoFillBackground(True)
        self.SearchButton.setStyleSheet("background-color: rgb(0, 130, 0); color: white;")

        # adding Widgets to the Grid-layout   (widget, row, column, alignment)
        FilterGridLayout.addWidget(self.RegionLabel, 1, 1)
        FilterGridLayout.addWidget(self.RegionComboBox, 2, 1)
        FilterGridLayout.addWidget(self.RegionLabelErgebnis, 3, 1)

        FilterGridLayout.addWidget(self.NachtLabel, 1, 2)
        FilterGridLayout.addWidget(self.NachtSpinBox, 2, 2)
        FilterGridLayout.addWidget(self.NachtLabelErgebnis, 3, 2)

        FilterGridLayout.addWidget(self.StadtLabel, 1, 3)
        FilterGridLayout.addWidget(self.StadtComboBox, 2, 3)
        FilterGridLayout.addWidget(self.StadtLabelErgebnis, 3, 3)

        FilterGridLayout.addWidget(self.SchiffsTypLabel, 1, 4)
        FilterGridLayout.addWidget(self.SchiffsTypComboBox, 2, 4)
        FilterGridLayout.addWidget(self.SchiffsTypLabelErgebnis, 3, 4)

        FilterGridLayout.addWidget(self.SearchButton, 2, 5)
        #myLayout.addStretch()


        # add items to Region CB
        self.RegionComboBox.addItem("Ostsee")
        self.RegionComboBox.addItem("Nordsee")
        self.RegionComboBox.addItem("Mittelmeer")
        self.RegionComboBox.activated.connect(self.updateCityFilter)

        # traversing items
        #for i in range(1):         # setzt leere checkboxen vor die items (Fehler: for i in range(i) ist die anzahl
                                    # wie viele items eine box bekommen aber auch wie oft die items ge-added werden

        # add items to StadtComboBox with Image Tooltip
        for city_num, city in enumerate(getCityList()):
            self.StadtComboBox.addItem(city)
            if file_exists('./data/images/Hafenstädte/' + city + '.jpg'):
                self.StadtComboBox.setItemData(city_num,
                                               '<img src="./data/images/Hafenstädte/' + city + '.jpg" width="500" height="350" />',
                                               QtCore.Qt.ToolTipRole)
            else:
                self.StadtComboBox.setItemData(city_num,"Kein Vorschaubild vorhanden", QtCore.Qt.ToolTipRole)

            #item = self.StadtComboBox.model().item(i, 0)

            # setting item unchecked
            #item.setCheckState(Qt.Unchecked)

        # add items to Schiffstyp
        self.SchiffsTypComboBox.addItem("A")
        self.SchiffsTypComboBox.addItem("B")
        self.SchiffsTypComboBox.addItem("C")
        self.SchiffsTypComboBox.addItem("D")
        self.SchiffsTypComboBox.addItem("E")
        self.SchiffsTypComboBox.addItem("F")




        #self.SearchComponents() # calling method
        self.show()

        # adding action to button
        #self.RegionComboBox = QComboBox(self)
        self.SearchButton.pressed.connect(self.Search)
        self.sendSelectionButton.pressed.connect(self.sendData)
        #self.RegionLabelErgebnis = QLabel(self)
        #self.RegionComboBox.setGeometry(100, 100, 200, 50)


        #Tabellenkonfiguration
        for x in range(len(getTable())):  # Row-Höhe festlegen
            self.table_view.setRowHeight(x, 128)

        self.table_view.setColumnWidth(4, 256)  # Schiffstypen größer machen für Bilder


    def updateCityFilter(self):
        selectedRegion = []
        filteredCitys = []

        #Clear Filter before refreshing
        for i in range(self.StadtComboBox.count()):
            self.StadtComboBox.clear()

        #Get selected Regions
        for i in range(self.RegionComboBox.count()):
            if self.RegionComboBox.itemChecked(i) == True:
                selectedRegion.append(self.RegionComboBox.itemText(i))

        #Fill City Filter
        for i in range(len(selectedRegion)):
            for city in getCityList(selectedRegion[i]):
                filteredCitys.append(city)

        filteredCitys.sort()
        for cityNum, cityElement in enumerate(filteredCitys):
            self.StadtComboBox.addItem(cityElement)
            if file_exists('./data/images/Hafenstädte/' + city + '.jpg'):
                self.StadtComboBox.setItemData(cityNum,
                                               '<img src="./data/images/Hafenstädte/' + city + '.jpg" width="500" height="350" />',
                                               QtCore.Qt.ToolTipRole)
            else:
                self.StadtComboBox.setItemData(cityNum, "Kein Vorschaubild vorhanden", QtCore.Qt.ToolTipRole)

    def sendData(self):
        currRow = self.table_view.currentRow()
        #naechte = self.table_view.currentRow(2)
        #staedte = self.table_view.item(currRow, x).text()
        data = []

        for x in range(1,8):
            #data.append(self.table_view.horizontalHeaderItem(x).text())
            data.append(self.table_view.item(currRow,x).text())

        #self.orderWindow.input1.setText(str(data))

        # Übergabe des Datensatzes der ausgewählten Reise
        self.orderWindow.cruiseData = data

        """
        self.orderWindow.LaRegion.setText("Region: " + data[0])
        self.orderWindow.LaUebernachtungen.setText("Uebernachtungen: " + data[1])
        #self.orderWindow.LaStadt.setText("Staedte: " + data[2])
        self.orderWindow.LaBuchungsnummer.setText("Buchungsnummer: " + str(random.randrange(2, 999999, 2)))
        self.orderWindow.InnenPreis.setText("Innenkabine\nPreis: " + data[4])
        self.orderWindow.AussenPreis.setText("Aussenkabine\nPreis: " + data[5])
        self.orderWindow.BalkonPreis.setText("Balkonkabine \nPreis: " + data[6])
        """


        # Gesamtpreis notwendig, wenn es keine Personenauswahl gibt?
        #
        # self.orderWindow.LaGestamtpreis.setText("Summe: " + str())

        # Funktion ausführen zum Anzeigen des Fensters
        self.orderWindow.displayWindow()


    # define button action
    def Search(self):

        region = []
        naechte = []
        staedte = []
        typ = []

        for i in range(self.RegionComboBox.count()):
            if self.RegionComboBox.itemChecked(i) == True:
                region.append(self.RegionComboBox.itemText(i))

        for i in range(-2,2):
            naechte.append(self.NachtSpinBox.value()+i)

        for i in range(self.StadtComboBox.count()):
            if self.StadtComboBox.itemChecked(i) == True:
                staedte.append(self.StadtComboBox.itemText(i))

        for i in range(self.SchiffsTypComboBox.count()):
            if self.SchiffsTypComboBox.itemChecked(i) == True:
                typ.append(self.SchiffsTypComboBox.itemText(i))

        FilterErgebnis = [region, naechte, staedte, typ]

        # showing content on the screen though label
        self.RegionLabelErgebnis.setText("Region: " + str(region))
        self.NachtLabelErgebnis.setText("Uebernachtungen: " + str(naechte))
        self.StadtLabelErgebnis.setText("Staedte: " + str(staedte))
        self.SchiffsTypLabelErgebnis.setText("Schiffstyp: " + str(typ))


        #Reset Filter
        for row_count in range(self.table_view.rowCount()):
            self.table_view.showRow(row_count)

        for row_count in range(self.table_view.rowCount()):

            #Check Region
            if len(FilterErgebnis[0]) != 0: # Wenn keine Auswahl, dann zeige alle
                if self.table_view.item(row_count, 1).text() not in FilterErgebnis[0]:
                    self.table_view.hideRow(row_count)

            #Check Übernachtung
            if len(FilterErgebnis[1]) != 0:
                if int(self.table_view.item(row_count, 2).text()) not in FilterErgebnis[1]:
                    self.table_view.hideRow(row_count)

            #Check City
            if len(FilterErgebnis[2]) != 0:
                for cityElement in FilterErgebnis[2]:
                    # Ändern, dass alle ausgewählten Städte enthalten sein MÜSSEN
                    if cityElement in self.table_view.item(row_count, 3).text():
                        break
                    elif cityElement not in self.table_view.item(row_count, 3).text():
                        self.table_view.hideRow(row_count)

            #Check Schiffstyp
            if len(FilterErgebnis[3]) != 0:
                if self.table_view.item(row_count, 4).text() not in FilterErgebnis[3]:
                    self.table_view.hideRow(row_count)







                        #self.table_view.hideRow(row_count)

        """
                for x in range(25):  # Test um spezifische Reihen anhand von Keywords auszublenden
                    #print("Ausgabe table.item(): " + str(self.table_view.item(x, 1)))  # Debug/Testprint
                    checkItem = self.table_view.item(x, 1)
                    #print("Ausgabe des Textes in table.item(): " + checkItem.text())  # Debug/Testprint
                    if checkItem.text() == "Ostsee":
                        self.table_view.hideRow(x)
                """

# drivers code
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())