from layout.main_window_ui import Ui_MainWindow
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Faktury")
        self.centralwidget.setLayout(self.verticalLayout)

        self.sort_index = -1

        self.set_table_headers()

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

        self.sorting_ascending = True
        self.action_sortowanie_rosnaco.setChecked(True)
        self.action_sortowanie_rosnaco.triggered.connect(self.evt_sort_ascending)
        self.action_sortowanie_malejaco.triggered.connect(self.evt_sort_descending)

        self.action_wyswietlanie_Wszystkie.setChecked(True)
        self.action_wyswietlanie_Wszystkie.triggered.connect(self.evt_show_all)
        self.action_wyswietlanie_Nieoplacone.triggered.connect(self.evt_show_unpaid)
        self.action_wyswietlanie_Oplacone.triggered.connect(self.evt_show_paid)

        # ACTION CLICK COLUMN SORTING
        self.tableWidget.horizontalHeader().sectionClicked.connect(
            self.evt_sort_column_clicked
        )

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

    def evt_sort_column_clicked(self, index):
        if index == self.sort_index:
            self.sorting_ascending = not self.sorting_ascending
            self.change_sort_order()
        else:
            self.sort_index = index
        self.set_table_headers()
        self.unchecked_sort(index)
        print(self.sort_index)
        if index == -1:
            return
        if self.sorting_ascending:
            self.tableWidget.sortItems(index, Qt.SortOrder.AscendingOrder)
            text = self.tableWidget.horizontalHeaderItem(index).text()
            self.tableWidget.horizontalHeaderItem(index).setText(text + " ▼")
        else:
            self.tableWidget.sortItems(index, Qt.SortOrder.DescendingOrder)
            text = self.tableWidget.horizontalHeaderItem(index).text()
            self.tableWidget.horizontalHeaderItem(index).setText(text + " ▲")

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
        pass

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

    def evt_show_unpaid(self):
        self.unchecked_display()
        self.action_wyswietlanie_Nieoplacone.setChecked(True)

    def evt_show_paid(self):
        self.unchecked_display()
        self.action_wyswietlanie_Oplacone.setChecked(True)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
