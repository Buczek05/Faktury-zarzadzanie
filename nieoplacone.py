from layout.nieoplacone_dialog_ui import Ui_Dialog
from PyQt6.QtWidgets import *
from PyQt6.QtSql import *
from PyQt6.QtCore import *
import os


class Nieoplacone(QDialog, Ui_Dialog):
    def __init__(self, overdue, today, tommorow, more_days):
        super(Nieoplacone, self).__init__()
        self.setupUi(self)
        self.setLayout(self.verticalLayout)
        self.setWindowTitle("Faktury do opłacenia")

        self.overdue = overdue
        self.today = today
        self.tommorow = tommorow
        self.more_days = more_days
        self.set_labels()
        self.what_to_do = 0  # 0 - nic, 1 - pokaż, 2 - przypomnij
        self.btn_ok.clicked.connect(self.evt_ok)
        self.btn_show.clicked.connect(self.evt_show)
        self.btn_remember.clicked.connect(self.evt_remember)

    def set_labels(self):
        if self.overdue == 0:
            self.zalegle.setStyleSheet("color: green")
        else:
            self.zalegle.setStyleSheet("color: red")

        if self.today == 0:
            self.dzisiaj.setStyleSheet("color: green")
        else:
            self.dzisiaj.setStyleSheet("color: red")

        if self.tommorow == 0:
            self.jutro.setStyleSheet("color: green")
        else:
            self.jutro.setStyleSheet("color: red")

        if self.more_days == 0:
            self.pozniej.setStyleSheet("color: green")
        else:
            self.pozniej.setStyleSheet("color: red")

        self.zalegle.setText("Zaległe: " + str(self.overdue))
        self.dzisiaj.setText("Dzisiaj: " + str(self.today))
        self.jutro.setText("Jutro: " + str(self.tommorow))
        self.pozniej.setText("Później: " + str(self.more_days))

    def evt_ok(self):
        self.close()

    def evt_show(self):
        self.what_to_do = 1
        self.close()

    def evt_remember(self):
        self.what_to_do = 2
        self.close()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Nieoplacone(1, 1, 1, 1)
    window.show()
    sys.exit(app.exec())
