from PyQt5 import QtCore, QtGui, QtWidgets
import sys
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *



class MyDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)

        self.textBrowser = QtGui.QTextBrowser(self)
        self.textBrowser.append("This is a QTextBrowser!")

        self.verticalLayout = QtGui.QVBoxLayout(self)
        self.verticalLayout.addWidget(self.textBrowser)
        self.verticalLayout.addWidget(self.buttonBox)


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):

        self.pushButtonWindow = QtGui.QPushButton(self)
        self.pushButtonWindow.setText("Click Me!")
        self.pushButtonWindow.clicked.connect(self.on_pushButton_clicked)

        self.layout = QtGui.QHBoxLayout(self)
        self.layout.addWidget(self.pushButtonWindow)

        self.dialogTextBrowser = MyDialog(self)

        self.show()
    @QtCore.pyqtSlot()
    def on_pushButton_clicked(self):
        self.dialogTextBrowser.exec_()






app = QApplication(sys.argv)
w = MyWindow()           #Fenster aufbauen (!= Fenster anzeigen)
sys.exit(app.exec_())   #Python Programm stoppt wenn Fenster geschlossen wird










#
# from PyQt5 import QtGui, QtCore
# import sys
# import design1, design2
#
# class Second(QtGui.QMainWindow, design2.Ui_MainWindow):
#     def __init__(self, parent=None):
#         super(Second, self).__init__(parent)
#         self.setupUi(self)
#
# class First(QtGui.QMainWindow, design1.Ui_MainWindow):
#     def __init__(self, parent=None):
#         super(First, self).__init__(parent)
#         self.setupUi(self)
#
#         self.pushButton.clicked.connect(self.on_pushButton_clicked)
#         self.dialog = Second(self)
#
#     def on_pushButton_clicked(self):
#         self.dialog.exec_()
#
# def main():
#     app = QtGui.QApplication(sys.argv)
#     main = First()
#     main.show()
#     sys.exit(app.exec_())
#
# if __name__ == '__main__':
#     main()