from layout.dodawanie_faktury_ui import Ui_Dialog
from PyQt6.QtWidgets import *
from PyQt6.QtSql import *
from PyQt6.QtCore import *
import os, shutil, math


def wrong_input_style():
    return """
        QLineEdit{
            border: 2px solid red;
        }
        QDateEdit{
            border: 2px solid red;
        }
        """


class Dodawanie_Edytowanie_Faktury(QDialog, Ui_Dialog):
    def __init__(self, id=None):
        super(Dodawanie_Edytowanie_Faktury, self).__init__()
        self.setupUi(self)
        self.setLayout(self.verticalLayout)

        self.set_database()
        self.set_completer()

        if id:
            self.setWindowTitle("Edytowanie faktury")
            self.id = id
            self.query.exec("SELECT * FROM faktury WHERE id = {}".format(self.id))
            if self.query.next():
                self.lineedit_numer_fv.setText(self.query.value("numer_fv"))
                self.lineedit_numer_konta.setText(
                    self.query.value("numer_konta_bankowego")
                )
                self.lineedit_kwota_netto.setText(str(self.query.value("kwota_netto")))
                self.lineedit_kwota_brutto.setText(
                    str(self.query.value("kwota_brutto"))
                )
                data_wystawienia = self.query.value("data_wystawienia").split("-")
                self.dateEdit_data_wystawienia.setDate(
                    QDate(
                        int(data_wystawienia[0]),
                        int(data_wystawienia[1]),
                        int(data_wystawienia[2]),
                    )
                )
                termin_platnosci = self.query.value("termin_platnosci").split("-")
                self.dateEdit_termin_platnosci.setDate(
                    QDate(
                        int(termin_platnosci[0]),
                        int(termin_platnosci[1]),
                        int(termin_platnosci[2]),
                    )
                )
                self.comboBox.setCurrentIndex(self.query.value("status_fv"))
                self.lineEdit_file_name.setText(self.query.value("nazwa_pliku"))
                self.file_path = os.path.join(
                    os.path.dirname(__file__),
                    "data",
                    "pdf",
                    self.query.value("nazwa_pliku"),
                )
                self.dodaj.setText("Zapisz zmiany")
                self.dodaj.clicked.connect(self.evt_save_changes)
                self.query.exec(
                    "SELECT nazwa FROM sprzedawcy WHERE id = {}".format(
                        self.query.value("id_sprzedawcy")
                    )
                )
                if self.query.next():
                    self.lineedit_sprzedawca.setText(self.query.value(0))
            else:
                QMessageBox.critical(
                    self, "Błąd", "Nie znaleziono faktury o podanym id"
                )
                self.close()
        else:
            self.file_path = None
            self.dodaj.clicked.connect(self.evt_dodaj)

        self.dateEdit_data_wystawienia.setDate(QDate.currentDate())
        self.dateEdit_termin_platnosci.setDate(QDate.currentDate())

        self.lineedit_sprzedawca.textChanged.connect(self.evt_sprzedawca_changed)
        self.lineedit_kwota_netto.textChanged.connect(self.evt_kwota_netto_changed)
        self.lineedit_kwota_brutto.textChanged.connect(self.evt_kwota_brutto_changed)

        self.toolButton_open_file.clicked.connect(self.evt_open_file)
        self.anuluj.clicked.connect(self.evt_anuluj)

    def set_database(self):
        if not QSqlDatabase.database().isValid():
            self.db = QSqlDatabase.addDatabase("QSQLITE")
            path = os.path.join(os.path.dirname(__file__), "data", "database.db")
            self.db.setDatabaseName(path)
            self.db.open()
        else:
            self.db = QSqlDatabase.database()
        self.query = QSqlQuery()

    def set_completer(self):
        self.completer_nazwa = QCompleter()
        self.completer_nazwa.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer_nazwa.setFilterMode(Qt.MatchFlag.MatchContains)
        self.lineedit_sprzedawca.setCompleter(self.completer_nazwa)

        self.model_nazwa = QSqlQueryModel()
        self.model_nazwa.setQuery("SELECT nazwa FROM sprzedawcy")
        self.completer_nazwa.setModel(self.model_nazwa)

        self.completer_konto = QCompleter()
        self.completer_konto.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer_konto.setFilterMode(Qt.MatchFlag.MatchContains)
        self.lineedit_numer_konta.setCompleter(self.completer_konto)

        self.model_konto = QSqlQueryModel()
        self.model_konto.setQuery("SELECT nr_konta FROM sprzedawcy")
        self.completer_konto.setModel(self.model_konto)

    def evt_sprzedawca_changed(self):
        sprzedawca = self.lineedit_sprzedawca.text()
        self.query.exec(
            "SELECT * FROM sprzedawcy WHERE nazwa = '{}'".format(sprzedawca)
        )
        if self.query.next():
            self.lineedit_numer_konta.setText(self.query.value(2))

    def evt_kwota_netto_changed(self):
        kursor = self.lineedit_kwota_netto.cursorPosition()
        kwota_netto = self.lineedit_kwota_netto.text()
        try:
            self.lineedit_kwota_netto.setStyleSheet("")
            kwota_netto = float(kwota_netto)
            if kwota_netto < 0:
                raise Exception
            self.lineedit_kwota_netto.setText(str(math.floor(kwota_netto * 100) / 100))
            kwota_brutto = kwota_netto * 1.23
            self.lineedit_kwota_brutto.setText(str(round(kwota_brutto, 2)))

        except:
            self.lineedit_kwota_netto.setStyleSheet(wrong_input_style())
        self.lineedit_kwota_netto.setCursorPosition(kursor)

    def evt_kwota_brutto_changed(self):
        kursor = self.lineedit_kwota_brutto.cursorPosition()
        kwota_brutto = self.lineedit_kwota_brutto.text()
        try:
            self.lineedit_kwota_brutto.setStyleSheet("")
            kwota_brutto = float(kwota_brutto)
            if kwota_brutto < 0:
                raise Exception
            self.lineedit_kwota_brutto.setText(
                str(math.floor(kwota_brutto * 100) / 100)
            )
        except:
            self.lineedit_kwota_brutto.setStyleSheet(wrong_input_style())
        self.lineedit_kwota_brutto.setCursorPosition(kursor)

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

    def get_id_and_nr_konta(self):
        self.query.exec(
            "SELECT id, nr_konta FROM sprzedawcy WHERE nazwa = '{}'".format(
                self.lineedit_sprzedawca.text()
            )
        )
        # check if sprzedawca is in database
        if not self.query.next():
            self.query.prepare(
                "INSERT INTO sprzedawcy (nazwa, nr_konta) VALUES (:nazwa, :nr_konta)"
            )
            self.query.bindValue(":nazwa", self.lineedit_sprzedawca.text())
            self.query.bindValue(":nr_konta", self.lineedit_numer_konta.text())
            self.query.exec()
            self.query.exec(
                "SELECT id FROM sprzedawcy WHERE nazwa = '{}'".format(
                    self.lineedit_sprzedawca.text()
                )
            )
            self.query.next()
        else:
            self.check_nr_konta(self.query.value(1), self.query.value(0))
        id_sprzedawcy = self.query.value(0)
        nr_konta = self.query.value(1)
        return id_sprzedawcy, nr_konta

    def check_nr_konta(self, nr_konta, id_sprzedawcy):
        change = False
        if nr_konta != self.lineedit_numer_konta.text():
            message = QMessageBox()
            message.setText(
                "Podany numer konta jest inny niż w bazie danych, czy zaktualizować numer konta?"
            )
            message.setWindowTitle("Uwaga")
            message.addButton("Tak", QMessageBox.ButtonRole.YesRole)
            message.addButton("Nie", QMessageBox.ButtonRole.NoRole)
            message.setIcon(QMessageBox.Icon.Warning)
            ret = message.exec()
            if ret == 0:
                change = True
        if not nr_konta or change:
            nr_konta = self.lineedit_numer_konta.text()
            self.query.prepare(
                "UPDATE sprzedawcy SET nr_konta = :nr_konta WHERE id = :id"
            )
            self.query.bindValue(":nr_konta", nr_konta)
            self.query.bindValue(":id", id_sprzedawcy)
            self.query.exec()

    def prepare_sql_message(self, id_sprzedawcy):
        self.query.bindValue(
            ":data_wystawienia",
            self.dateEdit_data_wystawienia.date().toString("yyyy-MM-dd"),
        )
        self.query.bindValue(":numer_fv", self.lineedit_numer_fv.text())
        self.query.bindValue(":id_sprzedawcy", id_sprzedawcy)
        self.query.bindValue(
            ":kwota_netto",
            float(self.lineedit_kwota_netto.text().replace(",", ".")),
        )
        self.query.bindValue(
            ":kwota_brutto",
            float(self.lineedit_kwota_brutto.text().replace(",", ".")),
        )
        self.query.bindValue(":numer_konta_bankowego", self.lineedit_numer_konta.text())
        self.query.bindValue(":status_fv", self.comboBox.currentIndex())
        self.query.bindValue(
            ":termin_platnosci",
            self.dateEdit_termin_platnosci.date().toString("yyyy-MM-dd"),
        )

    def copy_file_to_data_folder(self, file_name):
        new_path = os.path.join(os.path.dirname(__file__), "data", "pdf", file_name)
        if new_path != self.file_path:
            shutil.copyfile(self.file_path, new_path)

    def exec_query(self, file_name, add_edit=True):
        if add_edit:
            texts = ["Dodano", "dodać"]
        else:
            texts = ["Zapisano", "zapisać"]
        if self.query.exec():
            QMessageBox.information(
                self,
                "{}".format(texts[0]),
                "{} fakturę".format(texts[0]),
                QMessageBox.StandardButton.Ok,
            )
            self.copy_file_to_data_folder(file_name)
        else:
            QMessageBox.critical(
                self,
                "Błąd",
                "Nie udało się {} faktury".format(texts[1]),
                QMessageBox.StandardButton.Ok,
            )

    def evt_save_changes(self):
        if self.check_parametrs():
            id_sprzedawcy, nr_konta = self.get_id_and_nr_konta()
            self.query.prepare(
                "UPDATE faktury SET data_wystawienia = :data_wystawienia, numer_fv = :numer_fv, id_sprzedawcy = :id_sprzedawcy, kwota_netto = :kwota_netto, kwota_brutto = :kwota_brutto, numer_konta_bankowego = :numer_konta_bankowego, status_fv = :status_fv, termin_platnosci = :termin_platnosci WHERE id = :id"
            )
            self.prepare_sql_message(id_sprzedawcy)
            self.query.bindValue(":id", self.id)
            self.exec_query("id____{}.pdf".format(self.id), False)
            self.close()

    def evt_dodaj(self):
        if self.check_parametrs():
            id_sprzedawcy, nr_konta = self.get_id_and_nr_konta()

            self.query.exec("SELECT id FROM faktury ORDER BY id DESC LIMIT 1")
            self.query.next()
            try:
                id = self.query.value(0) + 1
            except:
                id = 1
            file_name = "id____{}.pdf".format(id)

            self.query.prepare(
                "INSERT INTO faktury (data_wystawienia, numer_fv, id_sprzedawcy, kwota_netto, kwota_brutto, numer_konta_bankowego, status_fv, termin_platnosci, nazwa_pliku) VALUES (:data_wystawienia, :numer_fv, :id_sprzedawcy, :kwota_netto, :kwota_brutto, :numer_konta_bankowego, :status_fv, :termin_platnosci, :nazwa_pliku)"
            )
            self.prepare_sql_message(id_sprzedawcy)
            self.query.bindValue(
                ":nazwa_pliku",
                file_name,
            )
            self.exec_query(file_name)
            self.close()

    def evt_anuluj(self):
        self.close()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = Dodawanie_Edytowanie_Faktury()
    window.show()
    sys.exit(app.exec())
