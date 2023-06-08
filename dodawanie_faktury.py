from layout.dodawanie_faktury_ui import Ui_Dialog
from PyQt6.QtWidgets import *
import os


def wrong_input_style():
    return """
        QLineEdit{
            border: 2px solid red;
        }
        """


class Dodawanie_Faktury(QDialog, Ui_Dialog):
    def __init__(self):
        super(Dodawanie_Faktury, self).__init__()
        self.setupUi(self)
        self.setLayout(self.verticalLayout)

        self.czy_dodano = False

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
        except ValueError:
            errors.append("Kwota brutto musi być liczbą")
            self.lineedit_kwota_brutto.setStyleSheet(wrong_input_style())
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
            self.czy_dodano = True
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
