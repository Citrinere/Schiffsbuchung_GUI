import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

from CWT import Ui_MainWindow

class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        self.ui.stackedWidget.setCurrentWidget(self.ui.Home)

        self.ui.blue_btn.clicked.connect(self.showBlue)
        self.ui.red_btn.clicked.connect(self.showRed)
        self.ui.yell_btn.clicked.connect(self.showYellow)
        self.ui.home_btn.clicked.connect(self.showHome)



    def show(self):
        self.main_win.show()

    def showBlue(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.blue)

    def showRed(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.red)

    def showYellow(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.yellow)

    def showHome(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Home)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())


