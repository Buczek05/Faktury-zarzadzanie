# Form implementation generated from reading ui file 'layout/dodawanie_faktury.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 624)
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 601, 621))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, -1, 10, -1)
        self.gridLayout.setObjectName("gridLayout")
        self.label_termin_wystawienia = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_termin_wystawienia.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_termin_wystawienia.setObjectName("label_termin_wystawienia")
        self.gridLayout.addWidget(self.label_termin_wystawienia, 0, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(parent=self.verticalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 7, 1, 1, 1)
        self.label_sprzedawca = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_sprzedawca.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_sprzedawca.setObjectName("label_sprzedawca")
        self.gridLayout.addWidget(self.label_sprzedawca, 3, 0, 1, 1)
        self.label_numer_fv = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_numer_fv.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_numer_fv.setObjectName("label_numer_fv")
        self.gridLayout.addWidget(self.label_numer_fv, 2, 0, 1, 1)
        self.label_plik_fv = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_plik_fv.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_plik_fv.setObjectName("label_plik_fv")
        self.gridLayout.addWidget(self.label_plik_fv, 9, 0, 1, 1)
        self.dateEdit_data_wystawienia = QtWidgets.QDateEdit(parent=self.verticalLayoutWidget)
        self.dateEdit_data_wystawienia.setObjectName("dateEdit_data_wystawienia")
        self.gridLayout.addWidget(self.dateEdit_data_wystawienia, 0, 1, 1, 1)
        self.label_kwota_netto = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_kwota_netto.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_kwota_netto.setObjectName("label_kwota_netto")
        self.gridLayout.addWidget(self.label_kwota_netto, 4, 0, 1, 1)
        self.label_status = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_status.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_status.setObjectName("label_status")
        self.gridLayout.addWidget(self.label_status, 7, 0, 1, 1)
        self.label_kwota_brutto = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_kwota_brutto.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_kwota_brutto.setObjectName("label_kwota_brutto")
        self.gridLayout.addWidget(self.label_kwota_brutto, 5, 0, 1, 1)
        self.lineedit_numer_fv = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.lineedit_numer_fv.setObjectName("lineedit_numer_fv")
        self.gridLayout.addWidget(self.lineedit_numer_fv, 2, 1, 1, 1)
        self.label_nr_konta = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_nr_konta.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_nr_konta.setObjectName("label_nr_konta")
        self.gridLayout.addWidget(self.label_nr_konta, 6, 0, 1, 1)
        self.lineedit_kwota_netto = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.lineedit_kwota_netto.setObjectName("lineedit_kwota_netto")
        self.gridLayout.addWidget(self.lineedit_kwota_netto, 4, 1, 1, 1)
        self.lineedit_sprzedawca = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.lineedit_sprzedawca.setObjectName("lineedit_sprzedawca")
        self.gridLayout.addWidget(self.lineedit_sprzedawca, 3, 1, 1, 1)
        self.label_termin_platnosci = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_termin_platnosci.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_termin_platnosci.setObjectName("label_termin_platnosci")
        self.gridLayout.addWidget(self.label_termin_platnosci, 10, 0, 1, 1)
        self.lineedit_numer_konta = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.lineedit_numer_konta.setObjectName("lineedit_numer_konta")
        self.gridLayout.addWidget(self.lineedit_numer_konta, 6, 1, 1, 1)
        self.dateEdit_termin_platnosci = QtWidgets.QDateEdit(parent=self.verticalLayoutWidget)
        self.dateEdit_termin_platnosci.setObjectName("dateEdit_termin_platnosci")
        self.gridLayout.addWidget(self.dateEdit_termin_platnosci, 10, 1, 1, 1)
        self.lineedit_kwota_brutto = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.lineedit_kwota_brutto.setObjectName("lineedit_kwota_brutto")
        self.gridLayout.addWidget(self.lineedit_kwota_brutto, 5, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit_file_name = QtWidgets.QLineEdit(parent=self.verticalLayoutWidget)
        self.lineEdit_file_name.setReadOnly(True)
        self.lineEdit_file_name.setObjectName("lineEdit_file_name")
        self.horizontalLayout_2.addWidget(self.lineEdit_file_name)
        self.toolButton_open_file = QtWidgets.QToolButton(parent=self.verticalLayoutWidget)
        self.toolButton_open_file.setObjectName("toolButton_open_file")
        self.horizontalLayout_2.addWidget(self.toolButton_open_file)
        self.gridLayout.addLayout(self.horizontalLayout_2, 9, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.dodaj = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.dodaj.setAutoDefault(False)
        self.dodaj.setObjectName("dodaj")
        self.horizontalLayout.addWidget(self.dodaj)
        self.anuluj = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.anuluj.setAutoDefault(False)
        self.anuluj.setObjectName("anuluj")
        self.horizontalLayout.addWidget(self.anuluj)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 9)
        self.verticalLayout.setStretch(3, 1)
        self.verticalLayout.setStretch(4, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.dateEdit_data_wystawienia, self.lineedit_numer_fv)
        Dialog.setTabOrder(self.lineedit_numer_fv, self.lineedit_sprzedawca)
        Dialog.setTabOrder(self.lineedit_sprzedawca, self.lineedit_kwota_netto)
        Dialog.setTabOrder(self.lineedit_kwota_netto, self.lineedit_kwota_brutto)
        Dialog.setTabOrder(self.lineedit_kwota_brutto, self.lineedit_numer_konta)
        Dialog.setTabOrder(self.lineedit_numer_konta, self.comboBox)
        Dialog.setTabOrder(self.comboBox, self.lineEdit_file_name)
        Dialog.setTabOrder(self.lineEdit_file_name, self.toolButton_open_file)
        Dialog.setTabOrder(self.toolButton_open_file, self.dateEdit_termin_platnosci)
        Dialog.setTabOrder(self.dateEdit_termin_platnosci, self.dodaj)
        Dialog.setTabOrder(self.dodaj, self.anuluj)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dodawanie Faktury"))
        self.label.setText(_translate("Dialog", "Dodawanie FV"))
        self.label_termin_wystawienia.setText(_translate("Dialog", "Data wystawienia: "))
        self.comboBox.setItemText(0, _translate("Dialog", "Nieopłacona"))
        self.comboBox.setItemText(1, _translate("Dialog", "Opłacona"))
        self.label_sprzedawca.setText(_translate("Dialog", "Nazwa sprzedawcy:"))
        self.label_numer_fv.setText(_translate("Dialog", "Numer FV: "))
        self.label_plik_fv.setText(_translate("Dialog", "Plik FV"))
        self.label_kwota_netto.setText(_translate("Dialog", "Kwota netto"))
        self.label_status.setText(_translate("Dialog", "Status:"))
        self.label_kwota_brutto.setText(_translate("Dialog", "Kwota brutto"))
        self.label_nr_konta.setText(_translate("Dialog", "Numer konta bankowego: "))
        self.label_termin_platnosci.setText(_translate("Dialog", "Termin płatności: "))
        self.toolButton_open_file.setText(_translate("Dialog", "..."))
        self.dodaj.setText(_translate("Dialog", "Dodaj"))
        self.anuluj.setText(_translate("Dialog", "Anuluj"))
