from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

from os.path import exists as file_exists
import sys
import random
import pandas

IMGPATH = r'data\images\Schiffstypen'  # Schiffstypen Bilder
TABLEPATH = r'data\Schiffreisen.xlsx'  # Excel Tabelle


# Read Excel file
def getTable():
    df = pandas.read_excel(TABLEPATH, header=3, usecols=lambda x: 'Unnamed' not in x, skiprows=range(25, 29))
    dfList = df.values.tolist()

    return dfList


# Get a list of citynames depending on selected region
def getCityList(regiontype="all"):  # example: getCityList("Nordsee")

    FullList = getTable()
    cityList = []

    # Go through excel data and put matching data in cityList[]
    for row_number, row_data in enumerate(FullList):
        for column_number, column_data in enumerate(row_data):
            if column_number == 3:
                if row_data[1] == regiontype or regiontype == "all":
                    cityBuff = column_data.split()
                    for city_num, city_data in enumerate(cityBuff):
                        cityBuff[city_num] = city_data.replace(",", "")
                        if cityBuff[city_num] not in cityList:
                            cityList.append(cityBuff[city_num])
    cityList.sort()
    return cityList


# Dialog window to enter personal data
class PersonalDataDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.editElement = None
        self.labelElement = None
        self.setWindowTitle("Persönliche Daten")
        self.setWindowIcon(QIcon("data\images\SchiffIcon.png"))
        self.setFixedWidth(300)
        self.setFixedHeight(440)

        # Add Personal Information Input
        self.PersonalDataLayout = QGridLayout()
        self.PersonalDataLayout.addWidget(self.createDialog("Name", ["Nachname", "Vorname"]), 0, 0)
        self.PersonalDataLayout.addWidget(self.createDialog("Adresse", ["Postleitzahl", "Ort", "Straße, Hausnummer"]),
                                          1, 0)
        self.PersonalDataLayout.addWidget(self.createDialog("Bankdaten", ["IBAN"]), 2, 0)

        # Save Button
        self.saveButton = QPushButton("Abspeichern", self)
        self.PersonalDataLayout.addWidget(self.saveButton)
        self.saveButton.clicked.connect(self.saveData)

        self.setLayout(self.PersonalDataLayout)

    # Create Dialog Groups with Text Input Fields
    def createDialog(self, groupType, groupElements):
        groupBox = QGroupBox(groupType)
        groupBox.setStyleSheet('QGroupBox {'
                               '    font-size: 11pt;'
                               '    padding: 10 10px;}')
        vLayout = QVBoxLayout()

        for element_num, element in enumerate(groupElements):
            self.labelElement = QLabel(element)
            self.editElement = QLineEdit(self)
            self.editElement.resize(280, 20)

            vLayout.addWidget(self.labelElement)
            vLayout.addWidget(self.editElement)

        groupBox.setLayout(vLayout)
        return groupBox

    # Save Input Data and close Window
    def saveData(self):

        textboxValue = []
        # Get Data from all QLineEdit Widgets in Window Layout
        for i in range(0, 3):
            groupWidget = self.PersonalDataLayout.itemAtPosition(i, 0)
            for textWidget in groupWidget.widget().children():
                if isinstance(textWidget, QLineEdit):
                    textboxValue.append(textWidget.text())

        # Save Data to file
        with open('data\PersonDaten.txt', 'w') as file:
            file.write('\n'.join(textboxValue))

        # Close Window and inform User about completion
        self.close()
        finishDialog = QMessageBox(self)
        finishDialog.setWindowTitle("Bestellung abgeschlossen")
        finishDialog.setText(
            "Bestellung abgeschlossen.\nSie können das Programm nun schließen oder weitere Reisen buchen.")
        finishDialog.exec()

    # Call Window to open
    def displayDialog(self):
        self.show()


# Order Window to show selected cruise with images and cabin selection
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
        self.SchiffsTypVorschau = QLabel(self)
        self.SchiffsTyp = QLabel()
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
        BestellGridLayout.addLayout(self.VerticalLayoutLO, 0, 0)  # (self.layout, reihe, spalte)

        # Layout fuer Kabinen-Preise und Vorschau
        self.hKabinenLayout = QHBoxLayout()
        BestellGridLayout.addLayout(self.hKabinenLayout, 0, 1)
        self.vKabinenPreisLayout = QVBoxLayout()
        self.InnenPreis = QRadioButton()
        self.vKabinenPreisLayout.addWidget(self.InnenPreis)
        self.AussenPreis = QRadioButton()
        self.vKabinenPreisLayout.addWidget(self.AussenPreis)
        self.BalkonPreis = QRadioButton()
        self.vKabinenPreisLayout.addWidget(self.BalkonPreis)
        self.hKabinenLayout.addLayout(self.vKabinenPreisLayout)
        self.vKabinenVorschauLayout = QVBoxLayout()
        self.InnenVorschau = QLabel(self)
        self.vKabinenVorschauLayout.addWidget(self.InnenVorschau)
        self.AussenVorschau = QLabel(self)
        self.vKabinenVorschauLayout.addWidget(self.AussenVorschau)
        self.BalkonVorschau = QLabel(self)
        self.vKabinenVorschauLayout.addWidget(self.BalkonVorschau)
        self.hKabinenLayout.addLayout(self.vKabinenVorschauLayout)

        """
        #self.input1 = QLabel()
        #BestellGridLayout.addWidget(self.input1, 1, 0)  # (self.widget, reihe, spalte)
        self.StadtView = QLabel(self)           # Label zum anzeigen des Bildes der Stadt
        self.VerticalLayoutLO.addWidget(self.StadtView)
        self.vStaedteViewLayout = QVBoxLayout()  # Layout fuer Stadnamen-Label und dessen Buttons
        self.LaStadt = QLabel()                 # Label zum anzeigen des Namen der in "StadtView" angezeigten Stadt
        self.vStaedteViewLayout.addWidget(self.LaStadt)
        #self.LaStadt.setWordWrap(True)
        #BestellGridLayout.addWidget(self.LaStadt, 1, 0)     # (self.widget, reihe, spalte)
        self.hPrevNextButtonLayout = QHBoxLayout()
        self.PrevStadtButton = QPushButton("Vorherige Stadt")
        self.NextStadtButton = QPushButton("Naechste Stadt")
        self.hPrevNextButtonLayout.addWidget(self.PrevStadtButton)
        self.hPrevNextButtonLayout.addWidget(self.NextStadtButton)
        self.vStaedteViewLayout.addLayout(self.hPrevNextButtonLayout)
        #BestellGridLayout.addLayout(self.PrevNextButtonLayout, 1, 0)    # (self.widget, reihe, spalte)
        BestellGridLayout.addLayout(self.VerticalLayoutLO, 1, 0)
        """

        self.StadtView = QLabel(self)                           # Label zum anzeigen des Bildes der Stadt
        self.VerticalLayoutLO.addWidget(self.StadtView)
        self.vStaedteViewLayout = QVBoxLayout()                 # Layout fuer Stadtnamen-Label und darunter dessen Buttons
        self.LaStadt = QLabel()                                 # Label zum anzeigen des Namen der in "StadtView" angezeigten Stadt
        self.vStaedteViewLayout.addWidget(self.LaStadt)         # Hinzufuegen des Widgets in das QVBoxlayout
        self.hPrevNextButtonLayout = QHBoxLayout()              # Horizontales Box Layout um die Buttons nebeneinander zu haben
        self.PrevStadtButton = QPushButton("Vorherige Stadt")
        self.NextStadtButton = QPushButton("Naechste Stadt")
        self.hPrevNextButtonLayout.addWidget(self.PrevStadtButton)
        self.hPrevNextButtonLayout.addWidget(self.NextStadtButton)
        self.vStaedteViewLayout.addLayout(self.hPrevNextButtonLayout)
        BestellGridLayout.addLayout(self.VerticalLayoutLO, 0, 0)
        BestellGridLayout.addLayout(self.vStaedteViewLayout, 1, 0)



        self.vBestaetigungsLayout = QVBoxLayout()
        self.LaGesamtpreis = QLabel("Summe: ...€")
        self.LaGesamtpreis.setAlignment(QtCore.Qt.AlignCenter)
        self.vBestaetigungsLayout.addWidget(self.LaGesamtpreis)
        self.ConfirmButton = QPushButton('Buchen')
        self.ConfirmButton.clicked.connect(self.confirmOrder)
        self.vBestaetigungsLayout.addWidget(self.ConfirmButton)
        # BestellGridLayout.addWidget(self.ConfirmButton, 1, 1)
        BestellGridLayout.addLayout(self.vBestaetigungsLayout, 1, 1)

        self.setLayout(BestellGridLayout)

    # Confirm Order, open personalDataDialog
    def confirmOrder(self):
        self.personalDataDialog.displayDialog()
        self.close()

    # imagePath = IMGPATH + "\Schiffstyp " + str(column_data) + ".jpg"

    # Open Order Window at put selected cruise data in Labels
    def displayWindow(self):
        self.LaRegion.setText("Region: " + self.cruiseData[0])
        self.LaUebernachtungen.setText("Uebernachtungen: " + self.cruiseData[1])
        self.LaBuchungsnummer.setText("Buchungsnummer: " + str(random.randrange(2, 999999, 2)))
        self.LaStadt.setText("Staedte: \n" + self.cruiseData[2])
        self.SchiffsTyp.setText("Schiffstyp: " + self.cruiseData[3])
        self.SchiffsTypPixmap = QPixmap('data/images/Schiffstypen/Schiffstyp ' + str(self.cruiseData[3]))
        SchiffsTypPixmap = self.SchiffsTypPixmap.scaled(
            QtCore.QSize(300, 172),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        self.SchiffsTypVorschau.setPixmap(SchiffsTypPixmap)
        self.InnenPreis.setText("Innenkabine\nPreis: " + self.cruiseData[4])
        self.InnenKabinePixmap = QPixmap('data/images/Kabinentypen/Innenkabine.jpg')
        InnenKabinePixmap = self.InnenKabinePixmap.scaled(
            QtCore.QSize(300, 172),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        self.InnenVorschau.setPixmap(InnenKabinePixmap)
        self.AussenPreis.setText("Aussenkabine\nPreis: " + self.cruiseData[5])
        self.AussenKabinePixmap = QPixmap('data/images/Kabinentypen/Aussenkabine.jpg')
        AussenKabinePixmap = self.AussenKabinePixmap.scaled(
            QtCore.QSize(300, 172),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        self.AussenVorschau.setPixmap(AussenKabinePixmap)
        self.BalkonPreis.setText("Balkonkabine \nPreis: " + self.cruiseData[6])
        self.BalkonKabinePixmap = QPixmap('data/images/Kabinentypen/Balkonkabine.jpg')
        BalkonKabinePixmap = self.BalkonKabinePixmap.scaled(
            QtCore.QSize(300, 172),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        self.BalkonVorschau.setPixmap(BalkonKabinePixmap)
        #for i in range(self.cruiseData[2].count()):
        cityviewlist = self.cruiseData[2]
        #self.StadtViewPixmap = QPixmap('data/images/Hafenstädte' + str(cityviewlist) + '.jpg')
        #self.StadtViewPixmap = QPixmap('data/images/Hafenstädte' + str(self.cruiseData[2]) + '.jpg') # geht warhscheinlich nicht da er mit cruiseData[2] alle staedte nimmt
        # self.StadtViewPixmap = QPixmap('data/images/Hafenstädte/Aberdeen.jpg')
        # StadtViewPixmap = self.StadtViewPixmap.scaled(
        #     QtCore.QSize(256, 128),
        #     Qt.KeepAspectRatioByExpanding,
        #     Qt.SmoothTransformation
        # )
        # self.StadtView.setPixmap(StadtViewPixmap)


        self.StadtViewPixmap = QPixmap('./data/images/Hafenstädte/Aberdeen.jpg')
        StadtViewPixmap = self.StadtViewPixmap.scaled(
            QtCore.QSize(350, 222),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        self.StadtView.setPixmap(StadtViewPixmap)



        print(self.cruiseData)
        self.show()


# Class to show Cruisship image
class ImageCruiseShip(QWidget):

    def __init__(self, image):
        super(ImageCruiseShip, self).__init__()

        self.labelImage = QLabel(self)
        self.pixmap = QPixmap(image)
        image_aspect = self.pixmap.size().width() / self.pixmap.size().height()

        # Scale image
        pixmap = self.pixmap.scaled(
            QtCore.QSize(256, 128),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )

        self.labelImage.setPixmap(pixmap)
        # Vertically align Label
        #self.labelImage.move(0, -128 * ((2 - image_aspect) / 2))


# creating checkable combo box class which will stay open after a selection
class CheckableComboBox(QComboBox):
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
        self._changed = False  # verhindert, dass wenn die combobox geoeffnett ist, man nichts anderes anklicken kann

    def itemChecked(self, index):
        item = self.model().item(index, self.modelColumn())
        return item.checkState() == QtCore.Qt.Checked

    def setItemChecked(self, index, checked=True):
        item = self.model().item(index, self.modelColumn())
        if checked:
            item.setCheckState(QtCore.Qt.Checked)
        else:
            item.setCheckState(QtCore.Qt.Unchecked)


# Tabelle
def getImageLabel(image):
    imageLabel = ImageCruiseShip(image)
    return imageLabel


class TableView(QTableWidget):
    def __init__(self, data, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.setData()

        self.setStyleSheet(
            "font-size: 12pt; background-color: rgba(255, 255, 255, 0.6); selection-background-color: rgba(156,222,"
            "255, 0.8); selection-color: black;")
        self.setSelectionBehavior(QAbstractItemView.SelectRows)  # Whole Row will be marked on click
        self.setSelectionMode(QAbstractItemView.SingleSelection)  # Only one Row can be selected at any time
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Data cant be edited
        #self.resizeColumnsToContents()
        self.resizeRowsToContents()
        # Column Spacing
        self.setColumnWidth(3, 400)
        for i in range(0,7):
            if i != 3:
                self.resizeColumnToContents(i)

    # Put data from Excel file in table
    def setData(self):
        # Create Header
        horHeaders = ["Reisenummer", "Meeresart", "Anzahl\nÜbernachtungen", "Besuchte Städte", "Schiffstyp",
                      "Preis\nInnenkabine", "Preis\nAußenkabine", "Preis\nBalkonkabine"]



        # Schleife, die alle Tabellenelemente durchgeht
        for row_number, row_data in enumerate(self.data):
            for column_number, column_data in enumerate(row_data):


                # Put image instead of text for cruisship kind
                if column_number == 4:
                    imagePath = IMGPATH + "\Schiffstyp " + str(column_data) + ".jpg"
                    item = getImageLabel(imagePath)
                    self.setCellWidget(row_number, column_number, item)

                # Format pricing
                if 5 <= column_number <= 7:
                    if column_data != "nicht vorhanden":
                        newItem = QTableWidgetItem(str(column_data) + " €")
                    else:
                        newItem = QTableWidgetItem(str(column_data))
                else:
                    newItem = QTableWidgetItem(str(column_data))

                newItem.setTextAlignment(Qt.AlignCenter)
                self.setItem(row_number, column_number, newItem)
                self.show()

        # Set Header
        self.setHorizontalHeaderLabels(horHeaders)

    # Get resized and repositioned image


# Main Window
class Window(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.orderWindow = OrderWindow()
        # Stylesheet
        self.setStyleSheet(
            "QMainWindow{background-image: url(data/images/background/Cruise Background 3_4.jpg) no-repeat center "
            "center fixed; background-size: cover;}")

        # creating a widget object
        myQWidget = QWidget()

        # Layout Creation
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

        # central widget
        self.setCentralWidget(myQWidget)

        # creating widgets and their details
        # main window
        self.setObjectName("MainWindow>")
        self.setWindowTitle("Kreuzfahrt-Buchung")
        self.setGeometry(100, 50, 1400, 720)  # x, y, width, height
        self.setWindowIcon(QIcon("data\images\SchiffIcon.png"))

        # Region Auswahl
        self.RegionLabel = QLabel()
        self.RegionLabelErgebnis = QLabel()  # Label zum Anzeigen der Auswahl
        # self.RegionLabelErgebnis.setStyleSheet("background-color: white;")
        self.RegionLabel.setText("Region")
        self.RegionLabel.setStyleSheet("background-color: white;")
        self.RegionComboBox = CheckableComboBox()

        # Uebernachtungen Anzahl
        self.NachtLabel = QLabel()
        self.NachtLabelErgebnis = QLabel()  # Label zum Anzeigen der Auswahl
        # self.NachtLabelErgebnis.setStyleSheet("background-color: white; border-color: black;")
        self.NachtLabel.setText("Uebernachtungen")
        self.NachtLabel.setStyleSheet("background-color: white; border-color: black;")
        self.NachtSpinBox = QSpinBox()
        self.NachtSpinBox.setMinimum(7)
        self.NachtSpinBox.setMaximum(21)

        # Zu besuchende Staedte
        self.StadtLabel = QLabel()
        self.StadtLabelErgebnis = QLabel()  # Label zum Anzeigen der Auswahl
        # self.StadtLabelErgebnis.setStyleSheet("background-color: white;")
        self.StadtLabel.setText("Staedte")
        self.StadtLabel.setStyleSheet("background-color: white;")
        self.StadtComboBox = CheckableComboBox()
        # self.StadtComboBox.setGeometry(QtCore.QRect(310, 70, 200, 41))

        # Schiffstyp Auswahl
        self.SchiffsTypLabel = QLabel()
        self.SchiffsTypLabelErgebnis = QLabel()  # Label zum Anzeigen der Auswahl
        # self.SchiffsTypLabelErgebnis.setStyleSheet("background-color: white;")
        self.SchiffsTypLabel.setText("Schiffstyp")
        self.SchiffsTypLabel.setStyleSheet("background-color: white;")
        self.SchiffsTypComboBox = CheckableComboBox()

        # Such Knopf
        self.SearchButton = QPushButton()
        self.SearchButton.setText("Search")
        # self.SearchButton.setGeometry(730, 20, 61, 41)
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
        # myLayout.addStretch()

        # add items to Region CB
        self.RegionComboBox.addItem("Ostsee")
        self.RegionComboBox.addItem("Nordsee")
        self.RegionComboBox.addItem("Mittelmeer")
        self.RegionComboBox.activated.connect(self.updateCityFilter)

        # traversing items
        # for i in range(1):         # setzt leere checkboxen vor die items (Fehler: for i in range(i) ist die anzahl
        # wie viele items eine box bekommen aber auch wie oft die items ge-added werden

        # add items to StadtComboBox with Image Tooltip
        for city_num, city in enumerate(getCityList()):
            self.StadtComboBox.addItem(city)
            if file_exists('./data/images/Hafenstädte/' + city + '.jpg'):
                self.StadtComboBox.setItemData(city_num,
                                               '<img src="./data/images/Hafenstädte/' + city + '.jpg" width="500" '
                                                                                               'height="350" />',
                                               QtCore.Qt.ToolTipRole)
            else:
                self.StadtComboBox.setItemData(city_num, "Kein Vorschaubild vorhanden", QtCore.Qt.ToolTipRole)

            # item = self.StadtComboBox.model().item(i, 0)

            # setting item unchecked
            # item.setCheckState(Qt.Unchecked)

        # add items to Schiffstyp
        self.SchiffsTypComboBox.addItem("A")
        self.SchiffsTypComboBox.addItem("B")
        self.SchiffsTypComboBox.addItem("C")
        self.SchiffsTypComboBox.addItem("D")
        self.SchiffsTypComboBox.addItem("E")
        self.SchiffsTypComboBox.addItem("F")

        # self.SearchComponents() # calling method
        self.show()

        # adding action to button
        # self.RegionComboBox = QComboBox(self)
        self.SearchButton.pressed.connect(self.Search)
        self.sendSelectionButton.pressed.connect(self.sendData)
        # self.RegionLabelErgebnis = QLabel(self)
        # self.RegionComboBox.setGeometry(100, 100, 200, 50)

        # Tabellenkonfiguration
        for x in range(len(getTable())):  # Row-Höhe festlegen
            self.table_view.setRowHeight(x, 128)

        self.table_view.setColumnWidth(4, 256)  # Schiffstypen größer machen für Bilder

    def updateCityFilter(self):
        selectedRegion = []
        filteredCitys = []

        # Clear Filter before refreshing
        for i in range(self.StadtComboBox.count()):
            self.StadtComboBox.clear()

        # Get selected Regions
        for i in range(self.RegionComboBox.count()):
            if self.RegionComboBox.itemChecked(i):
                selectedRegion.append(self.RegionComboBox.itemText(i))

        # Fill City Filter
        if len(selectedRegion) != 0:
            for i in range(len(selectedRegion)):
                for city in getCityList(selectedRegion[i]):
                    filteredCitys.append(city)
        else:
            for city_num, city in enumerate(getCityList()):
                filteredCitys.append(city)

        filteredCitys.sort()

        # Add Image Tooltip
        for cityNum, cityElement in enumerate(filteredCitys):
            self.StadtComboBox.addItem(cityElement)
            if file_exists('./data/images/Hafenstädte/' + cityElement + '.jpg'):
                self.StadtComboBox.setItemData(cityNum,
                                               '<img src="./data/images/Hafenstädte/' + cityElement + '.jpg" '
                                                                                                      'width="500" '
                                                                                                      'height="350" '
                                                                                                      '/>',
                                               QtCore.Qt.ToolTipRole)
            else:
                self.StadtComboBox.setItemData(cityNum, "Kein Vorschaubild vorhanden", QtCore.Qt.ToolTipRole)

    # Send selected trip information to order window
    def sendData(self):
        currRow = self.table_view.currentRow()
        data = []

        for x in range(1, 8):
            # data.append(self.table_view.horizontalHeaderItem(x).text())
            data.append(self.table_view.item(currRow, x).text())

        # self.orderWindow.input1.setText(str(data))

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
            if self.RegionComboBox.itemChecked(i):
                region.append(self.RegionComboBox.itemText(i))

        for i in range(-2, 3):
            naechte.append(self.NachtSpinBox.value() + i)

        for i in range(self.StadtComboBox.count()):
            if self.StadtComboBox.itemChecked(i):
                staedte.append(self.StadtComboBox.itemText(i))

        for i in range(self.SchiffsTypComboBox.count()):
            if self.SchiffsTypComboBox.itemChecked(i):
                typ.append(self.SchiffsTypComboBox.itemText(i))

        FilterErgebnis = [region, naechte, staedte, typ]

        # showing content on the screen though label
        self.RegionLabelErgebnis.setText("Region: " + str(region))
        self.NachtLabelErgebnis.setText("Uebernachtungen: " + str(naechte))
        self.StadtLabelErgebnis.setText("Staedte: " + str(staedte))
        self.SchiffsTypLabelErgebnis.setText("Schiffstyp: " + str(typ))

        # Reset Filter
        for row_count in range(self.table_view.rowCount()):
            self.table_view.showRow(row_count)

        for row_count in range(self.table_view.rowCount()):

            # Check Region
            if len(FilterErgebnis[0]) != 0:  # Wenn keine Auswahl, dann zeige alle
                if self.table_view.item(row_count, 1).text() not in FilterErgebnis[0]:
                    self.table_view.hideRow(row_count)

            # Check Übernachtung
            if len(FilterErgebnis[1]) != 0:
                if int(self.table_view.item(row_count, 2).text()) not in FilterErgebnis[1]:
                    self.table_view.hideRow(row_count)

            # Check City
            if len(FilterErgebnis[2]) != 0:
                for cityElement in FilterErgebnis[2]:
                    # Ändern, dass alle ausgewählten Städte enthalten sein MÜSSEN
                    if cityElement in self.table_view.item(row_count, 3).text():
                        break
                    elif cityElement not in self.table_view.item(row_count, 3).text():
                        self.table_view.hideRow(row_count)

            # Check Schiffstyp
            if len(FilterErgebnis[3]) != 0:
                if self.table_view.item(row_count, 4).text() not in FilterErgebnis[3]:
                    self.table_view.hideRow(row_count)


# drivers code
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
