from PyQt5.QtWidgets import QApplication, QComboBox, QMainWindow
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import Qt
import sys


# creating checkable combo box class
class CheckableComboBox(QComboBox):
    def __init__(self):
        super(CheckableComboBox, self).__init__()
        self.view().pressed.connect(self.handle_item_pressed)
        self.setModel(QStandardItemModel(self))

    # when any item get pressed
    def handle_item_pressed(self, index):

        # getting which item is pressed
        item = self.model().itemFromIndex(index)

        # make it check if unchecked and vice-versa
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)

        # calling method
        self.check_items()

    # method called by check_items
    def item_checked(self, index):

        # getting item at index
        item = self.model().item(index, 0)

        # return true if checked else false
        return item.checkState() == Qt.Checked

    # calling method
    def check_items(self):
        # blank list
        checkedItems = []

        # traversing the items
        for i in range(self.count()):

            # if item is checked add it to the list
            if self.item_checked(i):
                checkedItems.append(i)

        # call this method
        self.update_labels(checkedItems)

    # method to update the label
    def update_labels(self, item_list):

        n = ''
        count = 0

        # traversing the list
        for i in item_list:

            # if count value is 0 don't add comma
            if count == 0:
                n += ' % s' % i
            # else value is greater then 0
            # add comma
            else:
                n += ', % s' % i

            # increment count
            count += 1

        # loop
        for i in range(self.count()):

            # getting label
            text_label = self.model().item(i, 0).text()

            # default state
            if text_label.find('-') >= 0:
                text_label = text_label.split('-')[0]

            # shows the selected items
            item_new_text_label = text_label + ' - selected index: ' + n

            # setting text to combo box
            self.setItemText(i, item_new_text_label)

    # flush
    sys.stdout.flush()


class Window(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        # creating a widget object
        myQWidget = QWidget()

        # vertical box layout
        myBoxLayout = QVBoxLayout()
        myQWidget.setLayout(myBoxLayout)

        # central widget
        self.setCentralWidget(myQWidget)

        # creating checkable combo box
        self.StadtComboBox = CheckableComboBox()

        # traversing items
        for i in range(15):
            # adding item
            self.StadtComboBox.addItem("Combobox Item " + str(i))
            # self.StadtComboBox.addItem("Stadt")
            # self.StadtComboBox.addItem("Aberdeen", "Nordsee")
            # self.StadtComboBox.addItem("Algier")
            # self.StadtComboBox.addItem("Amsterdam")
            # self.StadtComboBox.addItem("Athen")
            # self.StadtComboBox.addItem("Barcelona")
            # self.StadtComboBox.addItem("Bari")
            # self.StadtComboBox.addItem("Bergen")
            # self.StadtComboBox.addItem("Cagliari")
            # self.StadtComboBox.addItem("Catania")
            # self.StadtComboBox.addItem("Danzig")
            # self.StadtComboBox.addItem("Den Haag")
            # self.StadtComboBox.addItem("Edinburg")
            # self.StadtComboBox.addItem("Genua")
            # self.StadtComboBox.addItem("Gibraltar")
            # self.StadtComboBox.addItem("Göteborg")
            # self.StadtComboBox.addItem("Haugesund")
            # self.StadtComboBox.addItem("Helsinki")
            # self.StadtComboBox.addItem("Kaliningrad")
            # self.StadtComboBox.addItem("Kleipeda")
            # self.StadtComboBox.addItem("Kopenhagen")
            # self.StadtComboBox.addItem("Kristiansand")
            # self.StadtComboBox.addItem("Malaga")
            # self.StadtComboBox.addItem("Marseille")
            # self.StadtComboBox.addItem("Neapel")
            # self.StadtComboBox.addItem("Palermo")
            # self.StadtComboBox.addItem("Riga")
            # self.StadtComboBox.addItem("Reykjavik")
            # self.StadtComboBox.addItem("Sankt Petersburg")
            # self.StadtComboBox.addItem("Split")
            # self.StadtComboBox.addItem("Stockholm")
            # self.StadtComboBox.addItem("Stralsund")
            # self.StadtComboBox.addItem("Tallin")
            # self.StadtComboBox.addItem("Tanger")
            # self.StadtComboBox.addItem("Torshavn")
            # self.StadtComboBox.addItem("Tromsö")
            # self.StadtComboBox.addItem("Trondheim")
            # self.StadtComboBox.addItem("Tunis")
            # self.StadtComboBox.addItem("Valencia")
            # self.StadtComboBox.addItem("Valetta")
            # self.StadtComboBox.addItem("Venedig")
            # self.StadtComboBox.addItem("Visby")
            # self.StadtComboBox.addItem("Ystad")
            item = self.StadtComboBox.model().item(i, 0)

            # setting item unchecked
            item.setCheckState(Qt.Unchecked)

        # adding combo box to the layout
        myBoxLayout.addWidget(self.StadtComboBox)


# drivers code
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    window.resize(480, 320)
    sys.exit(app.exec_())