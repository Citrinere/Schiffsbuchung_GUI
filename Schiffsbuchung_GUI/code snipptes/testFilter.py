import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableView, QMainWindow, QVBoxLayout, QLineEdit, QComboBox
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QAbstractTableModel


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QTableView()

        data = [
            [4, 9, 2],
            [1, "hello", 0],
            [3, 5, 0],
            [3, 3, "what"],
            ["this", 8, 9],
            ["Ostsee", 12, "Riga"],
            ["Nordsee", 10, "Rekjavik"],
            ["Mittelmeer", 8, "Palma"],
        ]

        self.model = TableModel(data)
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setFilterKeyColumn(-1) # Search all columns.
        self.proxy_model.setSourceModel(self.model)

        self.proxy_model.sort(0, Qt.AscendingOrder)

        self.table.setModel(self.proxy_model)

        self.dropdown = QComboBox()
        self.dropdown.addItems(["Ostsee", "Nordsee", "Mittelmeer"])

        # Sends the current index (position) of the selected item.
        #self.dropdown.currentIndexChanged.connect( self.index_changed )

        # There is an alternate signal to send the text.
        self.dropdown.textChanged.connect( self.proxy_model.setFilterFixedString )

        # You can choose the type of search by connecting to a different slot here.
        # see https://doc.qt.io/qt-5/qsortfilterproxymodel.html#public-slots
        #self.searchbar.textChanged.connect(self.proxy_model.setFilterFixedString)

        layout = QVBoxLayout()

        layout.addWidget(self.dropdown)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()