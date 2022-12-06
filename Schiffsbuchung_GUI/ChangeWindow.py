from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import*

class Ui_Form(object):
    def openwindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Page2()
        self.ui.setupUi(self.window)
        Form.hide()
        self.window.show()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(734, 428)
        self.label_username = QtWidgets.QLabel(Form)
        self.label_username.setGeometry(QtCore.QRect(160, 130, 120, 30))
        self.label_username.setObjectName("label_username")
        self.label_password = QtWidgets.QLabel(Form)
        self.label_password.setGeometry(QtCore.QRect(160, 190, 110, 20))
        self.label_password.setObjectName("label_password")
        self.txt_input_username = QtWidgets.QLineEdit(Form)
        self.txt_input_username.setGeometry(QtCore.QRect(380, 140, 200, 20))
        self.txt_input_username.setObjectName("txt_input_username")
        self.txt_input_password = QtWidgets.QLineEdit(Form)
        self.txt_input_password.setGeometry((QtCore.QRect(380, 190, 200, 20)))
        self.txt_input_password.setObjectName("txt_input_password")
        self.btn_submit = QtWidgets.QTextEdit(Form)
        self.btn_submit.setGeometry(QtCore.QRect(380, 190, 200, 20))
        self.btn_submit.setObjectName("btn_submit")
        self.text_title = QtWidgets.QTextEdit(Form)
        self.text_title.setGeometry(QtCore.QRect(60, 10, 630, 50))
        self.text_title.setObjectName("text_title")
        self.radioButton = QtWidgets.QRadioButton(Form)
        self.radioButton.setGeometry(QtCore.QRect(390, 290, 190, 20))
        self.radioButton.setObjectName("radioButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Login Page"))
        self.label_username.setText(_translate("Form", "Enter User Name"))
        self.label_password.setText(_translate("Form", "Enter Password"))



