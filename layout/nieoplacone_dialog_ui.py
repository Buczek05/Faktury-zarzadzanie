# Form implementation generated from reading ui file 'layout/nieoplacone_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.5.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(285, 239)
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 272, 241))
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
        self.zalegle = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.zalegle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.zalegle.setObjectName("zalegle")
        self.verticalLayout.addWidget(self.zalegle)
        self.dzisiaj = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.dzisiaj.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.dzisiaj.setObjectName("dzisiaj")
        self.verticalLayout.addWidget(self.dzisiaj)
        self.jutro = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.jutro.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.jutro.setObjectName("jutro")
        self.verticalLayout.addWidget(self.jutro)
        self.pozniej = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.pozniej.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.pozniej.setObjectName("pozniej")
        self.verticalLayout.addWidget(self.pozniej)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_show = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.btn_show.setObjectName("btn_show")
        self.horizontalLayout.addWidget(self.btn_show)
        self.btn_ok = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.btn_ok.setObjectName("btn_ok")
        self.horizontalLayout.addWidget(self.btn_ok)
        self.btn_remember = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.btn_remember.setObjectName("btn_remember")
        self.horizontalLayout.addWidget(self.btn_remember)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.btn_show, self.btn_ok)
        Dialog.setTabOrder(self.btn_ok, self.btn_remember)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Przypomnienia"))
        self.title.setText(_translate("Dialog", "Nieopłacone FV"))
        self.zalegle.setText(_translate("Dialog", "Zaległe - "))
        self.dzisiaj.setText(_translate("Dialog", "Dzisiaj - "))
        self.jutro.setText(_translate("Dialog", "Jutro - "))
        self.pozniej.setText(_translate("Dialog", "Później -"))
        self.btn_show.setText(_translate("Dialog", "Pokaż"))
        self.btn_ok.setText(_translate("Dialog", "Ok"))
        self.btn_remember.setText(_translate("Dialog", "Przypomnij później"))
