
from PyQt5 import QtCore
from PyQt5 import QtGui
#from PyQt5.QtWidgets import QApplication, QComboBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox, QLabel
from PyQt5.QtWidgets import *
#from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QPushButton, QSpinBox
from PyQt5.QtGui import QStandardItemModel, QIcon
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import *
import sys


# creating checkable combo box class which will close after a selection
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


class SearchWindow(QMainWindow):
    def __init__(self):
        super(SearchWindow, self).__init__()

        self.setGeometry(400, 200, 800, 600)
        # self.StadtLabelErgebnis = QLabel()          # Label zum Anzeigen der Auswahl
        # self.SchiffsTypLabelErgebnis.setStyleSheet("background-color: cyan;")



class Window(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.setWindowTitle("Kreuzfahrt-Buchung")
        self.setGeometry(400, 150, 1000, 1000)
        self.UiComponents()
        self.show()

    def UiComponents(self):
        # Stylesheet
        self.setStyleSheet("QMainWindow{background-image: url(Bilder/Cruise Background 3.jpg) 0 0 0 0 stretch stretch;}")

        # creating a widget object
        myQWidget = QWidget()

        # Layout
        myVLayout = QVBoxLayout()           # Vertikales BoxLayout
        #myHLayout = QHBoxLayout()           # Horizontales BoxLayout
        myGridLayout = QGridLayout()        # Grid Layout
        myQWidget.setLayout(myVLayout)      # Horizontales Layout als Basis setzen
        #myHLayout.addLayout(myVLayout)      # Vertikales Layout in das horizontale einfügen
        myVLayout.addLayout(myGridLayout)   # Grid Layout in Vertikales Layout einfügen


        # central widget
        self.setCentralWidget(myQWidget)

        # creating widgets and their details
    # main window
        self.setObjectName("MainWindow>")
        #self.setWindowTitle("Kreuzfahrt-Buchung")
        #self.setGeometry(400, 150, 1000, 5000)
        self.setWindowIcon(QIcon("Schifficon.png"))
        # Region Auswahl
        self.RegionLabel = QLabel()
        self.RegionLabelErgebnis = QLabel()         # Label zum Anzeigen der Auswahl
        self.RegionLabelErgebnis.setStyleSheet("background-color: cyan;")
        self.RegionLabel.setText("Region")
        self.RegionLabel.setStyleSheet("background-color: white;")
        self.RegionComboBox = QComboBox()
        # Uebernachtungen Anzahl
        self.NachtLabel = QLabel()
        self.NachtLabelErgebnis = QLabel()          # Label zum Anzeigen der Auswahl
        self.NachtLabelErgebnis.setStyleSheet("background-color: cyan; border-color: black;")
        self.NachtLabel.setText("Uebernachtungen")
        self.NachtLabel.setStyleSheet("background-color: white; border-color: black;")
        self.NachtSpinBox = QSpinBox()
        self.NachtSpinBox.setMinimum(7)
        self.NachtSpinBox.setMaximum(21)
        # Schiffstyp Auswahl
        self.SchiffsTypLabel = QLabel()
        self.SchiffsTypLabelErgebnis = QLabel()     # Label zum Anzeigen der Auswahl
        self.SchiffsTypLabelErgebnis.setStyleSheet("background-color: cyan;")
        self.SchiffsTypLabel.setText("Schiffstyp")
        self.SchiffsTypLabel.setStyleSheet("background-color: white;")
        self.CBSchiffsTyp = QComboBox()
        # Zu besuchende Staedte
        self.StadtLabel = QLabel()
        self.StadtLabelErgebnis = QLabel()          # Label zum Anzeigen der Auswahl
        self.StadtLabelErgebnis.setStyleSheet("background-color: cyan;")
        self.StadtLabel.setText("Staedte")
        self.StadtLabel.setStyleSheet("background-color: white;")
        self.StadtComboBox = CheckableComboBox()
            #self.StadtComboBox.setGeometry(QtCore.QRect(310, 70, 200, 41))
        # Such Knopf
        self.SearchButton = QPushButton()
        self.SearchButton.setText("Search")
        #self.SearchButton.setGeometry(730, 20, 61, 41)
        self.SearchButton.setAutoFillBackground(True)
        self.SearchButton.setStyleSheet("background-color: rgb(0, 130, 0); color: white;")

        # adding Widgets to the Grid-layout   (widget, row, column, alignment)
        myGridLayout.addWidget(self.RegionLabel, 1, 1)
        myGridLayout.addWidget(self.RegionComboBox, 2, 1)
        myGridLayout.addWidget(self.RegionLabelErgebnis, 3, 1)

        myGridLayout.addWidget(self.NachtLabel, 1, 2)
        myGridLayout.addWidget(self.NachtSpinBox, 2, 2)
        myGridLayout.addWidget(self.NachtLabelErgebnis, 3, 2)

        myGridLayout.addWidget(self.StadtLabel, 1, 3)
        myGridLayout.addWidget(self.StadtComboBox, 2, 3)
        myGridLayout.addWidget(self.StadtLabelErgebnis, 3, 3)

        myGridLayout.addWidget(self.SchiffsTypLabel, 1, 4)
        myGridLayout.addWidget(self.CBSchiffsTyp, 2, 4)
        myGridLayout.addWidget(self.SchiffsTypLabelErgebnis, 3, 4)

        myGridLayout.addWidget(self.SearchButton, 2, 5)
        #myLayout.addStretch()
        myVLayout.addStretch()

        # add items to Schiffstyp
        self.CBSchiffsTyp.addItem("A")
        self.CBSchiffsTyp.addItem("B")
        self.CBSchiffsTyp.addItem("C")
        self.CBSchiffsTyp.addItem("D")
        self.CBSchiffsTyp.addItem("E")
        self.CBSchiffsTyp.addItem("F")

        # traversing items
        #for i in range(1):         # setzt leere checkboxen vor die items (Fehler: for i in range(i) ist die anzahl
                                    # wie viele items eine box bekommen aber auch wie oft die items ge-added werden
        # add items to StadtComboBox
        self.StadtComboBox.addItem("Aberdeen", "Nordsee")
        self.StadtComboBox.addItem("Algier")
        self.StadtComboBox.addItem("Amsterdam")
        self.StadtComboBox.addItem("Athen")
        self.StadtComboBox.addItem("Barcelona")
        self.StadtComboBox.addItem("Bari")
        self.StadtComboBox.addItem("Bergen")
        self.StadtComboBox.addItem("Cagliari")
        self.StadtComboBox.addItem("Catania")
        self.StadtComboBox.addItem("Danzig")
        self.StadtComboBox.addItem("Den Haag")
        self.StadtComboBox.addItem("Edinburg")
        self.StadtComboBox.addItem("Genua")
        self.StadtComboBox.addItem("Gibraltar")
        self.StadtComboBox.addItem("Göteborg")
        self.StadtComboBox.addItem("Haugesund")
        self.StadtComboBox.addItem("Helsinki")
        self.StadtComboBox.addItem("Kaliningrad")
        self.StadtComboBox.addItem("Kleipeda")
        self.StadtComboBox.addItem("Kopenhagen")
        self.StadtComboBox.addItem("Kristiansand")
        self.StadtComboBox.addItem("Malaga")
        self.StadtComboBox.addItem("Marseille")
        self.StadtComboBox.addItem("Neapel")
        self.StadtComboBox.addItem("Palermo")
        self.StadtComboBox.addItem("Riga")
        self.StadtComboBox.addItem("Reykjavik")
        self.StadtComboBox.addItem("Sankt Petersburg")
        self.StadtComboBox.addItem("Split")
        self.StadtComboBox.addItem("Stockholm")
        self.StadtComboBox.addItem("Stralsund")
        self.StadtComboBox.addItem("Tallin")
        self.StadtComboBox.addItem("Tanger")
        self.StadtComboBox.addItem("Torshavn")
        self.StadtComboBox.addItem("Tromsö")
        self.StadtComboBox.addItem("Trondheim")
        self.StadtComboBox.addItem("Tunis")
        self.StadtComboBox.addItem("Valencia")
        self.StadtComboBox.addItem("Valetta")
        self.StadtComboBox.addItem("Venedig")
        self.StadtComboBox.addItem("Visby")
        self.StadtComboBox.addItem("Ystad")

            #item = self.StadtComboBox.model().item(i, 0)

            # setting item unchecked
            #item.setCheckState(Qt.Unchecked)


        # add items to Region CB
        self.RegionComboBox.addItem("Ostsee")
        self.RegionComboBox.addItem("Nordsee")
        self.RegionComboBox.addItem("Mittelmeer")


        #self.SearchComponents() # calling method
        self.show()

        # adding action to button
        self.SearchButton.pressed.connect(self.Search)


    # define button action
    def Search(self):
        region = self.RegionComboBox.currentText()
        naechte = self.NachtSpinBox.value()
        staedte = self.StadtComboBox.currentText()
        typ = self.CBSchiffsTyp.currentText()

        # showing content on the screen though label
        self.RegionLabelErgebnis.setText("Region: " + str(region))
        self.NachtLabelErgebnis.setText("Uebernachtungen: " + str(naechte))
        self.StadtLabelErgebnis.setText("Staedte: " + str(staedte))
        self.SchiffsTypLabelErgebnis.setText("Schiffstyp: " + str(typ))

        #Neues Fenster
        # Fenster zuweisen
        self.dialog = SearchWindow()
        # Neues Fenster bei anklicken anzeigen
        self.dialog.show()



# drivers code
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    window.resize(802, 606)
    sys.exit(app.exec_())