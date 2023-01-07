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
        self.cityData = []
        self.currCityIndex = 0
        self.setWindowTitle('Bestellung')
        self.setWindowIcon(QIcon("data\images\SchiffIcon.png"))
        self.setGeometry(150, 150, 560, 760)
        self.setFixedWidth(760)
        self.setFixedHeight(560)
        self.setStyleSheet("""
            background-color: rgb(252, 237, 217);
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
        self.LaInform = QLabel("Hier sehen Sie die Zusammenfassung Ihrer ausgewählten Reise.\nWählen Sie bitte noch Ihre gewünschte Kabinenart aus:")
        self.LaInform.setStyleSheet("font-size: 18px")
        #self.LaInform.setWordWrap(True)
        BestellGridLayout.addWidget(self.LaInform, 0, 0, 1, 0)      # row, column, row-span, column-span

        # ===== VerticalLayout ===== LayoutBox für Schiffstyp- & Staedtebilder Widget
        self.VerticalLayoutLO = QVBoxLayout()

        # ===== Schiffstyp Layout ===== LayoutBox für Schiffstyp-Widget
        self.SchiffstypLayout = QVBoxLayout()
        self.SchiffsTypVorschau = QLabel(self)
        self.SchiffsTypVorschau.resize(330, 202)
        self.SchiffsTyp = QLabel()
        self.SchiffsTyp.setAlignment(QtCore.Qt.AlignCenter)
        self.SchiffstypLayout.addWidget(self.SchiffsTypVorschau)
        self.SchiffstypLayout.addWidget(self.SchiffsTyp)
        self.VerticalLayoutLO.addLayout(self.SchiffstypLayout)
        #self.VerticalLayoutLO.addStretch()

        # ===== Reise Informationen ===== Anzeige der Informationen zur ausgewaehlten Reise
        self.LaRegion = QLabel("Region: ")
        self.VerticalLayoutLO.addWidget(self.LaRegion)
        self.LaUebernachtungen = QLabel("Uebernachtungen: ")
        self.VerticalLayoutLO.addWidget(self.LaUebernachtungen)
        self.LaBuchungsnummer = QLabel()
        self.VerticalLayoutLO.addWidget(self.LaBuchungsnummer)
        #self.VerticalLayoutLO.addStretch()
        #BestellGridLayout.addLayout(self.VerticalLayoutLO, 1, 0)  # (self.layout, reihe, spalte)

        # =========================================================
        # Alte Staedte View Ansicht
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
        # ======================================================

        # ===== StaedteViewChangeButton ===== Button zum Wechseln der Bilderansicht von Einzelnen Bilder zu einer Bilderliste
        # Create Menu to switch City View
        self.changeCityViewButton = QPushButton("Städte-Ansicht wechseln", self)
        changeCityViewMenu = QMenu(self)
        singleAction = QAction("Einzelansicht", self)
        singleAction.triggered.connect(lambda: self.changeCityView("single"))
        listAction = QAction("Ansicht als Liste", self)
        listAction.triggered.connect(lambda: self.changeCityView("list"))
        changeCityViewMenu.addAction(singleAction)
        changeCityViewMenu.addAction(listAction)
        self.changeCityViewButton.setMenu(changeCityViewMenu)
        self.VerticalLayoutLO.addWidget(self.changeCityViewButton)
        self.changeCityViewButton.resize(self.changeCityViewButton.sizeHint())

        # ===== Single City Image Layout ===== Layout Information für einzelne Bilderanzeige
        self.SingleCityView = QWidget()                             # Pack Single-City-Preview-Layout in a Widget, to allow hiding it
        self.SingleCityViewLayout = QVBoxLayout()
        self.SingleCityView.setLayout(self.SingleCityViewLayout)
        self.StadtView = QLabel(self)                               # Label zum anzeigen des Bildes der Stadt
        self.VerticalLayoutLO.addWidget(self.SingleCityView)

        # #========================================
        # List of Citys Layout
        # Dieses Widget muss an die gleiche Stelle, wie das Widget obendrüber
        #
        #1 self.view = QtWidgets.QWidget()                          # view widget erstellen
        #2 self.layout = QtWidgets.QVBoxLayout(self.view)           # layout erstellen
        #3 self.scroll = QtWidgets.QScrollArea(self)                # scrollarea erstellen
        #4 self.scroll.setWidgetResizable(True)                     # scrollarea resizable machen
        #5 self.scroll.setWidget(self.view)                         # scrollarea
        #6 self.setCentralWidget(self.scroll)                       # scrollarea als central widget setzen (machen wir ja nicht)
        #

        # self.ListCityView = QWidget()                                   #1 widget erstellen um es verstecken zu können
        # self.ListCityViewLayout = QVBoxLayout(self.ListCityView)        #2 layout im widget erstellen
        # self.ListCityScrollArea = QScrollArea(self)                     #3
        # self.ListCityScrollArea.setWidgetResizable(True)                #4
        # self.ListCityScrollArea.setWidget(self.ListCityView)            #5
        #self.ScrollContent = QWidget()


        # Widget mit Layout darin, mit Scroll-Area darin
        #self.ListCityView = QWidget()                                   # Pack Single-City-Preview-Layout in a Widget, to allow hiding it #1 self.view = QtWidgets.QWidget()                  # view widget erstellen
        #self.ListCityViewLayout = QVBoxLayout(self.ListCityView)        #2 self.layout = QtWidgets.QVBoxLayout(self.view)   # layout erstellen
        #self.ListCityView.setLayout(self.ListCityViewLayout)
        #ListCityScroll = QScrollArea(self)                              #3 self.scroll = QtWidgets.QScrollArea(self)        # scrollarea erstellen
        #ListCityScroll.setWidgetResizable(True)                         #4 self.scroll.setWidgetResizable(True)             # scrollarea resizable machen
        #ScrollContent = QWidget(ListCityScroll)
        #ScrollLayout = QVBoxLayout(ScrollContent)
        #ScrollContent.setLayout(ScrollLayout)
        #self.ListCityViewLayout.addWidget(ListCityScroll)               #6 Scroll Area in Layout bringen

        #ListCityScroll.setWidget(ScrollContent)
        #self.VerticalLayoutLO.addWidget(self.ListCityView)


        # Scroll-Area mit Widget darin, mit Layout darin
        self.ListCityScrollArea = QScrollArea(self)                      # Scrollarea erstellen
        self.ListCityScrollArea.setWidgetResizable(True)                 # Scroll-Area resizable machen
        self.ListCityScrollArea.setFixedHeight(202)
        #ListCityScrollArea.setContentsMargins(, 0, 0, 0, 0)
        self.ScrollContent = QWidget(self.ListCityScrollArea)                 # Inhalt-Widget mit Scrollarea als parent?
        self.ScrollLayout = QVBoxLayout(self.ScrollContent)                   # scroll-layout mit scroll-content als parent?
        self.ScrollContent.setLayout(self.ScrollLayout)                       # Content layout zuweisen zu Content
        self.ListCityScrollArea.setWidget(self.ScrollContent)                 # der Scroll-Area das inhalt-widget zuweisen
        self.ListCityView = QWidget()                               # Widget erstellen
        self.ListCityViewLayout = QVBoxLayout(self.ListCityView)    # Layout für widget erstellen
        self.ListCityViewLayout.setContentsMargins(0, 0, 0, 0)      # Margin setzen damit inhalt weiter links ist

        self.ScrollLayout.addWidget(self.ListCityView)                   # Widget in Scroll-Layout setzen

        self.VerticalLayoutLO.addWidget(self.ListCityScrollArea)         # ScrollArea in Layout setzen
        # ======================================================


        # self.StadtView.resize(330, 202)
        self.SingleCityViewLayout.addWidget(self.StadtView)
        #self.vStaedteViewLayout = QVBoxLayout()  # Layout fuer Stadtnamen-Label und darunter dessen Buttons
        self.LaStadt = QLabel()  # Label zum anzeigen des Namen der in "StadtView" angezeigten Stadt
        self.SingleCityViewLayout.addWidget(self.LaStadt)  # Hinzufuegen des Widgets in das QVBoxlayout
        self.hPrevNextButtonLayout = QHBoxLayout()  # Horizontales Box Layout um die Buttons nebeneinander zu haben

        # ===== Bilder Vor- & Zurueckbuttons =====
        self.PrevStadtButton = QPushButton("Vorherige Stadt")
        self.PrevStadtButton.setStyleSheet("background-color: rgb(208, 255, 163);")
        self.NextStadtButton = QPushButton("Naechste Stadt")
        self.NextStadtButton.setStyleSheet("background-color: rgb(208, 255, 163);")

        self.hPrevNextButtonLayout.addWidget(self.PrevStadtButton)
        self.hPrevNextButtonLayout.addWidget(self.NextStadtButton)
        self.PrevStadtButton.clicked.connect(lambda: self.updateCityLabel(-1))
        self.NextStadtButton.clicked.connect(lambda: self.updateCityLabel(1))

        self.SingleCityViewLayout.addLayout(self.hPrevNextButtonLayout)
        BestellGridLayout.addLayout(self.VerticalLayoutLO, 1, 0, 3, 1, )  # row, column, r-span, c-span
        #BestellGridLayout.addLayout(self.vStaedteViewLayout, 0, 0)

        """
        # List of Citys Layout
        # Dieses Widget muss an die gleiche Stelle, wie das Widget obendrüber
        # 
        self.MultiCityView = QWidget()
        self.VerticalLayoutLO.addWidget(self.SingleCityView)
        self.MultiCityViewLayout = QVBoxLayout()

        MultiCityScroll = QScrollArea(self)
        self.MultiCityViewLayout.addWidget(MultiCityScroll)
        MultiCityScroll.setWidgetResizable(True)
        ScrollContent = QWidget(MultiCityScroll)

        ScrollLayout = QVBoxLayout(ScrollContent)
        ScrollContent.setLayout(ScrollLayout)

        # Die for-Schleife muss in displayWindow() ODER changeCityView(), in __init__ ist self.cruiseData[2] noch leer
        for city in ["test", "test","test","test","test","test","test"]:  # self.cruiseData[2]
            # Stadtname
            CityName = QLabel(city)
            ScrollLayout.addWidget(CityName)

            # Bild erstellen
            CityImage = QLabel()
            ScrollLayout.addWidget(CityImage)
            # Spacer nach jeder Vorschau?
        MultiCityScroll.setWidget(ScrollContent)
        """

        # Layout fuer Kabinen-Preise und Vorschau
        # ===== KabinenLayout ===== LayoutBox zur Auswahl der zu Buchbaren Kabine
        self.hKabinenLayout = QHBoxLayout()
        BestellGridLayout.addLayout(self.hKabinenLayout, 1, 1,)
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

        # ===== BestaetigungsLayout ===== LayoutBox welche den Summenpreis & Buchungsbutton beinhaltet
        self.vBestaetigungsLayout = QVBoxLayout()
        self.LaGesamtpreis = QLabel("Summe: ......€")
        self.LaGesamtpreis.setAlignment(QtCore.Qt.AlignCenter)  # Text in die mitte setzen
        self.vBestaetigungsLayout.addWidget(self.LaGesamtpreis)
        self.ConfirmButton = QPushButton('Buchen')
        self.ConfirmButton.setStyleSheet("background-color: rgb(208, 255, 163);")
        self.ConfirmButton.clicked.connect(self.confirmOrder)
        self.vBestaetigungsLayout.addWidget(self.ConfirmButton)
        # BestellGridLayout.addWidget(self.ConfirmButton, 1, 1)
        BestellGridLayout.addLayout(self.vBestaetigungsLayout, 2, 1)
        # ===== Festlegung & Bestätigung des Layouts =====
        self.setLayout(BestellGridLayout)

    # Confirm Order, open personalDataDialog
    def confirmOrder(self):
        self.personalDataDialog.displayDialog()
        self.close()

    # Open Order Window and put selected cruise data in Labels
    def displayWindow(self):

        self.currCityIndex = 0

        # Create List of Citys out of String
        cityString = self.cruiseData[2]
        self.cityData = cityString.split(", ")
        # s = 0  # anzahl splits
        # for cityviewlist in enumerate:
        #     print(s)
        #     print(cityviewlist)
        print(self.cruiseData)
        print("-----create City Info-----------")
        print(self.currCityIndex)
        print(cityString)
        print(self.cityData)

        self.updateCityLabel(0)

        self.LaRegion.setText("Region: " + self.cruiseData[0])
        self.LaUebernachtungen.setText("Uebernachtungen: " + self.cruiseData[1])
        self.LaBuchungsnummer.setText("Buchungsnummer: " + str(random.randrange(2, 999999, 2)))
        self.SchiffsTyp.setText("Schiffstyp: " + self.cruiseData[3])
        self.SchiffsTypPixmap = QPixmap('data/images/Schiffstypen/Schiffstyp ' + str(self.cruiseData[3]))

        img_width = self.SchiffsTypPixmap.size().width()
        img_height = self.SchiffsTypPixmap.size().height()

        SchiffsTypPixmap = self.SchiffsTypPixmap.scaled(
            QtCore.QSize(330, 202),     # width, height
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        self.SchiffsTypVorschau.setPixmap(SchiffsTypPixmap)

        if (img_width / img_height) < 1.63:  # If Aspect Ratio < Frame Aspect Ratio: center vertical
            y = abs((img_height / (
                        img_width / 330) - 202) / 2)  # Get Pixel Difference between scaled Image and original Image (Cut section)
            self.SchiffsTypVorschau.move(0, int(-y))

        elif (img_width / img_height) > 1.63:  # If Aspect Ratio > Frame Aspect Ratio: center horizontal
            x = abs((img_width / (
                        img_height / 202) - 330) / 2)  # Get Pixel Difference between scaled Image and original Image (Cut section)
            self.SchiffsTypVorschau.move(int(-x), 0)

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
            QtCore.QSize(300, 172), # old values 300, 172
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        self.BalkonVorschau.setPixmap(BalkonKabinePixmap)

        #print(cityviewlist[i])

        # for i in range(self.cruiseData[2].count()):
        # self.StadtViewPixmap = QPixmap('data/images/Hafenstädte' + str(cityviewlist) + '.jpg')

        # self.cruiseData[2] = koblenz, wormms, bobenheim, mannheim
        #
        # QPixmap('data/images/Hafenstädte/' + self.cruiseData[2][i+1] + '.jpg')
        # i = 1
        #
        # while i > 0
        #     prevpushbutton = i-1;
        # while i < self.cruiseData[2].count()
        #     nextbutton = i+1

        # Reset City-Pointer after calling bestellwindow
        # if self.displayWindow.isVisible() == False:



        #self.PrevStadtButton.clicked.connect(lambda: self.stadtbuttons(self.stadtstelle))
        #self.NextStadtButton.clicked.connect(lambda: self.stadtbuttons(self.stadtstelle))

        #if self.PrevStadtButton.clicked()
        # if self.stadtstelle == 0:
        #     #self.PrevStadtButton.setText(" ")
        #     self.PrevStadtButton.hide()
        # elif self.stadtstelle + 1 == stadtanzahl:
        #     #self.NextStadtButton.setText(" ")
        #     self.NextStadtButton.hide()
        # else:
        #     self.PrevStadtButton.show()
        #     self.NextStadtButton.show()

        """
        self.LaStadt.setText("Stadt: " + cityviewlist[self.stadtstelle])
        self.StadtViewPixmap = QPixmap('data/images/Hafenstädte/' + cityviewlist[self.stadtstelle] + '.jpg')
        StadtViewPixmap = self.StadtViewPixmap.scaled(
            QtCore.QSize(350, 222),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        self.StadtView.setPixmap(StadtViewPixmap)
        """

        self.show()

        # print(self.cruiseData[2])
        # self.cityviewlist = list()
        # self.tempcruiseData = self.cruiseData[2]
        # for i in range self.tempcruiseData:
        #     while i != ("," & " "):
        #         i+1
        #         self.templist = list()
        #     self.templist.extned(i)
        #     self.cityviewlist.append(self.templist)
        #     self.templist.remove()
        #
        #     self.cityviewlist.extend(self.cruiseData[2])
        # print(self.cityviewlist)
        # for c in range(self.cityviewlist.count()):
        #     min = 0
        #     max =

        # radiobutton mit funktion verbinden
        self.InnenPreis.clicked.connect(self.summecheck)
        self.AussenPreis.clicked.connect(self.summecheck)
        self.BalkonPreis.clicked.connect(self.summecheck)

    # # Die for-Schleife muss in displayWindow() ODER changeCityView(), in __init__ ist self.cruiseData[2] noch leer
    # for city in ["test", "test", "test", "test", "test", "test", "test"]:  # self.cruiseData[2]
    #     # Stadtname
    #     CityName = QLabel(city)
    #     self.orderWindow.ScrollLayout.addWidget(CityName)
    #
    #     # Bild erstellen
    #     CityImage = QLabel()
    #     self.orderWindow.ScrollLayout.addWidget(CityImage)
    #     # Spacer nach jeder Vorschau?

    # Funktion um SUmme passend zur Auswahl zu setzen
    def summecheck(self):
        if self.InnenPreis.isChecked():
            self.LaGesamtpreis.setText("Summe: " + self.cruiseData[4])
        elif self.AussenPreis.isChecked():
            self.LaGesamtpreis.setText("Summe: " + self.cruiseData[5])
        elif self.BalkonPreis.isChecked():
            self.LaGesamtpreis.setText("Summe: " + self.cruiseData[6])
        else:
            self.LaGesamtpreis.setText("Summe: ......€")

    def updateCityLabel(self, counter):
        self.currCityIndex = self.currCityIndex + counter

        if 0 <= self.currCityIndex < len(self.cityData):

            self.PrevStadtButton.show()
            self.NextStadtButton.show()

            self.LaStadt.setText("Stadt: " + self.cityData[self.currCityIndex])

            # prüfen ob Bild vorhanden ist
            if file_exists('data/images/Hafenstädte/' + self.cityData[self.currCityIndex] + '.jpg') == True:
                self.StadtViewPixmap = QPixmap('data/images/Hafenstädte/' + self.cityData[self.currCityIndex] + '.jpg')
                StadtViewPixmap = self.StadtViewPixmap.scaled(
                    QtCore.QSize(330, 202),     # (old values: 330, 202  # new values 370, 242
                    Qt.KeepAspectRatioByExpanding,
                    Qt.SmoothTransformation,
                )
                self.StadtView.setPixmap(StadtViewPixmap)
            elif file_exists('data/images/Hafenstädte/' + self.cityData[self.currCityIndex] + '.jpg') == False:
                self.StadtViewPixmap = QPixmap('data/images/Hafenstädte/keinevorschau2.jpg')
                StadtViewPixmap = self.StadtViewPixmap.scaled(
                    QtCore.QSize(330, 202),  # (old values: 330, 202  # new values 370, 242
                    Qt.KeepAspectRatioByExpanding,
                    Qt.SmoothTransformation,
                )
                self.StadtView.setPixmap(StadtViewPixmap)

        if self.currCityIndex == 0:
            self.PrevStadtButton.hide()
        elif self.currCityIndex == len(self.cityData) - 1:
            self.NextStadtButton.hide()

    def changeCityView(self, keyword):
        if keyword == "single":
            self.SingleCityView.show()
            self.ListCityView.hide()
            self.ListCityScrollArea.hide()

            #self.OrderWindow.ListCityScrollArea.hide()
        elif keyword == "list":
            self.SingleCityView.hide()
            self.ListCityView.show()
            self.ListCityScrollArea.show()


        #print(self.cruiseData[2] + "   <====== das brauch ich")
        #print(self.cityData + "   <====== das brauch ich auch")
        # Die for-Schleife muss in displayWindow() ODER changeCityView(), in __init__ ist self.cruiseData[2] noch leer
        for city in self.cityData: #self.cruiseData[2]: # ["test", "test", "test", "test", "test", "test", "test"]:  # self.cruiseData[2]
            # Stadtname
            CityName = QLabel(city)
            #self.orderWindow.ScrollLayout.addWidget(CityName)
            CityName.setStyleSheet("background-color: rgb(255, 255,255); margin-left: 2px")
            self.ListCityViewLayout.addWidget(CityName)
            #self.ListCityViewLayout.addStretch()
            #ScrollLayout.addLayout(self.ListCityViewLayout)

            #print(city)

            # # Bild erstellen
            CityImage = QLabel()
            if file_exists('data/images/Hafenstädte/' + city + '.jpg') == True:
                self.CityImagePixmap = QPixmap('data/images/Hafenstädte/' + city + '.jpg')
                CityImagePixmap = self.CityImagePixmap.scaled(
                    QtCore.QSize(300, 400),     # (old values: 330, 202  # new values 370, 242
                    #Qt.KeepAspectRatioByExpanding,
                    #Qt.IgnoreAspectRatio,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )
                CityImage.setPixmap(CityImagePixmap)
            elif file_exists('data/images/Hafenstädte/' + city + '.jpg') == False:
                self.CityImagePixmap = QPixmap('data/images/Hafenstädte/keinevorschau2.jpg')
                CityImagePixmap = self.CityImagePixmap.scaled(
                    QtCore.QSize(300, 300),  # (old values: 330, 202 with KeepAspectRatioByExpanding  / 300, 190 with IgnoreAR
                    #Qt.KeepAspectRatioByExpanding,
                    #Qt.IgnoreAspectRatio,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation,
                )
                CityImage.setPixmap(CityImagePixmap)
            self.ListCityViewLayout.addWidget(CityImage)
            #ScrollLayout.addLayout(self.ListCityViewLayout)

            #ScrollLayout.addWidget(CityImage)

            #self.MultiCityViewLayout.addSpacing()
            #self.MultiCityViewLayout.addStretch()



            # CityImage = QLabel()
            # self.orderWindow.ScrollLayout.addWidget(CityImage)
            # # Spacer nach jeder Vorschau?
            #
            # # Platz zwischen Staedten lassen
            # self.orderWindow.ScrollLayout.addStretch()
    """
    def PrevStadt(self, stadtstelle):
        # c = self.cruiseData[2]
        # cityviewlist = c.split(", ")
        # #stadtanzahl = c.count(",") + 1
        # # y = stadtanzahl + 1
        # # max = y+1

        self.currCityIndex -= 1
        print(self.currCityIndex)

        if self.currCityIndex == 0:
            self.PrevStadtButton.hide()
        else:
            self.PrevStadtButton.show()
            self.NextStadtButton.show()
        return self.currCityIndex

    def NextStadt(self, stadtstelle):
        c = self.cruiseData[2]
        # cityviewlist = c.split(", ")
        stadtcount = c.count(",") + 1
        # x = cityviewlist
        # # y = stadtanzahl
        # # max = y+1

        self.currCityIndex += 1
        print(self.currCityIndex)
        #print(stadtcount)

        if self.currCityIndex + 1 == stadtcount:
            self.NextStadtButton.hide()
        else:
            self.PrevStadtButton.show()
            self.NextStadtButton.show()
        return self.currCityIndex

    """

    # def stadtbuttons(self, stadtstelle):
    #     # if i == 0:
    #     #     self.PrevStadtButton.isEnabled() == False
    #     # elif i == max:
    #     #     self.NextStadtButton.isEnabled() == False
    #     # else:
    #     #     self.PrevStadtButton.isEnabled() == True
    #     #     self.NextStadtButton.isEnabled() == True
    #
    #     if self.PrevStadtButton.clicked():
    #         #i = i - i
    #         self.stadtstelle -= 1
    #         #return self.stadtstelle
    #     elif self.NextStadtButton.clicked():
    #         #i = i + 1
    #         self.stadtstelle += 1
    #         #return self.stadtstelle
    #
    #     c = self.cruiseData[2]
    #     # cityviewlist = c.split(", ")
    #     stadtcount = c.count(",") + 1
    #     # = cityviewlist
    #     # y = stadtanzahl
    #     # max = y+1
    #
    #     if self.stadtstelle == 0:
    #         self.PrevStadtButton.hide()
    #     else:
    #         self.PrevStadtButton.show()
    #
    #     if self.stadtstelle + 1 == stadtcount:
    #         self.NextStadtButton.hide()
    #     else:
    #         self.NextStadtButton.show()
    #
    #
    #     return self.stadtstelle




        # while i > 0:
        #     if self.PrevStadtButton.clicked():
        #         i-1
        #         #self.LaStadt.setText("Stadt: " + './data/images/Hafenstädte' + x[i] + '.jpg')
        # while i < max:
        #     if self.NextStadtButton.clicked():
        #         i+1
                  #self.LaStadt.setText("Stadt: " + './data/images/Hafenstädte' + x[i] + '.jpg')

        # self.StadtViewPixmap = QPixmap('data/images/Hafenstädte/' + cityviewlist[i] + '.jpg')
        # StadtViewPixmap = self.displayWindow.StadtViewPixmap.scaled(
        #     QtCore.QSize(350, 222),
        #     Qt.KeepAspectRatioByExpanding,
        #     Qt.SmoothTransformation
        # )
        # self.orderWindow.StadtView.setPixmap(StadtViewPixmap)
        # self.LaStadt.setText("Stadt: " + './data/images/Hafenstädte' + cityviewlist[i] + '.jpg')




# Class to show Cruisship image
class ImageCruiseShip(QWidget):

    def __init__(self, image):
        super(ImageCruiseShip, self).__init__()

        if file_exists(image):
            self.labelImage = QLabel(self)
            self.pixmap = QPixmap(image)
            img_width = self.pixmap.size().width()
            img_height = self.pixmap.size().height()
            # Scale image
            pixmap = self.pixmap.scaled(
                QtCore.QSize(256, 128),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )

            self.labelImage.setPixmap(pixmap)

            # Align Image to Center
            if (img_width / img_height) < 2:  # If Aspect Ratio < Frame Aspect Ratio: center vertical
                y = abs((img_height / (img_width / 256) - 128) / 2)  # Get Pixel Difference between scaled Image and original Image (Cut section)
                self.labelImage.move(0, int(-y))

            elif (img_width / img_height) > 2:  # If Aspect Ratio > Frame Aspect Ratio: center horizontal
                x = abs((img_width / (img_height / 128) - 256) / 2) # Get Pixel Difference between scaled Image and original Image (Cut section)
                self.labelImage.move(int(-x), 0)



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

    def resetItemChecked(self, index):
        item = self.model().item(index, self.modelColumn())
        if item.checkState() == QtCore.Qt.Checked:
            item.setCheckState(QtCore.Qt.Unchecked)


# Tabelle
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

    def getImageLabel(self, image):
        imageLabel = ImageCruiseShip(image)
        return imageLabel

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
                    item = self.getImageLabel(imagePath)
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
                # Put Item in Table
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
        # main window
        self.setObjectName("MainWindow>")
        self.setWindowTitle("Kreuzfahrt-Buchung")
        self.setGeometry(100, 50, 1400, 720)  # x, y, width, height
        self.setWindowIcon(QIcon("data\images\SchiffIcon.png"))

        # Overall Layout Creation
        ApplicationVerticalLayout = QVBoxLayout()
        ApplicationVerticalLayout.setSpacing(20)
        myQWidget.setLayout(ApplicationVerticalLayout)

        #Infotext for Filter
        self.FilterInfoLabel = QLabel()
        self.FilterInfoLabel.setText(
            "Sie können den Filter nutzen, um Ihre Auswahl einzugrenzen\n(Auswahl der Städte wird durch die ausgewählten Regionen begrenzt)\n(Anzahl der Übernachtungen werden +- 2 Tage angezeigt)")
        self.FilterInfoLabel.setStyleSheet("font-size: 12pt; background-color: rgba(255, 255, 255, 0.6);")
        self.FilterInfoLabel.setAlignment(QtCore.Qt.AlignCenter)
        ApplicationVerticalLayout.addWidget(self.FilterInfoLabel)

        # Grid Layout for fILTER
        FilterGridLayout = QGridLayout()
        FilterGridLayout.setSpacing(5)
        ApplicationVerticalLayout.addLayout(FilterGridLayout)

        # Infotext for Tabelle
        self.FilterInfoLabel = QLabel()
        self.FilterInfoLabel.setText(
            "Klicken Sie die Reise an, welche Sie auswählen wollen")
        self.FilterInfoLabel.setStyleSheet("font-size: 12pt; background-color: rgba(255, 255, 255, 0.6);")
        self.FilterInfoLabel.setAlignment(QtCore.Qt.AlignCenter)
        ApplicationVerticalLayout.addWidget(self.FilterInfoLabel)

        # Table Creation
        self.table_view = TableView(getTable(), len(getTable()), 8)
        tableLayout = QVBoxLayout()  # Tabellen Layout
        tableLayout.addWidget(self.table_view)
        tableLayout.minimumSize()
        ApplicationVerticalLayout.addLayout(tableLayout)
        # Tabellenkonfiguration
        for x in range(len(getTable())):  # Row-Höhe festlegen
            self.table_view.setRowHeight(x, 128)

        self.table_view.setColumnWidth(4, 256)  # Schiffstypen größer machen für Bilder

        # Order Button
        self.sendSelectionButton = QPushButton("Auswahl bestellen", self)
        self.sendSelectionButton.setAutoFillBackground(True)
        self.sendSelectionButton.resize(150, 70)
        self.sendSelectionButton.setStyleSheet("background-color: rgb(0, 130, 0); color: white;")
        ApplicationVerticalLayout.addWidget(self.sendSelectionButton)

        # central widget
        self.setCentralWidget(myQWidget)

        # creating widgets and their details
        # Region Auswahl
        self.RegionLabel = QLabel()
        #self.RegionLabelErgebnis = QLabel()  # Label zum Anzeigen der Auswahl
        # self.RegionLabelErgebnis.setStyleSheet("background-color: white;")
        self.RegionLabel.setText("Region")
        self.RegionLabel.setStyleSheet("font-size: 12pt;font-weight: bold; background-color: rgba(255, 255, 255, 0.6);")
        self.RegionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.RegionComboBox = CheckableComboBox()

        # Uebernachtungen Anzahl
        self.NachtLabel = QLabel()
        #self.NachtLabelErgebnis = QLabel()  # Label zum Anzeigen der Auswahl
        # self.NachtLabelErgebnis.setStyleSheet("background-color: white; border-color: black;")
        self.NachtLabel.setText("Übernachtungen")
        self.NachtLabel.setStyleSheet("font-size: 12pt;font-weight: bold; background-color: rgba(255, 255, 255, 0.6);")
        self.NachtLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.NachtSpinBox = QSpinBox()
        self.NachtSpinBox.setMinimum(7)
        self.NachtSpinBox.setMaximum(21)

        # Zu besuchende Staedte
        self.StadtLabel = QLabel()
        #self.StadtLabelErgebnis = QLabel()  # Label zum Anzeigen der Auswahl
        # self.StadtLabelErgebnis.setStyleSheet("background-color: white;")
        self.StadtLabel.setText("Städte")
        self.StadtLabel.setStyleSheet("font-size: 12pt;font-weight: bold; background-color: rgba(255, 255, 255, 0.6);")
        self.StadtLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.StadtComboBox = CheckableComboBox()
        # self.StadtComboBox.setGeometry(QtCore.QRect(310, 70, 200, 41))

        # Schiffstyp Auswahl
        self.SchiffsTypLabel = QLabel()
        #self.SchiffsTypLabelErgebnis = QLabel()  # Label zum Anzeigen der Auswahl
        # self.SchiffsTypLabelErgebnis.setStyleSheet("background-color: white;")
        self.SchiffsTypLabel.setText("Schiffstyp")
        self.SchiffsTypLabel.setStyleSheet("font-size: 12pt;font-weight: bold; background-color: rgba(255, 255, 255, 0.6);")
        self.SchiffsTypLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SchiffsTypComboBox = CheckableComboBox()

        # Such Knopf
        self.SearchButton = QPushButton()
        self.SearchButton.setText("Suchen")
        # self.SearchButton.setGeometry(730, 20, 61, 41)
        self.SearchButton.setAutoFillBackground(True)
        self.SearchButton.setStyleSheet("background-color: rgb(0, 130, 0); color: white;")

        # Reset Knopf
        self.ResetButton = QPushButton()
        self.ResetButton.setText("Filter zurücksetzen")
        self.ResetButton.setAutoFillBackground(True)
        self.ResetButton.setStyleSheet("background-color: rgb(130, 0, 0); color: white;")

        # adding Widgets to the Grid-layout   (widget, row, column, alignment)
        FilterGridLayout.addWidget(self.RegionLabel, 1, 1)
        FilterGridLayout.addWidget(self.RegionComboBox, 2, 1)
        #FilterGridLayout.addWidget(self.RegionLabelErgebnis, 3, 1)

        FilterGridLayout.addWidget(self.NachtLabel, 1, 2)
        FilterGridLayout.addWidget(self.NachtSpinBox, 2, 2)
        #FilterGridLayout.addWidget(self.NachtLabelErgebnis, 3, 2)

        FilterGridLayout.addWidget(self.StadtLabel, 1, 3)
        FilterGridLayout.addWidget(self.StadtComboBox, 2, 3)
        #FilterGridLayout.addWidget(self.StadtLabelErgebnis, 3, 3)

        FilterGridLayout.addWidget(self.SchiffsTypLabel, 1, 4)
        FilterGridLayout.addWidget(self.SchiffsTypComboBox, 2, 4)
        #FilterGridLayout.addWidget(self.SchiffsTypLabelErgebnis, 3, 4)

        FilterGridLayout.addWidget(self.SearchButton, 2, 5)
        FilterGridLayout.addWidget(self.ResetButton, 1, 5)
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
        for i in ["A", "B", "C", "D", "E", "F"]:
            self.SchiffsTypComboBox.addItem(i)

        # self.SearchComponents() # calling method
        self.show()

        # adding action to button
        # self.RegionComboBox = QComboBox(self)
        self.SearchButton.pressed.connect(self.Search)
        self.ResetButton.pressed.connect(self.Reset)
        self.sendSelectionButton.pressed.connect(self.sendData)
        # self.RegionLabelErgebnis = QLabel(self)
        # self.RegionComboBox.setGeometry(100, 100, 200, 50)



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

        if self.orderWindow.cruiseData[4] == 'nicht vorhanden':
            self.orderWindow.InnenPreis.setCheckable(False)
        if self.orderWindow.cruiseData[5] == 'nicht vorhanden':
            self.orderWindow.AussenPreis.setCheckable(False)
        if self.orderWindow.cruiseData[6] == 'nicht vorhanden':
            self.orderWindow.BalkonPreis.setCheckable(False)

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

    # Reset Filter with nothing selected and Übernachtungen = 7
    def Reset(self):

        for i in range(self.RegionComboBox.count()):
            self.RegionComboBox.resetItemChecked(i)
        self.NachtSpinBox.setValue(7)
        for i in range(self.StadtComboBox.count()):
            self.StadtComboBox.resetItemChecked(i)
        for i in range(self.SchiffsTypComboBox.count()):
            self.SchiffsTypComboBox.resetItemChecked(i)

        # Show all Table elements
        for row_count in range(self.table_view.rowCount()):
            self.table_view.showRow(row_count)


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
        #self.RegionLabelErgebnis.setText("Region: " + str(region))
        #self.NachtLabelErgebnis.setText("Uebernachtungen: " + str(naechte))
        #self.StadtLabelErgebnis.setText("Staedte: " + str(staedte))
        #self.SchiffsTypLabelErgebnis.setText("Schiffstyp: " + str(typ))


        # Reset old Filter before applying new one
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
            cityElementTable = self.table_view.item(row_count, 3).text().split(", ")    # Get List of Citys in current Table Row
            if len(FilterErgebnis[2]) != 0:
                # Check if all Citys from Filter are in CityList of Table
                check = all(item in cityElementTable for item in FilterErgebnis[2])
                if check is False:
                    self.table_view.hideRow(row_count)

                """
                for cityNum, cityElement in enumerate(FilterErgebnis[2]):
                    # Ändern, dass alle ausgewählten Städte enthalten sein MÜSSEN

                    if cityElement in self.table_view.item(row_count, 3).text():
                        break
                    elif cityElement not in self.table_view.item(row_count, 3).text():
                        self.table_view.hideRow(row_count)
                """
            # Check Schiffstyp
            if len(FilterErgebnis[3]) != 0:
                if self.table_view.item(row_count, 4).text() not in FilterErgebnis[3]:
                    self.table_view.hideRow(row_count)

        if self.table_view.rowAt(0) == -1:
            emptyTableDialog = QMessageBox(self)
            emptyTableDialog.setWindowTitle("Kein Suchergebnis gefunden")
            emptyTableDialog.setText(
                "Für Ihre Auswahl wurde kein Suchergebnis gefunden.")
            emptyTableDialog.exec()



# drivers code
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
