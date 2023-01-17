from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

from os.path import exists as file_exists   # To check, if files exists
import sys
import random
import pandas                               # Read Excel file

IMGPATH = r'data\images\Schiffstypen'  # Schiffstypen Bilder
TABLEPATH = r'data\Schiffreisen.xlsx'  # Excel Tabelle


# Read Excel file
def getTable():
    df = pandas.read_excel(TABLEPATH, header=3, usecols=lambda x: 'Unnamed' not in x, skiprows=range(25, 29))
    dfList = df.values.tolist()

    return dfList   # Returns List


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

        #self.OrderWindow = OrderWindow()
        self.editElement = None
        self.labelElement = None
        self.setWindowTitle("Persönliche Daten")
        self.setWindowIcon(QIcon("data\images\SchiffIcon.png"))
        self.buchungsData = []
        self.setFixedWidth(340)
        self.setFixedHeight(480)
        self.setStyleSheet("font-size: 12px; background-color: rgb(200, 255, 255);") #




        self.PersonalDataLayout = QGridLayout()
        self.InformationLabel = QLabel("Geben Sie Ihre Kontaktinformationen und\nBankverbindung an, um die Bestellung abzuschließen.")
        self.InformationLabel.setStyleSheet("font-size: 12px; background-color: rgb(255,255,255); padding-left: 8px; border-radius: 10px")
        self.PersonalDataLayout.addWidget(self.InformationLabel)

        # Add Personal Information Input
        self.PersonalDataLayout.addWidget(self.createDialog("Name", ["Nachname", "Vorname"]), 1, 0)
        self.PersonalDataLayout.addWidget(self.createDialog("Adresse", ["Postleitzahl", "Ort", "Straße, Hausnummer"]), 2, 0)
        self.PersonalDataLayout.addWidget(self.createDialog("Bankdaten", ["IBAN"]), 3, 0)

        # Save Button
        self.saveButton = QPushButton("Abspeichern", self)
        self.saveButton.setStyleSheet("QPushButton{background-color: rgb(208, 255, 163)}")
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
            self.editElement.setStyleSheet("background-color: rgb(255,255,255)")

            vLayout.addWidget(self.labelElement)
            vLayout.addWidget(self.editElement)

        groupBox.setLayout(vLayout)
        return groupBox

    # Save Input Data and close Window
    def saveData(self):

        isFilled = True
        self.OrderWindow = OrderWindow()
        textboxValue = []
        # Get Data from all QLineEdit Widgets in Window Layout
        for i in range(0, 4):
            groupWidget = self.PersonalDataLayout.itemAtPosition(i, 0)
            for textWidget in groupWidget.widget().children():
                if isinstance(textWidget, QLineEdit):
                    if not textWidget.text():   # Check if all QLineEdits are filled with text
                        isFilled = False
                    textboxValue.append(textWidget.text())

        # Finish Saving, when all QLines are filled
        if isFilled == True:
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

        # Else inform user
        else:
            noTextDialog = QMessageBox(self)
            noTextDialog.setWindowTitle("Bitte Ausfüllen")
            noTextDialog.setText(
                "Sie müssen alle Felder ausfüllen, um die Bestellung abzuschließen"
            )
            noTextDialog.exec()

    # Call Window to open
    def displayDialog(self):
        self.show()

# ======================================================================================================================
#
# End of DialogWindow
#
# ======================================================================================================================


# Order Window to show selected cruise with images and cabin selection
class OrderWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.personalDataDialog = PersonalDataDialog()
        self.cruiseData = []
        self.cityData = []
        self.bestellData = []
        self.currCityIndex = 0
        self.setWindowTitle('Bestellung')
        self.setWindowIcon(QIcon("data\images\SchiffIcon.png"))
        self.setGeometry(150, 150, 560, 760)
        self.setFixedWidth(760)
        self.setFixedHeight(560)
        self.setStyleSheet("""
            background-color: rgb(153, 216, 244);
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
        # Layout for Schiffstyp(Vorschau), Region, Uebernachtungen, Buchungsnummer
        self.LaInform = QLabel("Hier sehen Sie die Zusammenfassung Ihrer ausgewählten Reise.\nWählen Sie bitte noch Ihre gewünschte Kabinenart aus:")
        self.LaInform.setStyleSheet("font-size: 18px; background-color: rgb(255,255,255); padding-left: 8px; border-radius: 20px")
        BestellGridLayout.addWidget(self.LaInform, 0, 0, 1, 0)      # row, column, row-span, column-span

        # VerticalLayout = LayoutBox for Schiffstyp- & Staedtebilder Widget
        self.VerticalLayoutLO = QVBoxLayout()

        # Schiffstyp Layout = LayoutBox for Schiffstyp-Widget
        self.SchiffstypLayout = QVBoxLayout()
        self.SchiffsTypVorschau = QLabel(self)
        self.SchiffsTypVorschau.resize(330, 202)
        self.SchiffsTyp = QLabel()
        self.SchiffsTyp.setAlignment(QtCore.Qt.AlignCenter)
        self.SchiffstypLayout.addWidget(self.SchiffsTypVorschau)
        self.SchiffstypLayout.addWidget(self.SchiffsTyp)
        self.VerticalLayoutLO.addLayout(self.SchiffstypLayout)

        # Cruise information = Shows region, "Uebernachtungen" & Order number
        self.LaRegion = QLabel("Region: ")
        self.VerticalLayoutLO.addWidget(self.LaRegion)
        self.LaUebernachtungen = QLabel("Übernachtungen: ")
        self.VerticalLayoutLO.addWidget(self.LaUebernachtungen)
        self.LaBuchungsnummer = QLabel()
        self.VerticalLayoutLO.addWidget(self.LaBuchungsnummer)

        # StaedteViewChangeButton = Button to change between single Image-View or Scroll-Area-View
        # Create Menu to switch City View
        self.changeCityViewButton = QPushButton("Städte-Ansicht wechseln", self)
        self.changeCityViewButton.setFixedWidth(350)
        changeCityViewMenu = QMenu(self)
        singleAction = QAction("Einzelansicht", self)
        singleAction.triggered.connect(lambda: self.changeCityView("single"))
        listAction = QAction("Ansicht als Liste", self)
        listAction.triggered.connect(lambda: self.changeCityView("list"))
        changeCityViewMenu.addAction(singleAction)
        changeCityViewMenu.addAction(listAction)
        self.changeCityViewButton.setMenu(changeCityViewMenu)
        self.changeCityViewButton.setStyleSheet("background-color: rgb(208, 255, 163); margin-right: 10px; font-size: 11pt")
        changeCityViewMenu.setStyleSheet("background-color: rgb(208, 255, 163);")
        self.VerticalLayoutLO.addWidget(self.changeCityViewButton)
        self.changeCityViewButton.resize(self.changeCityViewButton.sizeHint())

        # Single City Image Layout = Layout Information for single Image-View
        self.SingleCityView = QWidget()                             # Pack Single-City-Preview-Layout in a Widget, to allow hiding it
        self.SingleCityViewLayout = QVBoxLayout()
        self.SingleCityView.setLayout(self.SingleCityViewLayout)
        self.StadtView = QLabel(self)                               # Label zum anzeigen des Bildes der Stadt
        self.VerticalLayoutLO.addWidget(self.SingleCityView)




        # Scroll-Area-View Widget & Layout
        self.ListCityScrollArea = QScrollArea(self)                                     # create Scroll-Area
        self.ListCityScrollArea.setWidgetResizable(True)                                # make Scroll-Area resizable
        self.ListCityScrollArea.setFixedHeight(202)
        #ListCityScrollArea.setContentsMargins(, 0, 0, 0, 0)
        self.ScrollContent = QWidget(self.ListCityScrollArea)                           # Inhalt-Widget mit Scrollarea als parent?
        self.ScrollLayout = QVBoxLayout(self.ScrollContent)                             # scroll-layout mit scroll-content als parent?
        self.ScrollContent.setLayout(self.ScrollLayout)                                 # Content layout zuweisen zu Content
        self.ListCityScrollArea.setWidget(self.ScrollContent)                           # der Scroll-Area das inhalt-widget zuweisen
        self.ListCityView = QWidget()                                                   # Widget erstellen
        self.ListCityViewLayout = QVBoxLayout(self.ListCityView)                        # Layout für widget erstellen
        self.ListCityViewLayout.setContentsMargins(0, 0, 0, 0)                          # Margin setzen damit inhalt weiter links ist
        self.ScrollLayout.addWidget(self.ListCityView)                                  # Widget in Scroll-Layout setzen
        self.ScrollContent.setStyleSheet("background-color: rgba(255, 255, 255, 0.6)")
        self.VerticalLayoutLO.addWidget(self.ListCityScrollArea)                        # ScrollArea in Layout setzen


        # self.StadtView.resize(330, 202)
        self.SingleCityViewLayout.addWidget(self.StadtView)
        #self.vStaedteViewLayout = QVBoxLayout()  # Layout fuer Stadtnamen-Label und darunter dessen Buttons
        self.LaStadt = QLabel()  # Label zum anzeigen des Namen der in "StadtView" angezeigten Stadt
        self.LaStadt.setStyleSheet("background-color: rgba(255, 255, 255, 0.6); font-size: 10pt; border-radius: 10px; padding: 2px")
        self.SingleCityViewLayout.addWidget(self.LaStadt)  # Hinzufuegen des Widgets in das QVBoxlayout
        self.hPrevNextButtonLayout = QHBoxLayout()  # Horizontales Box Layout um die Buttons nebeneinander zu haben

        # Single Image-View back & forward buttons
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


        # Layout for Cabin prices & images
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

        # "BestaetigungsLayout" = LayoutBox which contains the cabin price & confirm button
        self.vBestaetigungsLayout = QVBoxLayout()
        self.LaGesamtpreis = QLabel("Summe: ......€")
        self.LaGesamtpreis.setStyleSheet("font-size: 12pt")
        self.LaGesamtpreis.setAlignment(QtCore.Qt.AlignCenter)  # Text in die mitte setzen
        self.vBestaetigungsLayout.addWidget(self.LaGesamtpreis)
        self.ConfirmButton = QPushButton('Buchen')
        self.ConfirmButton.setStyleSheet("background-color: rgb(208, 255, 163);")
        self.ConfirmButton.clicked.connect(self.confirmOrder)
        self.vBestaetigungsLayout.addWidget(self.ConfirmButton)
        # BestellGridLayout.addWidget(self.ConfirmButton, 1, 1)
        BestellGridLayout.addLayout(self.vBestaetigungsLayout, 2, 1)
        self.setLayout(BestellGridLayout)

    # Confirm Order, open personalDataDialog
    def confirmOrder(self):
        self.personalDataDialog.displayDialog()
        self.close()

    # Open Order Window and put selected cruise data in Labels
    def displayWindow(self):


        # Reset-Section
        self.currCityIndex = 0                          # zuruecksetzen des Indexes bei aufruf des Fensters
        self.LaGesamtpreis.setText("Summe: ......€")    # zuruecksetzen des Gesamtpreises bei aufruf des Fensters


        # Reset Radiobutton selection by turning them off and on again
        self.InnenPreis.setCheckable(False)
        self.InnenPreis.setCheckable(True)
        self.AussenPreis.setCheckable(False)
        self.AussenPreis.setCheckable(True)
        self.BalkonPreis.setCheckable(False)
        self.BalkonPreis.setCheckable(True)


        # Create List of Citys out of String
        cityString = self.cruiseData[2]
        self.cityData = cityString.split(", ")

        self.updateCityLabel(0)

        self.LaRegion.setText("Region: " + self.cruiseData[0])
        self.LaRegion.setStyleSheet("background-color: rgba(255, 255, 255, 0.6); font-size: 11pt; border-radius: 10px; margin-right: 150px;")
        self.LaUebernachtungen.setText("Übernachtungen: " + self.cruiseData[1])
        self.LaUebernachtungen.setStyleSheet("background-color: rgba(255, 255, 255, 0.6); font-size: 11pt; border-radius: 10px; margin-right: 150px;")
        self.LaBuchungsnummer.setText("Buchungsnummer: " + str(random.randrange(2, 999999, 2)))
        self.LaBuchungsnummer.setStyleSheet("background-color: rgba(255, 255, 255, 0.6); font-size: 11pt; border-radius: 10px; margin-right: 150px;")
        self.SchiffsTyp.setText("Schiffstyp: " + self.cruiseData[3])
        self.SchiffsTyp.setStyleSheet("background-color: rgba(255, 255, 255, 0.6); font-size: 11pt; border-radius: 10px; margin-right: 20px; ")
        self.SchiffsTypPixmap = QPixmap('data/images/Schiffstypen/Schiffstyp ' + str(self.cruiseData[3]))

        img_width = self.SchiffsTypPixmap.size().width()
        img_height = self.SchiffsTypPixmap.size().height()

        SchiffsTypPixmap = self.SchiffsTypPixmap.scaled(
            QtCore.QSize(330, 202),     # width, height
            #Qt.KeepAspectRatioByExpanding,
            Qt.IgnoreAspectRatio,
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
        self.InnenPreis.setStyleSheet("font-size: 10pt")
        self.InnenKabinePixmap = QPixmap('data/images/Kabinentypen/Innenkabine.jpg')
        InnenKabinePixmap = self.InnenKabinePixmap.scaled(
            QtCore.QSize(330, 202),             # old value 300, 172
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        self.InnenVorschau.setPixmap(InnenKabinePixmap)
        self.AussenPreis.setText("Aussenkabine\nPreis: " + self.cruiseData[5])
        self.AussenPreis.setStyleSheet("font-size: 10pt")
        self.AussenKabinePixmap = QPixmap('data/images/Kabinentypen/Aussenkabine.jpg')
        AussenKabinePixmap = self.AussenKabinePixmap.scaled(
            QtCore.QSize(330, 202),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        self.AussenVorschau.setPixmap(AussenKabinePixmap)
        self.BalkonPreis.setText("Balkonkabine \nPreis: " + self.cruiseData[6])
        self.BalkonPreis.setStyleSheet("font-size: 10pt")
        self.BalkonKabinePixmap = QPixmap('data/images/Kabinentypen/Balkonkabine.jpg')
        BalkonKabinePixmap = self.BalkonKabinePixmap.scaled(
            QtCore.QSize(330, 202), # old values 300, 172
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )
        self.BalkonVorschau.setPixmap(BalkonKabinePixmap)

        self.changeCityView("single")
        self.show()

        # connect radiobutton with functions
        self.InnenPreis.clicked.connect(self.summecheck)
        self.AussenPreis.clicked.connect(self.summecheck)
        self.BalkonPreis.clicked.connect(self.summecheck)


        # check if a Cabin is unavailable
        if self.cruiseData[4] == 'nicht vorhanden':
            self.InnenPreis.setCheckable(False)
        else:
            self.InnenPreis.setCheckable(True)
        if self.cruiseData[5] == 'nicht vorhanden':
            self.AussenPreis.setCheckable(False)
        else:
            self.AussenPreis.setCheckable(True)
        if self.cruiseData[6] == 'nicht vorhanden':
            self.BalkonPreis.setCheckable(False)
        else:
            self.BalkonPreis.setCheckable(True)


    # function to check if sum is correct to selection
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

            # check for images
            if file_exists('data/images/Hafenstädte/' + self.cityData[self.currCityIndex] + '.jpg') == True:
                self.StadtViewPixmap = QPixmap('data/images/Hafenstädte/' + self.cityData[self.currCityIndex] + '.jpg')
                StadtViewPixmap = self.StadtViewPixmap.scaled(
                    QtCore.QSize(330, 202),     # (old values: 330, 202  # new values 370, 242
                    #Qt.KeepAspectRatioByExpanding,
                    Qt.IgnoreAspectRatio,
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
        # if "single" open Single-Image-View
        if keyword == "single":
            self.SingleCityView.show()
            self.ListCityView.hide()
            self.ListCityScrollArea.hide()

            # empty ListCityViewLayout in the ScrollArea
            for city in reversed(range(self.ListCityViewLayout.count())):
                self.ListCityViewLayout.itemAt(city).widget().setParent(None)


            #self.OrderWindow.ListCityScrollArea.hide()
        # if "list" open Scrollarea-Image-View
        elif keyword == "list":
            self.SingleCityView.hide()
            self.ListCityView.show()
            self.ListCityScrollArea.show()


            for city in self.cityData:
                # Stadtname
                CityName = QLabel(city)
                CityName.setStyleSheet("background-color: rgba(255, 255, 255, 0.6); font-size: 10pt; border-radius: 10px; padding: 2px; margin-left: 2px; margin-right: 12px")
                self.ListCityViewLayout.addWidget(CityName)

                # create Image
                CityImage = QLabel()
                if file_exists('data/images/Hafenstädte/' + city + '.jpg') == True:
                    self.CityImagePixmap = QPixmap('data/images/Hafenstädte/' + city + '.jpg')
                    CityImagePixmap = self.CityImagePixmap.scaled(
                        QtCore.QSize(300, 150),     # (old values: 330, 202 with KeepAspectRatioByExpanding  / 300, 190 with IgnoreAR / 300 400 with KeepAspectRatio
                        #Qt.KeepAspectRatioByExpanding,
                        Qt.IgnoreAspectRatio,
                        #Qt.KeepAspectRatio,
                        Qt.SmoothTransformation,
                    )
                    CityImage.setPixmap(CityImagePixmap)
                elif file_exists('data/images/Hafenstädte/' + city + '.jpg') == False:
                    self.CityImagePixmap = QPixmap('data/images/Hafenstädte/keinevorschau2.jpg')
                    CityImagePixmap = self.CityImagePixmap.scaled(
                        QtCore.QSize(300, 180),  # (old values: 330, 202 with KeepAspectRatioByExpanding  / 300, 190 with IgnoreAR / 300 400 with KeepAspectRatio
                        #Qt.KeepAspectRatioByExpanding,
                        #Qt.IgnoreAspectRatio,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation,
                    )
                    CityImage.setPixmap(CityImagePixmap)
                self.ListCityViewLayout.addWidget(CityImage)
                CitySpacer = QLabel(" \n \n ")
                self.ListCityViewLayout.addWidget(CitySpacer)
                self.ListCityScrollArea.setStyleSheet("margin-right: 6px")
                self.ListCityScrollArea.setStyleSheet("margin-right: 10px; background-color: rgba(255,255,255,0.6);")

# ===========================================================================================================================
#
# End of orderWindow
#
# ===========================================================================================================================

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
        self._changed = False  # makes that only the combobox can be clicked, when it´s opened

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
            "font-size: 12pt; font-weight: bold; background-color: rgba(255, 255, 255, 0.6); selection-background-color: rgba(156,222,"
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



        # Reading the List from Excel sheet
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
            "Sie können den Filter nutzen, um Ihre Auswahl einzugrenzen. \n Die Auswahl der Städte wird durch die ausgewählten Regionen begrenzt und die Anzahl der Übernachtungen werden mit  +/- 2 Tagen angezeigt.")
        self.FilterInfoLabel.setStyleSheet("font-size: 12pt; background-color: rgba(255, 255, 255, 0.6);")
        self.FilterInfoLabel.setAlignment(QtCore.Qt.AlignCenter)
        ApplicationVerticalLayout.addWidget(self.FilterInfoLabel)

        # Grid Layout for Filter
        FilterGridLayout = QGridLayout()
        FilterGridLayout.setSpacing(5)
        ApplicationVerticalLayout.addLayout(FilterGridLayout)

        # Infotext for Tabelle
        self.FilterInfoLabel = QLabel()
        self.FilterInfoLabel.setText(
            "Klicken Sie die Reise an, welche Sie auswählen wollen.")
        self.FilterInfoLabel.setStyleSheet("font-size: 14pt; background-color: rgba(255, 255, 255, 0.6); margin-left: 400px; margin-right: 400px")
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
        self.sendSelectionButton.setStyleSheet("background-color: rgb(0, 130, 0); color: white; font-size: 14pt")
        ApplicationVerticalLayout.addWidget(self.sendSelectionButton)

        # central widget
        self.setCentralWidget(myQWidget)

        # creating widgets and their details
        # Region selection
        self.RegionLabel = QLabel()
        #self.RegionLabelErgebnis = QLabel()  # Label zum Anzeigen der Auswahl
        # self.RegionLabelErgebnis.setStyleSheet("background-color: white;")
        self.RegionLabel.setText("Region")
        self.RegionLabel.setStyleSheet("font-size: 12pt;font-weight: bold; background-color: rgba(255, 255, 255, 0.6);")
        self.RegionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.RegionComboBox = CheckableComboBox()

        # Uebernachtungen selection
        self.NachtLabel = QLabel()
        #self.NachtLabelErgebnis = QLabel()  # Label zum Anzeigen der Auswahl
        # self.NachtLabelErgebnis.setStyleSheet("background-color: white; border-color: black;")
        self.NachtLabel.setText("Übernachtungen\n(7-21 Tage)")
        self.NachtLabel.setStyleSheet("font-size: 12pt;font-weight: bold; background-color: rgba(255, 255, 255, 0.6);")
        self.NachtLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.NachtSpinBox = QSpinBox()
        self.NachtSpinBox.setMinimum(7)
        self.NachtSpinBox.setMaximum(21)

        # Cities
        self.StadtLabel = QLabel()
        self.StadtLabel.setText("Städte")
        self.StadtLabel.setStyleSheet("font-size: 12pt;font-weight: bold; background-color: rgba(255, 255, 255, 0.6);")
        self.StadtLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.StadtComboBox = CheckableComboBox()
        # self.StadtComboBox.setGeometry(QtCore.QRect(310, 70, 200, 41))

        # Schiffstype
        self.SchiffsTypLabel = QLabel()
        self.SchiffsTypLabel.setText("Schiffstyp")
        self.SchiffsTypLabel.setStyleSheet("font-size: 12pt;font-weight: bold; background-color: rgba(255, 255, 255, 0.6);")
        self.SchiffsTypLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SchiffsTypComboBox = CheckableComboBox()

        # Search Button
        self.SearchButton = QPushButton()
        self.SearchButton.setText("Suchen")
        self.SearchButton.setAutoFillBackground(True)
        self.SearchButton.setStyleSheet("background-color: rgb(0, 130, 0); color: white; font-size: 11pt")

        # Reset Button
        self.ResetButton = QPushButton()
        self.ResetButton.setText("Filter zurücksetzen")
        self.ResetButton.setAutoFillBackground(True)
        self.ResetButton.setStyleSheet("background-color: rgb(130, 0, 0); color: white; font-size: 11pt")

        # adding Widgets to the Grid-layout   (widget, row, column, alignment)
        FilterGridLayout.addWidget(self.RegionLabel, 1, 1)
        FilterGridLayout.addWidget(self.RegionComboBox, 2, 1)

        FilterGridLayout.addWidget(self.NachtLabel, 1, 2)
        FilterGridLayout.addWidget(self.NachtSpinBox, 2, 2)

        FilterGridLayout.addWidget(self.StadtLabel, 1, 3)
        FilterGridLayout.addWidget(self.StadtComboBox, 2, 3)

        FilterGridLayout.addWidget(self.SchiffsTypLabel, 1, 4)
        FilterGridLayout.addWidget(self.SchiffsTypComboBox, 2, 4)

        FilterGridLayout.addWidget(self.SearchButton, 2, 5)
        FilterGridLayout.addWidget(self.ResetButton, 1, 5)

        # add items to Region CB
        self.RegionComboBox.addItem("Ostsee")
        self.RegionComboBox.addItem("Nordsee")
        self.RegionComboBox.addItem("Mittelmeer")
        self.RegionComboBox.activated.connect(self.updateCityFilter)


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

        # add items to Schiffstyp
        for j, i in enumerate(["A", "B", "C", "D", "E", "F"]):
            self.SchiffsTypComboBox.addItem(i)

            if file_exists('./data/images/Schiffstypen/Schiffstyp ' + i + '.jpg'):
                self.SchiffsTypComboBox.setItemData(j,
                                               '<img src="./data/images/Schiffstypen/Schiffstyp ' + i + '.jpg" width="500" '
                                                                                               'height="350" />',
                                               QtCore.Qt.ToolTipRole)
            else:
                self.SchiffsTypComboBox.setItemData(j, "Kein Vorschaubild vorhanden", QtCore.Qt.ToolTipRole)

        self.show()

        # adding action to button
        self.SearchButton.pressed.connect(self.Search)
        self.ResetButton.pressed.connect(self.Reset)
        self.sendSelectionButton.pressed.connect(self.sendData)


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
            data.append(self.table_view.item(currRow, x).text())

        # Transfer the Data of choosen cruise
        self.orderWindow.cruiseData = data

        # Open new Window => orderWindow
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
