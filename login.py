from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from layout.login_ui import Ui_Dialog
import hashlib

PASSWORD = "abe31fe1a2113e7e8bf174164515802806d388cf4f394cceace7341a182271ab"


class Login(QDialog, Ui_Dialog):
    def __init__(self):
        super(Login, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Logowanie")
        self.setLayout(self.verticalLayout)
        self.pushButton.clicked.connect(self.evt_login)
        self.login_entered = False

    def evt_login(self):
        self.password = self.lineEdit.text()
        self.password = hashlib.sha256(self.password.encode()).hexdigest()
        if self.password == PASSWORD:
            self.login_entered = True
            self.close()

        else:
            QMessageBox.warning(
                self,
                "Błąd",
                "Hasło nieprawidłowe",
                QMessageBox.StandardButton.Ok,
            )
            return


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    login = Login()
    login.exec()
