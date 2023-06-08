from layout.main_window_ui import Ui_MainWindow
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtSql import *
import os
from dodawanie_faktury import Dodawanie_Faktury


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Faktury")
        self.centralwidget.setLayout(self.verticalLayout)

        self.sort_index = -1
        self.sorting_ascending = True
        self.show_all_unpaid_paid = 0  # 0 - all, 1 - unpaid, 2 - paid
        self.sorting_column_name = "id"

        self.set_table_headers()
        self.setup_connection()
        self.create_db_file_and_table_if_not_exists()
        self.populating_table()

    ### SQL ###
    def create_db_file_and_table_if_not_exists(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        path = os.path.join(os.path.dirname(__file__), "data", "fv.db")
        self.db.setDatabaseName(path)
        if self.db.open():
            if "faktury" not in self.db.tables():
                self.query = QSqlQuery()
                self.query.exec(
                    """CREATE TABLE IF NOT EXISTS faktury (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data_wystawienia TEXT,
                    numer_fv TEXT,
                    sprzedawca TEXT,
                    kwota_netto REAL,
                    kwota_brutto REAL,
                    numer_konta_bankowego TEXT,
                    status_fv BOOLEAN, 
                    termin_platnosci TEXT,
                    nazwa_pliku TEXT
                    )"""  ### status_fv - 0 - nieopłacona, 1 - opłacona
                )
                # test data
                self.query.exec(
                    """INSERT INTO faktury (data_wystawienia, numer_fv, sprzedawca, kwota_netto, kwota_brutto, numer_konta_bankowego, status_fv, termin_platnosci, nazwa_pliku) VALUES ('2021-01-01', '1/2021', 'Jan Kowalski', 100, 123, '123456789', 0, '2021-01-31', 'test.pdf')"""
                )
                self.query.exec(
                    """INSERT INTO faktury (data_wystawienia, numer_fv, sprzedawca, kwota_netto, kwota_brutto, numer_konta_bankowego, status_fv, termin_platnosci, nazwa_pliku) VALUES ('2021-02-01', '2/2021', 'Jan Kowalski', 200, 246, '123456789', 1, '2021-02-28', 'test.pdf')"""
                )
                self.query.exec(
                    """INSERT INTO faktury (data_wystawienia, numer_fv, sprzedawca, kwota_netto, kwota_brutto, numer_konta_bankowego, status_fv, termin_platnosci, nazwa_pliku) VALUES ('2021-03-01', '3/2021', 'Jan Kowalski', 300, 369, '123456789', 0, '2021-03-31', 'test.pdf')"""
                )
                self.query.exec(
                    """INSERT INTO faktury (data_wystawienia, numer_fv, sprzedawca, kwota_netto, kwota_brutto, numer_konta_bankowego, status_fv, termin_platnosci, nazwa_pliku) VALUES ('2021-02-01', '2/2021', 'Jan Kowalski', 200, 246, '123456789', 1, '2021-02-28', 'test.pdf')"""
                )  # TODO: remove test data
                print(self.query.lastError().text())
        else:
            QMessageBox.critical(
                self,
                "Błąd",
                "Nie udało się otworzyć bazy danych",
                QMessageBox.StandardButton.Ok,
            )

        ### FOLDER FOR PDF FILES ###
        if not os.path.exists(os.path.join(os.path.dirname(__file__), "data", "pdf")):
            os.makedirs(os.path.join(os.path.dirname(__file__), "data", "pdf"))

    def populating_table(self):
        # Clear the table.
        self.tableWidget.setRowCount(0)
        self.tableWidget.clearContents()
        # Create a query to select the data.

        match self.show_all_unpaid_paid:
            case 0:
                where_clause = ""
            case 1:
                where_clause = "WHERE status_fv = 0"
            case 2:
                where_clause = "WHERE status_fv = 1"

        self.query = QSqlQuery()
        self.query.exec(
            "SELECT id, data_wystawienia, numer_fv, sprzedawca, kwota_netto, kwota_brutto, numer_konta_bankowego, status_fv, termin_platnosci FROM faktury {} ORDER BY {} {}".format(
                where_clause,
                self.sorting_column_name,
                "ASC" if self.sorting_ascending else "DESC",
            )
        )
        # Populate the table.
        while self.query.next():
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            for col in range(8):
                if col == 6:
                    self.tableWidget.setItem(
                        row,
                        col,
                        QTableWidgetItem(
                            "Opłacona" if self.query.value(col + 1) else "Nieopłacona"
                        ),
                    )
                    continue
                self.tableWidget.setItem(
                    row, col, QTableWidgetItem(str(self.query.value(col + 1)))
                )

    ### SETUP CONNECTIONS ###
    def setup_connection(self):
        # ACTION CLICK CONNECTIONS

        self.action_faktury_Dodaj_FV.triggered.connect(self.evt_add_fv)
        self.action_wyszukiwanie_ZnajdzFV.triggered.connect(self.evt_find_fv)

        self.action_sortowanie_domyslne.setChecked(True)
        self.action_sortowanie_domyslne.triggered.connect(self.evt_sort_default)
        self.action_sortowanie_Data_wystawienia.triggered.connect(
            self.evt_sort_data_wystawienia
        )
        self.action_sortowanie_numer_FV.triggered.connect(self.evt_sort_numer_fv)
        self.action_sortowanie_sprzedawca.triggered.connect(self.evt_sort_sprzedawca)
        self.action_sortowanie_Kwota_netto.triggered.connect(self.evt_sort_kwota_netto)
        self.action_sortowanie_Kwota_brutto.triggered.connect(
            self.evt_sort_kwota_brutto
        )
        self.action_sortowanie_numer_konta_bankowego.triggered.connect(
            self.evt_sort_bank_account_number
        )
        self.action_sortowanie_Status_FV.triggered.connect(self.evt_sort_status_fv)
        self.action_sortowanie_termin_platnosci.triggered.connect(
            self.evt_sort_termin_platnosci
        )

        self.action_sortowanie_rosnaco.setChecked(True)
        self.action_sortowanie_rosnaco.triggered.connect(self.evt_sort_ascending)
        self.action_sortowanie_malejaco.triggered.connect(self.evt_sort_descending)

        self.action_wyswietlanie_Wszystkie.setChecked(True)
        self.action_wyswietlanie_Wszystkie.triggered.connect(self.evt_show_all)
        self.action_wyswietlanie_Nieoplacone.triggered.connect(self.evt_show_unpaid)
        self.action_wyswietlanie_Oplacone.triggered.connect(self.evt_show_paid)

        # ACTION CLICK COLUMN SORTING
        self.tableWidget.horizontalHeader().sectionClicked.connect(self.sorting)

        # TABLE WIDGET CLICK CONNECTIONS
        self.tableWidget.cellDoubleClicked.connect(self.evt_open_fv)

    ### TABLE WIDGET ###

    def set_table_headers(self):
        self.tableWidget.setHorizontalHeaderLabels(
            [
                "Data wystawienia",
                "Numer FV",
                "Sprzedawca",
                "Kwota netto",
                "Kwota brutto",
                "Numer konta bankowego",
                "Status FV",
                "Termin płatności",
            ]
        )
        # TABLE WIDGET ADJUSTMENTS (COLUMN WIDTHS)
        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setColumnWidth(2, 200)
        self.tableWidget.setColumnWidth(3, 100)
        self.tableWidget.setColumnWidth(4, 100)
        self.tableWidget.setColumnWidth(5, 170)
        self.tableWidget.setColumnWidth(6, 80)
        self.tableWidget.setColumnWidth(7, 120)

    def get_column_sql_name(self, index):
        match index:
            case -1:
                return "id"
            case 0:
                return "data_wystawienia"
            case 1:
                return "numer_fv"
            case 2:
                return "sprzedawca"
            case 3:
                return "kwota_netto"
            case 4:
                return "kwota_brutto"
            case 5:
                return "numer_konta_bankowego"
            case 6:
                return "status_fv"
            case 7:
                return "termin_platnosci"

    def sorting(self, index):
        if index == self.sort_index:
            self.sorting_ascending = not self.sorting_ascending
            self.change_sort_order()
        else:
            self.sort_index = index

        self.set_table_headers()
        self.unchecked_sort(index)
        self.sorting_column_name = self.get_column_sql_name(index)
        self.populating_table()

        text = self.tableWidget.horizontalHeaderItem(index).text()
        self.tableWidget.horizontalHeaderItem(index).setText(
            text + " ▼" if self.sorting_ascending else text + " ▲"
        )

    def evt_open_fv(self, row, column):
        self.query.prepare(
            "SELECT nazwa_pliku from faktury WHERE data_wystawienia = :data_wystawienia AND numer_fv = :numer_fv AND Sprzedawca = :sprzedawca AND kwota_netto = :kwota_netto AND kwota_brutto = :kwota_brutto AND numer_konta_bankowego = :numer_konta_bankowego AND termin_platnosci = :termin_platnosci"
        )
        self.query.bindValue(":data_wystawienia", self.tableWidget.item(row, 0).text())
        self.query.bindValue(":numer_fv", self.tableWidget.item(row, 1).text())
        self.query.bindValue(":sprzedawca", self.tableWidget.item(row, 2).text())
        self.query.bindValue(
            ":kwota_netto", float(self.tableWidget.item(row, 3).text())
        )
        self.query.bindValue(
            ":kwota_brutto", float(self.tableWidget.item(row, 4).text())
        )
        self.query.bindValue(
            ":numer_konta_bankowego", self.tableWidget.item(row, 5).text()
        )
        self.query.bindValue(":termin_platnosci", self.tableWidget.item(row, 7).text())

        self.query.exec()
        self.query.next()
        print(self.query.value(0))
        file = self.query.value(0)
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

    ### EVENT HANDLERS - ACTION ###
    def unchecked_sort(self, index):
        self.action_sortowanie_domyslne.setChecked(False)
        self.action_sortowanie_Data_wystawienia.setChecked(False)
        self.action_sortowanie_numer_FV.setChecked(False)
        self.action_sortowanie_sprzedawca.setChecked(False)
        self.action_sortowanie_Kwota_netto.setChecked(False)
        self.action_sortowanie_Kwota_brutto.setChecked(False)
        self.action_sortowanie_numer_konta_bankowego.setChecked(False)
        self.action_sortowanie_Status_FV.setChecked(False)
        self.action_sortowanie_termin_platnosci.setChecked(False)

        match index:
            case -1:
                self.action_sortowanie_domyslne.setChecked(True)
            case 0:
                self.action_sortowanie_Data_wystawienia.setChecked(True)
            case 1:
                self.action_sortowanie_numer_FV.setChecked(True)
            case 2:
                self.action_sortowanie_sprzedawca.setChecked(True)
            case 3:
                self.action_sortowanie_Kwota_netto.setChecked(True)
            case 4:
                self.action_sortowanie_Kwota_brutto.setChecked(True)
            case 5:
                self.action_sortowanie_numer_konta_bankowego.setChecked(True)
            case 6:
                self.action_sortowanie_Status_FV.setChecked(True)
            case 7:
                self.action_sortowanie_termin_platnosci.setChecked(True)

    def change_sort_order(self):
        self.action_sortowanie_rosnaco.setChecked(self.sorting_ascending)
        self.action_sortowanie_malejaco.setChecked(not self.sorting_ascending)

    def unchecked_display(self):
        self.action_wyswietlanie_Wszystkie.setChecked(False)
        self.action_wyswietlanie_Nieoplacone.setChecked(False)
        self.action_wyswietlanie_Oplacone.setChecked(False)

    def evt_add_fv(self):
        new_fv = Dodawanie_Faktury()
        new_fv.exec()
        if new_fv.czy_dodano:
            self.populating_table()

    def evt_find_fv(self):
        pass

    def evt_sort_default(self):
        self.evt_sort_column_clicked(-1)

    def evt_sort_data_wystawienia(self):
        self.evt_sort_column_clicked(0)

    def evt_sort_numer_fv(self):
        self.evt_sort_column_clicked(1)

    def evt_sort_sprzedawca(self):
        self.evt_sort_column_clicked(2)

    def evt_sort_kwota_netto(self):
        self.evt_sort_column_clicked(3)

    def evt_sort_kwota_brutto(self):
        self.evt_sort_column_clicked(4)

    def evt_sort_bank_account_number(self):
        self.evt_sort_column_clicked(5)

    def evt_sort_status_fv(self):
        self.evt_sort_column_clicked(6)

    def evt_sort_termin_platnosci(self):
        self.evt_sort_column_clicked(7)

    def evt_sort_descending(self):
        if self.sorting_ascending == True:
            self.evt_sort_column_clicked(self.sort_index)
        else:
            self.action_sortowanie_malejaco.setChecked(True)

    def evt_sort_ascending(self):
        if self.sorting_ascending == False:
            self.evt_sort_column_clicked(self.sort_index)
        else:
            self.action_sortowanie_rosnaco.setChecked(True)

    def evt_show_all(self):
        self.unchecked_display()
        self.action_wyswietlanie_Wszystkie.setChecked(True)
        self.show_all_unpaid_paid = 0
        self.populating_table()

    def evt_show_unpaid(self):
        self.unchecked_display()
        self.action_wyswietlanie_Nieoplacone.setChecked(True)
        self.show_all_unpaid_paid = 1
        self.populating_table()

    def evt_show_paid(self):
        self.unchecked_display()
        self.action_wyswietlanie_Oplacone.setChecked(True)
        self.show_all_unpaid_paid = 2
        self.populating_table()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
