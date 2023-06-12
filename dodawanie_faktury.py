from layout.dodawanie_faktury_ui import Ui_Dialog
from PyQt6.QtWidgets import *
from PyQt6.QtSql import *
from PyQt6.QtCore import *
import os, shutil


def wrong_input_style():
    return """
        QLineEdit{
            border: 2px solid red;
        }
        QDateEdit{
            border: 2px solid red;
        }
        """


class Dodawanie_Faktury(QDialog, Ui_Dialog):
    def __init__(self):
        super(Dodawanie_Faktury, self).__init__()
        self.setupUi(self)
        self.setLayout(self.verticalLayout)

        self.czy_dodano = False
        self.file_path = None

        self.dateEdit_data_wystawienia.setDate(QDate.currentDate())
        self.dateEdit_termin_platnosci.setDate(QDate.currentDate())

        self.toolButton_open_file.clicked.connect(self.evt_open_file)
        self.dodaj.clicked.connect(self.evt_dodaj)
        self.anuluj.clicked.connect(self.evt_anuluj)

    def evt_open_file(self):
        fname = QFileDialog.getOpenFileName(self, "Open file", "", "PDF (*.pdf)")
        if fname[0]:
            file_name = os.path.basename(fname[0])
            self.lineEdit_file_name.setText(file_name)
            self.file_path = fname[0]

    def check_parametrs(self):
        self.lineedit_numer_fv.setStyleSheet("")
        self.lineedit_sprzedawca.setStyleSheet("")
        self.lineedit_kwota_netto.setStyleSheet("")
        self.lineedit_kwota_brutto.setStyleSheet("")
        self.lineEdit_file_name.setStyleSheet("")
        self.dateEdit_termin_platnosci.setStyleSheet("")
        self.dateEdit_termin_platnosci.setStyleSheet("")
        errors = []

        if not self.lineedit_numer_fv.text():
            errors.append("Nie podano numeru faktury")
            self.lineedit_numer_fv.setStyleSheet(wrong_input_style())
        if not self.lineedit_sprzedawca.text():
            errors.append("Nie podano sprzedawcy")
            self.lineedit_sprzedawca.setStyleSheet(wrong_input_style())
        if not self.lineedit_kwota_netto.text():
            errors.append("Nie podano kwoty netto")
            self.lineedit_kwota_netto.setStyleSheet(wrong_input_style())
        try:
            float(
                self.lineedit_kwota_netto.text().replace(",", ".")
            )  # zamiana przecinka na kropkę
            if len(
                self.lineedit_kwota_netto.text().replace(",", ".").split(".")[-1]
            ) > 2 and "." in self.lineedit_kwota_netto.text().replace(",", "."):
                errors.append(
                    "Kwota netto musi mieć maksymalnie 2 miejsca po przecinku"
                )
                self.lineedit_kwota_netto.setStyleSheet(wrong_input_style())
        except ValueError:
            errors.append("Kwota netto musi być liczbą")
            self.lineedit_kwota_netto.setStyleSheet(wrong_input_style())
        if not self.lineedit_kwota_brutto.text():
            errors.append("Nie podano kwoty brutto")
            self.lineedit_kwota_brutto.setStyleSheet(wrong_input_style())
        try:
            float(
                self.lineedit_kwota_brutto.text().replace(",", ".")
            )  # zamiana przecinka na kropkę
            if len(
                self.lineedit_kwota_brutto.text().replace(",", ".").split(".")[-1]
            ) > 2 and "." in self.lineedit_kwota_brutto.text().replace(",", "."):
                errors.append(
                    "Kwota brutto musi mieć maksymalnie 2 miejsca po przecinku"
                )
                self.lineedit_kwota_brutto.setStyleSheet(wrong_input_style())

            if float(self.lineedit_kwota_brutto.text().replace(",", ".")) < float(
                self.lineedit_kwota_netto.text().replace(",", ".")
            ):
                errors.append("Kwota brutto nie może być mniejsza od kwoty netto")
                self.lineedit_kwota_brutto.setStyleSheet(wrong_input_style())
                self.lineedit_kwota_netto.setStyleSheet(wrong_input_style())
        except ValueError:
            errors.append("Kwota brutto musi być liczbą")
            self.lineedit_kwota_brutto.setStyleSheet(wrong_input_style())
        if (
            self.dateEdit_data_wystawienia.date()
            > self.dateEdit_termin_platnosci.date()
        ):
            errors.append(
                "Data wystawienia nie może być późniejsza niż termin płatności"
            )
            self.dateEdit_termin_platnosci.setStyleSheet(wrong_input_style())
            self.dateEdit_data_wystawienia.setStyleSheet(wrong_input_style())
        if not self.file_path:
            errors.append("Nie wybrano pliku")
            self.lineEdit_file_name.setStyleSheet(wrong_input_style())
        if errors:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("\n".join(errors))
            msg.setWindowTitle("Błąd")
            msg.exec()
            return False
        else:
            return True

    def evt_dodaj(self):
        if self.check_parametrs():
            # add to database
            if not QSqlDatabase.database().isValid():
                self.db = QSqlDatabase.addDatabase("QSQLITE")
                path = os.path.join(os.path.dirname(__file__), "data", "database.db")
                self.db.setDatabaseName(path)
                self.db.open()
            else:
                self.db = QSqlDatabase.database()
            self.query = QSqlQuery()

            self.query.exec("SELECT id FROM faktury ORDER BY id DESC LIMIT 1")
            self.query.next()
            try:
                id = self.query.value(0) + 1
            except:
                id = 1
            file_name = "{}____{}.pdf".format(id, self.lineedit_numer_fv.text())

            self.query.prepare(
                "INSERT INTO faktury (data_wystawienia, numer_fv, sprzedawca, kwota_netto, kwota_brutto, numer_konta_bankowego, status_fv, termin_platnosci, nazwa_pliku) VALUES (:data_wystawienia, :numer_fv, :sprzedawca, :kwota_netto, :kwota_brutto, :numer_konta_bankowego, :status_fv, :termin_platnosci, :nazwa_pliku)"
            )
            self.query.bindValue(
                ":data_wystawienia",
                self.dateEdit_data_wystawienia.date().toString("yyyy-MM-dd"),
            )
            self.query.bindValue(":numer_fv", self.lineedit_numer_fv.text())
            self.query.bindValue(":sprzedawca", self.lineedit_sprzedawca.text())
            self.query.bindValue(
                ":kwota_netto",
                float(self.lineedit_kwota_netto.text().replace(",", ".")),
            )
            self.query.bindValue(
                ":kwota_brutto",
                float(self.lineedit_kwota_brutto.text().replace(",", ".")),
            )
            self.query.bindValue(
                ":numer_konta_bankowego", self.lineedit_numer_konta.text()
            )
            self.query.bindValue(":status_fv", self.comboBox.currentIndex())
            self.query.bindValue(
                ":termin_platnosci",
                self.dateEdit_termin_platnosci.date().toString("yyyy-MM-dd"),
            )
            self.query.bindValue(
                ":nazwa_pliku",
                file_name,
            )
            if self.query.exec():
                self.czy_dodano = True
                QMessageBox.information(
                    self,
                    "Dodano",
                    "Dodano fakturę",
                    QMessageBox.StandardButton.Ok,
                )
                # copy file to data folder
                new_path = os.path.join(
                    os.path.dirname(__file__), "data", "pdf", file_name
                )
                shutil.copyfile(self.file_path, new_path)

            else:
                QMessageBox.critical(
                    self,
                    "Błąd",
                    "Nie udało się dodać faktury",
                    QMessageBox.StandardButton.Ok,
                )

            self.close()

    def evt_anuluj(self):
        self.close()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Dodawanie_Faktury()
    window.show()
    sys.exit(app.exec())
