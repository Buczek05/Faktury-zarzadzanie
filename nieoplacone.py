from layout.nieoplacone_dialog_ui import Ui_Dialog
from PyQt6.QtWidgets import *


class Nieoplacone(QDialog, Ui_Dialog):
    def __init__(self):
        super(Nieoplacone, self).__init__()
        self.setupUi(self)
        self.setLayout(self.verticalLayout)
        self.setWindowTitle("Faktury do opłacenia")

        self.what_to_do = 0  # 0 - nic, 1 - pokaż, 2 - przypomnij
        self.btn_ok.clicked.connect(self.evt_ok)
        self.btn_show.clicked.connect(self.evt_show)
        self.btn_remember.clicked.connect(self.evt_remember)

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
    window = Nieoplacone()
    window.show()
    sys.exit(app.exec())
