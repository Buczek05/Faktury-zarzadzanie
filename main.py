from layout.main_window_ui import Ui_MainWindow
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtSql import *
import os, time
from dodawanie_faktury import Dodawanie_Edytowanie_Faktury
from remember_system import Remember_system, Worker_wait_x_min
from nieoplacone import Nieoplacone
from settings import Settings
from placenie import Payment
from dodawanie_samochodu import Dodawanie_Edytowanie_Samochodu
from dodawanie_OC import DodawanieOCAC
from datetime import datetime
from login import Login
from openfile import open_file
from dodawanie_przegladu import DodawaniePrzegladu


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Faktury")
        self.resize(1050, 600)
        self.FONT = QFont("MS Shell Dlg 2", 9)
        self.setFont(self.FONT)

        self.widget_filters = QWidget()
        self.widget_filters.setLayout(self.filers_and_buttons)
        self.lyt_faktury.addWidget(self.widget_filters, 0)
        self.lyt_faktury.addWidget(self.tableWidget, 5)
        self.Faktury.setLayout(self.lyt_faktury)
        self.lyt_samochody.addWidget(self.table_cars, 5)
        self.Samochody.setLayout(self.lyt_samochody)
        self.centralwidget.setLayout(self.lyt_main)
        self.widget_filters.setVisible(False)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.is_logged = False
        self.sort_index = -1
        self.sorting_ascending = True
        self.show_all_unpaid_paid = 0  # 0 - all, 1 - unpaid, 2 - paid
        self.sorting_column_name = "faktury.id"
        self.search_clause_elements = []

        self.evt_tab_changed(0)
        self.setup_tray_icon()
        self.set_table_headers()
        self.set_cars_table_headers()
        self.create_db_file_and_table_if_not_exists()
        self.setup_connection()
        self.setup_searching_lyts()
        self.connect_serching_everything()
        self.populating_table()

    ### SEARCHING ###
    def evt_search_fv(self, checked):
        self.widget_filters.setVisible(checked)

    def setup_searching_lyts(self):
        self.dateEdit_data_wystawienia_konkretna.setVisible(False)
        self.dateEdit_termin_platnosci_konkretna.setVisible(False)
        self.doubleSpinBox_kwota_brutto_konkretna.setVisible(False)
        self.doubleSpinBox_kwota_netto_konkretna.setVisible(False)

        self.groupBox_numer_FV.setLayout(self.lyt_numer_FV_radio_btn)
        self.groupBox_sprzedawca.setLayout(self.lyt_sprzedawca_radio_btn)
        self.groupBox_nr_konta.setLayout(self.lyt_numer_konta_radio_btn)

        self.dateEdit_data_wystawienia_do.setDate(QDate.currentDate())
        self.dateEdit_termin_platnosci_do.setDate(QDate.currentDate())

        font = QFont("MS Shell Dlg 2", 12)
        self.label_data_wystawienia.setFont(font)
        self.label_numer_fv.setFont(font)
        self.label_sprzedawca.setFont(font)
        self.label_kwota_netto.setFont(font)
        self.label_kwota_brutto.setFont(font)
        self.label_nr_konta.setFont(font)
        self.label_termin_platnosci.setFont(font)

    def connect_serching_everything(self):
        self.checkBox_data_wystawienia.stateChanged.connect(self.evt_date_wystawienia)
        self.checkBox_kwota_netto.stateChanged.connect(self.evt_kwota_netto)
        self.checkBox_kwota_brutto.stateChanged.connect(self.evt_kwota_brutto)
        self.checkBox_termin_platnosci.stateChanged.connect(self.evt_termin_platnosci)

        self.btn_search.clicked.connect(self.evt_search_prepare_clause)
        self.btn_clear_search.clicked.connect(self.evt_clear_search)

    def evt_search_prepare_clause(self):
        self.search_clause_elements = []
        ###### DATA WYSTAWIENIA ######
        if self.checkBox_data_wystawienia.isChecked():
            date_from = self.dateEdit_data_wystawienia_od.date().toString("yyyy-MM-dd")
            date_to = self.dateEdit_data_wystawienia_do.date().toString("yyyy-MM-dd")
            if date_from != "2000-01-01" or date_to != QDate.currentDate().toString(
                "yyyy-MM-dd"
            ):
                self.search_clause_elements.append(
                    "data_wystawienia BETWEEN '{}' AND '{}'".format(date_from, date_to)
                )
        else:
            date_specific = self.dateEdit_data_wystawienia_konkretna.date().toString(
                "yyyy-MM-dd"
            )
            if date_specific != "2000-01-01":
                self.search_clause_elements.append(
                    "data_wystawienia = '{}'".format(date_specific)
                )

        ###### NUMER FV ######
        if self.lineEdit_numer_fv.text() != "":
            if self.radioButton_numer_FV_contain.isChecked():
                clause = "numer_fv LIKE '%{}%'".format(self.lineEdit_numer_fv.text())
            elif self.radioButton_numer_FV_not_contain.isChecked():
                clause = "numer_fv NOT LIKE '%{}%'".format(
                    self.lineEdit_numer_fv.text()
                )
            elif self.radioButton_numer_FV_equal.isChecked():
                clause = "numer_fv = '{}'".format(self.lineEdit_numer_fv.text())
            elif self.radioButton_numer_FV_different.isChecked():
                clause = "numer_fv != '{}'".format(self.lineEdit_numer_fv.text())
            self.search_clause_elements.append(clause)

        ###### SPRZEDAWCA ######
        if self.lineEdit_sprzedawca.text() != "":
            if self.radioButton_sprzedawca_contain.isChecked():
                clause = "sprzedawca LIKE '%{}%'".format(
                    self.lineEdit_sprzedawca.text()
                )
            elif self.radioButton_sprzedawca_not_contain.isChecked():
                clause = "sprzedawca NOT LIKE '%{}%'".format(
                    self.lineEdit_sprzedawca.text()
                )
            elif self.radioButton_sprzedawca_equal.isChecked():
                clause = "sprzedawca = '{}'".format(self.lineEdit_sprzedawca.text())
            elif self.radioButton_sprzedawca_different.isChecked():
                clause = "sprzedawca != '{}'".format(self.lineEdit_sprzedawca.text())
            self.search_clause_elements.append(clause)

        ###### KWOTA NETTO ######
        if self.checkBox_kwota_netto.isChecked():
            kwota_netto_from = self.doubleSpinBox_kwota_netto_od.value()
            kwota_netto_to = self.doubleSpinBox_kwota_netto_do.value()
            if kwota_netto_from != 0 or kwota_netto_to != 0:
                self.search_clause_elements.append(
                    "kwota_netto BETWEEN {} AND {}".format(
                        kwota_netto_from, kwota_netto_to
                    )
                )
        else:
            kwota_netto_specific = self.doubleSpinBox_kwota_netto_konkretna.value()
            if kwota_netto_specific != 0:
                self.search_clause_elements.append(
                    "kwota_netto = {}".format(kwota_netto_specific)
                )

        ###### KWOTA BRUTTO ######
        if self.checkBox_kwota_brutto.isChecked():
            kwota_brutto_from = self.doubleSpinBox_kwota_brutto_od.value()
            kwota_brutto_to = self.doubleSpinBox_kwota_brutto_do.value()
            if kwota_brutto_from != 0 or kwota_brutto_to != 0:
                self.search_clause_elements.append(
                    "kwota_brutto BETWEEN {} AND {}".format(
                        kwota_brutto_from, kwota_brutto_to
                    )
                )
        else:
            kwota_brutto_specific = self.doubleSpinBox_kwota_brutto_konkretna.value()
            if kwota_brutto_specific != 0:
                self.search_clause_elements.append(
                    "kwota_brutto = {}".format(kwota_brutto_specific)
                )

        ###### NUMER KONTA ######
        if self.lineEdit_nr_konta.text() != "":
            if self.radioButton_nr_konta_contain.isChecked():
                clause = "numer_konta_bankowego LIKE '%{}%'".format(
                    self.lineEdit_nr_konta.text()
                )
            elif self.radioButton_nr_konta_equal.isChecked():
                clause = "numer_konta_bankowego = '{}'".format(
                    self.lineEdit_nr_konta.text()
                )
            elif self.radioButton_nr_konta_start_on.isChecked():
                clause = "numer_konta_bankowego LIKE '{}%'".format(
                    self.lineEdit_nr_konta.text()
                )
            elif self.radioButton_nr_konta_end_on.isChecked():
                clause = "numer_konta_bankowego LIKE '%{}'".format(
                    self.lineEdit_nr_konta.text()
                )
            self.search_clause_elements.append(clause)

        ###### TERMIN PLATNOSCI ######
        if self.checkBox_termin_platnosci.isChecked():
            pay_date_from = self.dateEdit_termin_platnosci_od.date().toString(
                "yyyy-MM-dd"
            )
            pay_date_to = self.dateEdit_termin_platnosci_do.date().toString(
                "yyyy-MM-dd"
            )
            if (
                pay_date_from != "2000-01-01"
                or pay_date_to != QDate.currentDate().toString("yyyy-MM-dd")
            ):
                self.search_clause_elements.append(
                    "termin_platnosci BETWEEN '{}' AND '{}'".format(
                        pay_date_from, pay_date_to
                    )
                )
        else:
            pay_date_specific = (
                self.dateEdit_termin_platnosci_konkretna.date().toString("yyyy-MM-dd")
            )
            if pay_date_specific != "2000-01-01":
                self.search_clause_elements.append(
                    "termin_platnosci = '{}'".format(pay_date_specific)
                )

        self.populating_table()

    def evt_clear_search(self):
        self.checkBox_data_wystawienia.setChecked(True)
        self.checkBox_kwota_netto.setChecked(True)
        self.checkBox_kwota_brutto.setChecked(True)
        self.checkBox_termin_platnosci.setChecked(True)

        self.radioButton_numer_FV_contain.setChecked(True)
        self.radioButton_sprzedawca_contain.setChecked(True)
        self.radioButton_nr_konta_contain.setChecked(True)

        self.lineEdit_numer_fv.setText("")
        self.lineEdit_sprzedawca.setText("")
        self.lineEdit_nr_konta.setText("")

        self.dateEdit_data_wystawienia_konkretna.setDate(QDate(0, 0, 0))
        self.dateEdit_data_wystawienia_od.setDate(QDate(0, 0, 0))
        self.dateEdit_data_wystawienia_do.setDate(QDate.currentDate())

        self.doubleSpinBox_kwota_netto_konkretna.setValue(0)
        self.doubleSpinBox_kwota_netto_od.setValue(0)
        self.doubleSpinBox_kwota_netto_do.setValue(0)

        self.doubleSpinBox_kwota_brutto_konkretna.setValue(0)
        self.doubleSpinBox_kwota_brutto_od.setValue(0)
        self.doubleSpinBox_kwota_brutto_do.setValue(0)

        self.dateEdit_termin_platnosci_konkretna.setDate(QDate(0, 0, 0))
        self.dateEdit_termin_platnosci_od.setDate(QDate(0, 0, 0))
        self.dateEdit_termin_platnosci_do.setDate(QDate.currentDate())

        self.search_clause_elements = []
        self.populating_table()

    def evt_date_wystawienia(self, checked):
        self.dateEdit_data_wystawienia_konkretna.setVisible(not checked)
        self.label_data_wystawienia_od.setVisible(checked)
        self.dateEdit_data_wystawienia_od.setVisible(checked)
        self.label_data_wystawienia_do.setVisible(checked)
        self.dateEdit_data_wystawienia_do.setVisible(checked)

    def evt_kwota_netto(self, checked):
        self.doubleSpinBox_kwota_netto_konkretna.setVisible(not checked)
        self.label_kwota_netto_od.setVisible(checked)
        self.doubleSpinBox_kwota_netto_od.setVisible(checked)
        self.label_kwota_netto_do.setVisible(checked)
        self.doubleSpinBox_kwota_netto_do.setVisible(checked)

    def evt_kwota_brutto(self, checked):
        self.doubleSpinBox_kwota_brutto_konkretna.setVisible(not checked)
        self.label_kwota_brutto_od.setVisible(checked)
        self.doubleSpinBox_kwota_brutto_od.setVisible(checked)
        self.label_kwota_brutto_do.setVisible(checked)
        self.doubleSpinBox_kwota_brutto_do.setVisible(checked)

    def evt_termin_platnosci(self, checked):
        self.dateEdit_termin_platnosci_konkretna.setVisible(not checked)
        self.label_termin_platnosci_od.setVisible(checked)
        self.dateEdit_termin_platnosci_od.setVisible(checked)
        self.label_termin_platnosci_do.setVisible(checked)
        self.dateEdit_termin_platnosci_do.setVisible(checked)

    ### SQL ###
    def create_db_file_and_table_if_not_exists(self):
        ### FOLDER FOR PDF FILES ###
        if not os.path.exists(os.path.join(os.path.dirname(__file__), "data", "pdf")):
            os.makedirs(os.path.join(os.path.dirname(__file__), "data", "pdf"))

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        path = os.path.join(os.path.dirname(__file__), "data", "database.db")
        self.db.setDatabaseName(path)
        if self.db.open():
            self.query = QSqlQuery()
            if "faktury" not in self.db.tables():
                self.query.exec(
                    """CREATE TABLE IF NOT EXISTS faktury (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data_wystawienia TEXT,
                    numer_fv TEXT,
                    id_sprzedawcy INTEGER,
                    kwota_netto REAL,
                    kwota_brutto REAL,
                    numer_konta_bankowego TEXT,
                    status_fv BOOLEAN, 
                    termin_platnosci TEXT,
                    nazwa_pliku TEXT,
                    deleted BOOLEAN DEFAULT 0
                    )"""  ### status_fv - 0 - nieopłacona, 1 - opłacona
                )
                print(self.query.lastError().text())
            if "sprzedawcy" not in self.db.tables():
                self.query.exec(
                    """CREATE TABLE IF NOT EXISTS sprzedawcy (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nazwa TEXT,
                    nr_konta TEXT
                    )"""
                )
                print(self.query.lastError().text())
            if "samochody" not in self.db.tables():
                self.query.exec(
                    """
                    CREATE TABLE IF NOT EXISTS samochody (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    marka TEXT,
                    model TEXT,
                    data_zakupu TEXT,
                    nr_rejestracyjny TEXT,
                    firma TEXT,
                    pliki TEXT
                    )"""
                )
                print(self.query.lastError().text())
            if "przeglady" not in self.db.tables():
                self.query.exec(
                    """
                    CREATE TABLE IF NOT EXISTS przeglady (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_samochodu INTEGER,
                    data_przegladu TEXT,
                    okres_przegladu TEXT
                    )"""
                )
                print(self.query.lastError().text())
            if "ubezpieczenie" not in self.db.tables():
                self.query.exec(
                    """
                    CREATE TABLE IF NOT EXISTS ubezpieczenie (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_samochodu INTEGER,
                    data_zawarcia_ubezpieczenia TEXT,
                    okres_waznosci TEXT
                    )"""
                )
                print(self.query.lastError().text())
        else:
            QMessageBox.critical(
                self,
                "Błąd",
                "Nie udało się otworzyć bazy danych",
                QMessageBox.StandardButton.Ok,
            )

    def populating_table(self):
        # Clear the table.
        self.tableWidget.setRowCount(0)
        self.tableWidget.clearContents()
        if not self.is_logged:
            login = Login()
            login.exec()
            if login.login_entered:
                self.is_logged = True
            else:
                return
        # Create a query to select the data.
        elements = ["deleted = 0"]
        elements.extend(self.search_clause_elements)
        match self.show_all_unpaid_paid:
            case 1:
                elements.append("status_fv = 0")
            case 2:
                elements.append("status_fv = 1")
        if len(elements) > 0:
            where_clause = "WHERE " + " AND ".join(elements)
        else:
            where_clause = ""

        self.query = QSqlQuery()
        self.query.exec("SELECT id, nazwa FROM sprzedawcy")
        my_sellers_dict = {}
        while self.query.next():
            my_sellers_dict[self.query.value(0)] = self.query.value(1)
        self.query.exec(
            "SELECT faktury.id, data_wystawienia, numer_fv, nazwa as sprzedawca, kwota_netto, kwota_brutto, numer_konta_bankowego, status_fv, termin_platnosci FROM faktury LEFT JOIN sprzedawcy ON faktury.id_sprzedawcy = sprzedawcy.id {} ORDER BY {} {}".format(
                where_clause,
                self.sorting_column_name,
                "ASC" if self.sorting_ascending else "DESC",
            )
        )
        print(self.query.lastError().text())
        # Populate the table.
        while self.query.next():
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            for col in range(8):
                if col == 2:
                    self.tableWidget.setItem(
                        row,
                        col,
                        QTableWidgetItem(self.query.value("sprzedawca")),
                    )
                    continue
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

        #### CARS ####
        self.table_cars.setRowCount(0)
        self.table_cars.clearContents()
        self.query.exec("SELECT id, marka, model, nr_rejestracyjny FROM samochody")
        cars = {}
        while self.query.next():
            cars[self.query.value(0)] = [
                self.query.value(1),
                self.query.value(2),
                self.query.value(3),
            ]
        for car_id in cars.keys():
            # Przeglad
            self.query.exec(
                "SELECT data_przegladu, okres_przegladu FROM przeglady WHERE id_samochodu = {} ORDER BY data_przegladu DESC LIMIT 1".format(
                    car_id
                )
            )
            if self.query.next():
                data = self.query.value(0)
                okres = self.query.value(1)
                # convert data to date
                data = datetime.strptime(data, "%Y-%m-%d")
                # add okres to data
                data = data.replace(year=data.year + int(okres))
                # get today's date
                today = datetime.today()
                nastepny_przeglad_za_dni = (data - today).days
                cars[car_id].append(
                    "{}dni --- {}".format(nastepny_przeglad_za_dni, data.date())
                )
            else:
                cars[car_id].append("brak informacji")

            # Ubezpieczenie
            self.query.exec(
                "SELECT data_zawarcia_ubezpieczenia, okres_waznosci FROM ubezpieczenie WHERE id_samochodu = {} ORDER BY data_zawarcia_ubezpieczenia DESC, okres_waznosci DESC LIMIT 1".format(
                    car_id
                )
            )
            if self.query.next():
                data = self.query.value(0)
                okres = self.query.value(1)
                # convert data to date
                data = datetime.strptime(data, "%Y-%m-%d")
                # add okres to data
                data = data.replace(year=data.year + int(okres))
                # get today's date
                today = datetime.today()
                nastepne_ubezpieczenie_za_dni = (data - today).days
                cars[car_id].append(
                    "{}dni --- {}".format(nastepne_ubezpieczenie_za_dni, data.date())
                )
            else:
                cars[car_id].append("brak informacji")
        for car in cars.values():
            row = self.table_cars.rowCount()
            self.table_cars.insertRow(row)
            for col, value in enumerate(car):
                self.table_cars.setItem(row, col, QTableWidgetItem(str(value)))

    def finding_current_row_fv_data(self):
        if self.tableWidget.currentRow() == -1:
            return
        row = self.tableWidget.currentRow()
        self.query.prepare(
            "SELECT * from faktury WHERE data_wystawienia = :data_wystawienia AND numer_fv = :numer_fv AND kwota_netto = :kwota_netto AND kwota_brutto = :kwota_brutto AND numer_konta_bankowego = :numer_konta_bankowego AND termin_platnosci = :termin_platnosci"
        )
        self.query.bindValue(":data_wystawienia", self.tableWidget.item(row, 0).text())
        self.query.bindValue(":numer_fv", self.tableWidget.item(row, 1).text())
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
        return self.query

    ### SETUP CONNECTIONS ###
    def setup_connection(self):
        # REMEMBERS SYSTEM CONNECTIONS

        self.remember_system = Remember_system()
        self.remember_system.start()
        self.remember_system.show_not_paid.connect(self.show_not_paid)
        self.remember_system.get_data_not_paid_info.connect(self.set_not_paid_info)

        # ACTION CLICK CONNECTIONS

        self.action_faktury_Dodaj_FV.triggered.connect(self.evt_add_fv)
        self.action_faktury_open_pdf.triggered.connect(self.open_pdf_file)
        self.action_faktury_zaplac.triggered.connect(self.pay_for_invoice)
        self.action_faktury_edit.triggered.connect(self.evt_edit_invoice)
        self.action_faktury_delete.triggered.connect(self.evt_delete_invoice)
        self.action_faktury_settings.triggered.connect(self.evt_settings)

        self.action_faktury_search.triggered.connect(self.evt_search_fv)

        self.action_sortowanie_FV_domyslne.setChecked(True)
        self.action_sortowanie_FV_domyslne.triggered.connect(self.evt_sort_default)
        self.action_sortowanie_FV_Data_wystawienia.triggered.connect(
            self.evt_sort_data_wystawienia
        )
        self.action_sortowanie_FV_numer_FV.triggered.connect(self.evt_sort_numer_fv)
        self.action_sortowanie_FV_sprzedawca.triggered.connect(self.evt_sort_sprzedawca)
        self.action_sortowanie_FV_Kwota_netto.triggered.connect(
            self.evt_sort_kwota_netto
        )
        self.action_sortowanie_FV_Kwota_brutto.triggered.connect(
            self.evt_sort_kwota_brutto
        )
        self.action_sortowanie_FV_numer_konta_bankowego.triggered.connect(
            self.evt_sort_bank_account_number
        )
        self.action_sortowanie_FV_Status_FV.triggered.connect(self.evt_sort_status_fv)
        self.action_sortowanie_FV_termin_platnosci.triggered.connect(
            self.evt_sort_termin_platnosci
        )

        self.action_sortowanie_FV_rosnaco.setChecked(True)
        self.action_sortowanie_FV_rosnaco.triggered.connect(self.evt_sort_ascending)
        self.action_sortowanie_FV_malejaco.triggered.connect(self.evt_sort_descending)

        self.action_wyswietlanie_FV_Wszystkie.setChecked(True)
        self.action_wyswietlanie_FV_Wszystkie.triggered.connect(self.evt_show_all)
        self.action_wyswietlanie_FV_Nieoplacone.triggered.connect(self.evt_show_unpaid)
        self.action_wyswietlanie_FV_Oplacone.triggered.connect(self.evt_show_paid)

        # ACTION CLICK COLUMN SORTING
        self.tableWidget.horizontalHeader().sectionClicked.connect(self.sorting)

        # TABLE WIDGET CLICK CONNECTIONS
        self.tableWidget.cellDoubleClicked.connect(self.evt_table_double_clicked)

        # CHANGE TAB WIDGET CONNECTIONS
        self.tabWidget.currentChanged.connect(self.evt_tab_changed)

        # CARS
        self.action_samochody_dodaj_Samochod.triggered.connect(self.evt_add_car)
        self.action_samochody_dodaj_Przeglad.triggered.connect(self.evt_add_review)
        self.action_samochody_dodaj_Ubezpieczenie.triggered.connect(
            self.evt_add_insurance
        )
        self.action_samochody_karta_Pojazdu.triggered.connect(
            self.evt_table_cars_double_clicked
        )

        self.table_cars.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table_cars.cellDoubleClicked.connect(self.evt_table_cars_double_clicked)

    ### TABLE WIDGET ###

    def set_table_headers(self):
        self.tableWidget.setHorizontalHeaderLabels(
            [
                "Data wystawienia",
                "Numer FV",
                "Sprzedawca",
                "Kwota netto",
                "Kwota brutto",
                "Numer konta",
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

    def set_cars_table_headers(self):
        self.table_cars.setHorizontalHeaderLabels(
            [
                "Marka",
                "Model",
                "Numer rejestracyjny",
                "Następny przegląd",
                "Koniec ubezpieczenia",
            ]
        )
        self.table_cars.setColumnWidth(0, 150)
        self.table_cars.setColumnWidth(1, 150)
        self.table_cars.setColumnWidth(2, 150)
        self.table_cars.setColumnWidth(3, 250)
        self.table_cars.setColumnWidth(4, 250)

    def get_column_sql_name(self, index):
        match index:
            case -1:
                return "faktury.id"
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
        if index != -1:
            text = self.tableWidget.horizontalHeaderItem(index).text()
            self.tableWidget.horizontalHeaderItem(index).setText(
                text + " ▼" if self.sorting_ascending else text + " ▲"
            )

    def evt_table_double_clicked(self, row, column):
        if column == 6:
            self.pay_for_invoice()
        else:
            self.open_pdf_file()

    def pay_for_invoice(self):
        data = self.finding_current_row_fv_data()
        if not data:
            return
        if data.value("status_fv") == 0:
            paymant = Payment(data.value("id"))
            paymant.exec()
            if paymant.czy_zaplacono:
                self.populating_table()
        else:
            QMessageBox.warning(
                self,
                "Błąd",
                "Nie można zapłacić za fakturę, która została już opłacona",
                QMessageBox.StandardButton.Ok,
            )

    def open_pdf_file(self):
        data = self.finding_current_row_fv_data()
        if not data:
            return
        file = data.value("nazwa_pliku")
        if ".pdf" in file:
            file = os.path.join(os.path.dirname(__file__), "data", "pdf", file)
            try:
                open_file(file)
            except:
                QMessageBox.warning(
                    self,
                    "Błąd",
                    "Nie można otworzyć pliku. Prawdopodobnie plik nie istnieje, nie jest w formacie PDF lub jest pusty",
                    QMessageBox.StandardButton.Ok,
                )
        else:
            QMessageBox.warning(
                self,
                "Błąd",
                "Nie można otworzyć pliku. Prawdopodobnie plik nie istnieje, nie jest w formacie PDF lub jest pusty",
                QMessageBox.StandardButton.Ok,
            )

    def show_not_paid(self):
        self.show_all_unpaid_paid = 1
        self.populating_table()
        self.show()
        self.activateWindow()

    def set_not_paid_info(self):
        overdue = 0
        today = 0
        tommorow = 0
        more_days = 0

        self.query.exec(
            "SELECT termin_platnosci FROM faktury WHERE deleted = 0 AND status_fv = 0"
        )

        while self.query.next():
            if QDate.currentDate().toString("yyyy-MM-dd") > self.query.value(0):
                overdue += 1
            elif QDate.currentDate().toString("yyyy-MM-dd") == self.query.value(0):
                today += 1
            elif QDate.currentDate().addDays(1).toString(
                "yyyy-MM-dd"
            ) == self.query.value(0):
                tommorow += 1
            # do 2 tygodni
            elif QDate.currentDate().addDays(14).toString(
                "yyyy-MM-dd"
            ) >= self.query.value(0):
                more_days += 1
        if not overdue and not today and not tommorow and not more_days:
            return
        nieoplacone = Nieoplacone(overdue, today, tommorow, more_days)
        nieoplacone.exec()
        if nieoplacone.what_to_do == 1:
            self.show_not_paid()
        elif nieoplacone.what_to_do == 2:
            self.wait = Worker_wait_x_min()
            self.wait.time = 30
            self.wait.start()
            self.wait.waited_emit.connect(self.set_not_paid_info)

    def get_current_row_car_id(self):
        id_samochodu = None
        current_row = self.table_cars.currentRow()
        if current_row != -1:
            nr_rejestracyjny = self.table_cars.item(current_row, 2).text()
            self.query.exec(
                "SELECT id FROM samochody WHERE nr_rejestracyjny = '"
                + nr_rejestracyjny
                + "'"
            )
            self.query.next()
            id_samochodu = self.query.value(0)
        return id_samochodu

    ### EVENT HANDLERS ###
    def evt_table_cars_double_clicked(self, row=None, column=None):
        id_samochodu = self.get_current_row_car_id()
        if id_samochodu == -1 or not id_samochodu:
            QMessageBox.warning(
                self,
                "Błąd",
                "Nie wybrano pojazdu",
                QMessageBox.StandardButton.Ok,
            )
            return
        window = Dodawanie_Edytowanie_Samochodu(id_samochodu)
        window.exec()
        self.populating_table()

    def unchecked_sort(self, index):
        self.action_sortowanie_FV_domyslne.setChecked(False)
        self.action_sortowanie_FV_Data_wystawienia.setChecked(False)
        self.action_sortowanie_FV_numer_FV.setChecked(False)
        self.action_sortowanie_FV_sprzedawca.setChecked(False)
        self.action_sortowanie_FV_Kwota_netto.setChecked(False)
        self.action_sortowanie_FV_Kwota_brutto.setChecked(False)
        self.action_sortowanie_FV_numer_konta_bankowego.setChecked(False)
        self.action_sortowanie_FV_Status_FV.setChecked(False)
        self.action_sortowanie_FV_termin_platnosci.setChecked(False)

        match index:
            case -1:
                self.action_sortowanie_FV_domyslne.setChecked(True)
            case 0:
                self.action_sortowanie_FV_Data_wystawienia.setChecked(True)
            case 1:
                self.action_sortowanie_FV_numer_FV.setChecked(True)
            case 2:
                self.action_sortowanie_FV_sprzedawca.setChecked(True)
            case 3:
                self.action_sortowanie_FV_Kwota_netto.setChecked(True)
            case 4:
                self.action_sortowanie_FV_Kwota_brutto.setChecked(True)
            case 5:
                self.action_sortowanie_FV_numer_konta_bankowego.setChecked(True)
            case 6:
                self.action_sortowanie_FV_Status_FV.setChecked(True)
            case 7:
                self.action_sortowanie_FV_termin_platnosci.setChecked(True)

    def change_sort_order(self):
        self.action_sortowanie_FV_rosnaco.setChecked(self.sorting_ascending)
        self.action_sortowanie_FV_malejaco.setChecked(not self.sorting_ascending)

    def unchecked_display(self):
        self.action_wyswietlanie_FV_Wszystkie.setChecked(False)
        self.action_wyswietlanie_FV_Nieoplacone.setChecked(False)
        self.action_wyswietlanie_FV_Oplacone.setChecked(False)

    def evt_tab_changed(self, index):
        if index == 0:
            self.toolBar.clear()
            self.toolBar.addAction(self.action_faktury_Dodaj_FV)
            self.toolBar.addAction(self.action_faktury_open_pdf)
            self.toolBar.addAction(self.action_faktury_zaplac)
            self.toolBar.addSeparator()
            self.toolBar.addAction(self.action_faktury_search)
            self.toolBar.addSeparator()
            self.toolBar.addAction(self.action_wyswietlanie_FV_Wszystkie)
            self.toolBar.addAction(self.action_wyswietlanie_FV_Nieoplacone)
            self.toolBar.addSeparator()
            self.toolBar.addAction(self.action_sortowanie_FV_domyslne)
            self.toolBar.addAction(self.action_sortowanie_FV_rosnaco)
            self.toolBar.addAction(self.action_sortowanie_FV_malejaco)

            self.menuSamochody.setEnabled(False)
            self.menuFaktury.setEnabled(True)
            self.menuSortowanie_FV.setEnabled(True)
            self.menuWyswietlanie_FV.setEnabled(True)
        elif index == 1:
            self.toolBar.clear()
            self.toolBar.addAction(self.action_samochody_karta_Pojazdu)
            self.toolBar.addSeparator()
            self.toolBar.addAction(self.action_samochody_dodaj_Samochod)
            self.toolBar.addAction(self.action_samochody_dodaj_Przeglad)
            self.toolBar.addAction(self.action_samochody_dodaj_Ubezpieczenie)

            self.menuFaktury.setEnabled(False)
            self.menuSortowanie_FV.setEnabled(False)
            self.menuWyswietlanie_FV.setEnabled(False)
            self.menuSamochody.setEnabled(True)

    def evt_add_fv(self):
        new_fv = Dodawanie_Edytowanie_Faktury()
        new_fv.exec()
        self.populating_table()

    def evt_edit_invoice(self):
        data = self.finding_current_row_fv_data()
        edit = Dodawanie_Edytowanie_Faktury(data.value("id"))
        edit.exec()
        self.populating_table()

    def evt_delete_invoice(self):
        data = self.finding_current_row_fv_data()
        usun = QMessageBox()
        usun.setWindowTitle("Usuwanie faktury")
        usun.setText("Czy na pewno chcesz usunąć fakturę?")
        usun.addButton("Tak", QMessageBox.ButtonRole.YesRole)
        usun.addButton("Nie", QMessageBox.ButtonRole.NoRole)
        usun.exec()
        if usun.clickedButton().text() == "Tak":
            self.query.exec(
                "UPDATE faktury SET deleted = 1 WHERE id = " + str(data.value("id"))
            )
            print(self.query.lastError().text())
            self.populating_table()

    def evt_settings(self):
        settings = Settings()
        settings.exec()

        self.remember_system.terminate()
        self.remember_system = Remember_system()
        self.remember_system.start()
        self.remember_system.show_not_paid.connect(self.show_not_paid)
        self.remember_system.get_data_not_paid_info.connect(self.set_not_paid_info)

    def evt_sort_default(self):
        self.sorting(-1)

    def evt_sort_data_wystawienia(self):
        self.sorting(0)

    def evt_sort_numer_fv(self):
        self.sorting(1)

    def evt_sort_sprzedawca(self):
        self.sorting(2)

    def evt_sort_kwota_netto(self):
        self.sorting(3)

    def evt_sort_kwota_brutto(self):
        self.sorting(4)

    def evt_sort_bank_account_number(self):
        self.sorting(5)

    def evt_sort_status_fv(self):
        self.sorting(6)

    def evt_sort_termin_platnosci(self):
        self.sorting(7)

    def evt_sort_descending(self):
        if self.sorting_ascending == True:
            self.sorting(self.sort_index)
        else:
            self.action_sortowanie_FV_malejaco.setChecked(True)

    def evt_sort_ascending(self):
        if self.sorting_ascending == False:
            self.sorting(self.sort_index)
        else:
            self.action_sortowanie_FV_rosnaco.setChecked(True)

    def evt_show_all(self):
        self.unchecked_display()
        self.action_wyswietlanie_FV_Wszystkie.setChecked(True)
        self.show_all_unpaid_paid = 0
        self.populating_table()

    def evt_show_unpaid(self):
        self.unchecked_display()
        self.action_wyswietlanie_FV_Nieoplacone.setChecked(True)
        self.show_all_unpaid_paid = 1
        self.populating_table()

    def evt_show_paid(self):
        self.unchecked_display()
        self.action_wyswietlanie_FV_Oplacone.setChecked(True)
        self.show_all_unpaid_paid = 2
        self.populating_table()

    def evt_add_car(self):
        window = Dodawanie_Edytowanie_Samochodu()
        window.exec()
        self.populating_table()

    def evt_add_insurance(self):
        id_samochodu = self.get_current_row_car_id()

        window = DodawanieOCAC(id_samochodu)
        window.exec()
        self.populating_table()

    def evt_add_review(self):
        id_samochodu = self.get_current_row_car_id()

        window = DodawaniePrzegladu(id_samochodu)
        window.exec()
        self.populating_table()

    ### CLOSE WINDOW ###
    def setup_tray_icon(self):
        # create tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("ikony/add.png"))
        self.tray_icon.setToolTip("Faktury")
        # show icon name on mouse hover

        # add menu
        self.menu = QMenu()
        self.menu.addAction("Pokaż")
        self.menu.addAction("Dodaj fakturę")
        self.menu.addAction("Zamknij")
        self.tray_icon.setContextMenu(self.menu)
        self.menu.triggered.connect(self.menu_triggered)
        # on mouse right click
        self.tray_icon.activated.connect(self.tray_activation)
        self.tray_icon.show()

    def tray_activation(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isHidden():
                self.show()
                self.populating_table()
            else:
                self.hide()

    def menu_triggered(self, action):
        if action.text() == "Zamknij":
            sys.exit()
        elif action.text() == "Pokaż":
            self.show()
            self.populating_table()
        elif action.text() == "Dodaj fakturę":
            self.show()
            new_fv = Dodawanie_Edytowanie_Faktury()
            new_fv.exec()
            self.hide()

    def closeEvent(self, event):
        self.tray_icon.show()
        self.is_logged = False
        event.ignore()
        self.hide()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
