from layout.placenie_ui import Ui_Dialog
from PyQt6.QtWidgets import QDialog, QApplication


class Payment(QDialog, Ui_Dialog):
    def __init__(self):
        super(Payment, self).__init__()
        self.czy_zaplacono = False
        self.setupUi(self)

        self.zaplacono.clicked.connect(self.evt_zaplacono)
        self.anuluj.clicked.connect(self.evt_anuluj)

    def evt_zaplacono(self):
        self.czy_zaplacono = True
        self.close()

    def evt_anuluj(self):
        self.close()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = Payment()
    window.show()
    sys.exit(app.exec())
