from layout.placenie_ui import Ui_Dialog
from PyQt6.QtWidgets import *
from PyQt6.QtSql import *
from PyQt6.QtCore import *
import os


class Payment(QDialog, Ui_Dialog):
    def __init__(self, id):
        super(Payment, self).__init__()
        self.czy_zaplacono = False
        self.setupUi(self)
        self.id = id

        self.zaplacono.clicked.connect(self.evt_zaplacono)
        self.open_file.clicked.connect(self.evt_open_file)
        self.anuluj.clicked.connect(self.evt_anuluj)

        self.setup_data()

    def setup_data(self):
        if not QSqlDatabase.database().isValid():
            self.db = QSqlDatabase.addDatabase("QSQLITE")
            path = os.path.join(os.path.dirname(__file__), "data", "database.db")
            self.db.setDatabaseName(path)
            self.db.open()
        else:
            self.db = QSqlDatabase.database()
        self.query = QSqlQuery()

        self.query.exec(
            "SELECT faktury.id, id_sprzedawcy, status_fv, nazwa as sprzedawca, numer_fv, numer_konta_bankowego, kwota_brutto, nazwa_pliku FROM faktury LEFT JOIN sprzedawcy ON id_sprzedawcy = sprzedawcy.id WHERE faktury.id = {}".format(
                self.id
            )
        )

        self.query.next()

        if self.query.value("status_fv") == 1:
            self.czy_zaplacono = True
            QMessageBox.warning(
                self,
                "Błąd",
                "Faktura została już opłacona",
                QMessageBox.StandardButton.Ok,
            )
            return None

        self.firma.setText("Sprzedawca - {}".format(self.query.value("sprzedawca")))
        self.nr_fv.setText("Nr faktury - {}".format(self.query.value("numer_fv")))
        self.numer_konta.setText(
            "Numer konta - {}".format(self.query.value("numer_konta_bankowego"))
        )
        self.kwota_brutto.setText(
            "Kwota brutto - {}".format(self.query.value("kwota_brutto"))
        )

    def evt_open_file(self):
        file = self.query.value("nazwa_pliku")
        if ".pdf" in file:
            file = os.path.join(os.path.dirname(__file__), "data", "pdf", file)
            try:
                os.startfile(file)
            except:
                QMessageBox.warning(
                    self,
                    "Błąd",
                    "Nie można otworzyć pliku. Plik nie jest w formacie PDF lub jest pusty",
                    QMessageBox.StandardButton.Ok,
                )
        else:
            QMessageBox.warning(
                self,
                "Błąd",
                "Nie można otworzyć pliku. Plik nie jest w formacie PDF lub jest pusty",
                QMessageBox.StandardButton.Ok,
            )

    def evt_zaplacono(self):
        self.czy_zaplacono = True
        self.query.exec(
            "UPDATE faktury SET status_fv = 1 WHERE id = {}".format(self.id)
        )
        print(self.query.lastError().text())
        QMessageBox.information(self, "Informacja", "Zapłacono")
        self.close()

    def evt_anuluj(self):
        self.close()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = Payment(6)
    window.show()
    sys.exit(app.exec())
