# Form implementation generated from reading ui file 'layout/placenie.ui'
#
# Created by: PyQt6 UI code generator 6.5.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(320, 240)
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 321, 241))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignHCenter | QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title)
        self.firma = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.firma.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.firma.setObjectName("firma")
        self.verticalLayout.addWidget(self.firma)
        self.nr_fv = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.nr_fv.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.nr_fv.setObjectName("nr_fv")
        self.verticalLayout.addWidget(self.nr_fv)
        self.numer_konta = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.numer_konta.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.numer_konta.setObjectName("numer_konta")
        self.verticalLayout.addWidget(self.numer_konta)
        self.kwota_brutto = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.kwota_brutto.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.kwota_brutto.setObjectName("kwota_brutto")
        self.verticalLayout.addWidget(self.kwota_brutto)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.zaplacono = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.zaplacono.setObjectName("zaplacono")
        self.horizontalLayout_2.addWidget(self.zaplacono)
        self.open_file = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.open_file.setObjectName("open_file")
        self.horizontalLayout_2.addWidget(self.open_file)
        self.anuluj = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.anuluj.setObjectName("anuluj")
        self.horizontalLayout_2.addWidget(self.anuluj)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Płacenie FV"))
        self.title.setText(_translate("Dialog", "Płacenie FV"))
        self.firma.setText(_translate("Dialog", "Firma - "))
        self.nr_fv.setText(_translate("Dialog", "Numer FV - "))
        self.numer_konta.setText(_translate("Dialog", "Numer konta"))
        self.kwota_brutto.setText(_translate("Dialog", "Kwota Brutto - "))
        self.zaplacono.setText(_translate("Dialog", "Zapłacono"))
        self.open_file.setText(_translate("Dialog", "Otwórz plik"))
        self.anuluj.setText(_translate("Dialog", "Anuluj"))
