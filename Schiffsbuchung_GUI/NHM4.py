# Form implementation generated from reading ui file 'NeuesHauptmenu2.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(802, 595)
        MainWindow.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(
        "background-image: url(Bilder/Cruise Background 3.jpg) 0 0 0 0 stretch stretch;\n"
        "      \n"
        "    /*\n"
        "    background-position: top;\n"
        "    background-repeat: repeat-xy;\n"
        "    background-size: cover;\n"
        "    background-attachment: fixed;\n"
        "    */")
        MainWindow.setIconSize(QtCore.QSize(24, 24))
        MainWindow.setAnimated(True)
        MainWindow.setDocumentMode(False)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.CBOrt = QtWidgets.QComboBox(self.centralwidget)
        self.CBOrt.setGeometry(QtCore.QRect(250, 20, 231, 41))
        self.CBOrt.setObjectName("CBOrt")
        self.CBOrt.addItem("")
        self.CBOrt.addItem("")
        self.CBOrt.addItem("")
        self.CBOrt.addItem("")
        self.CBPersonen = QtWidgets.QComboBox(self.centralwidget)
        self.CBPersonen.setGeometry(QtCore.QRect(490, 20, 231, 41))
        self.CBPersonen.setObjectName("CBPersonen")
        self.CBPersonen.addItem("")
        self.CBPersonen.addItem("")
        self.CBPersonen.addItem("")
        self.CBPersonen.addItem("")
        self.CBPersonen.addItem("")
        self.CBPersonen.addItem("")
        self.CBPersonen.addItem("")
        self.SearchButton = QtWidgets.QPushButton(self.centralwidget)
        self.SearchButton.setGeometry(QtCore.QRect(730, 20, 51, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.SearchButton.setFont(font)
        self.SearchButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.SearchButton.setMouseTracking(False)
        self.SearchButton.setStyleSheet("color: yellow;")
        self.SearchButton.setAutoRepeat(False)
        self.SearchButton.setObjectName("SearchButton")
        self.dateEdit_2 = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit_2.setGeometry(QtCore.QRect(10, 20, 231, 41))
        self.dateEdit_2.setObjectName("dateEdit_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 802, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.CBOrt.setToolTip(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.CBOrt.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.CBOrt.setItemText(0, _translate("MainWindow", "Bitte Auswählen", "True"))
        self.CBOrt.setItemText(1, _translate("MainWindow", "Ostsee"))
        self.CBOrt.setItemText(2, _translate("MainWindow", "Nordsee"))
        self.CBOrt.setItemText(3, _translate("MainWindow", "Mittelmeer"))
        self.CBPersonen.setItemText(0, _translate("MainWindow", "2 Personen"))
        self.CBPersonen.setItemText(1, _translate("MainWindow", "3 Personen"))
        self.CBPersonen.setItemText(2, _translate("MainWindow", "4 Personen"))
        self.CBPersonen.setItemText(3, _translate("MainWindow", "5 Personen"))
        self.CBPersonen.setItemText(4, _translate("MainWindow", "6 Personen"))
        self.CBPersonen.setItemText(5, _translate("MainWindow", "7 Personen"))
        self.CBPersonen.setItemText(6, _translate("MainWindow", "8 Personen"))
        self.SearchButton.setText(_translate("MainWindow", "Search"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
