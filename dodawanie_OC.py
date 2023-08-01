from layout.dodawanie_oc_ac_ui import Ui_Dialog
from PyQt6.QtWidgets import *
from PyQt6.QtSql import *
from PyQt6.QtCore import *
import os


class DodawanieOCAC(QDialog, Ui_Dialog):
    def __init__(self, id_pojazdu=None):
        super(DodawanieOCAC, self).__init__()
        self.setupUi(self)
        self.id_pojazdu = id_pojazdu

        self.btn_submit.clicked.connect(self.evt_submit)
        self.btn_cancel.clicked.connect(self.close)
        self.btn_submit.setDefault(True)
        self.date_edit_data_zawarcia_ubezpieczenia.setDate(QDate.currentDate())
        self.setLayout(self.verticalLayout)
        self.setup_data()
        if id_pojazdu:
            self.combo_box_samochod.setCurrentText(self.cars[id_pojazdu])

    def setup_data(self):
        if not QSqlDatabase.database().isValid():
            self.db = QSqlDatabase.addDatabase("QSQLITE")
            path = os.path.join(os.path.dirname(__file__), "data", "database.db")
            self.db.setDatabaseName(path)
            self.db.open()
        else:
            self.db = QSqlDatabase.database()
        self.query = QSqlQuery()

        self.cars = {}
        self.query.exec("SELECT id, marka, model, nr_rejestracyjny FROM samochody")
        while self.query.next():
            self.cars[
                self.query.value(0)
            ] = f"{self.query.value(1)} {self.query.value(2)} - {self.query.value(3)}"
        self.combo_box_samochod.clear()
        self.combo_box_samochod.addItems(self.cars.values())

    def evt_submit(self):
        id_samochodu = list(self.cars.keys())[
            list(self.cars.values()).index(self.combo_box_samochod.currentText())
        ]
        data_zawarcia = self.date_edit_data_zawarcia_ubezpieczenia.date().toString(
            "yyyy-MM-dd"
        )
        okres = self.combo_box_okres.currentIndex() + 1

        if not data_zawarcia or not okres:
            QMessageBox.warning(
                self,
                "Błąd",
                "Uzupełnij wszystkie pola",
                QMessageBox.StandardButton.Ok,
            )
            return None

        # Sprawdz czy nie ma ubezpieczenia tego dnia
        self.query.exec(
            f"""SELECT id FROM ubezpieczenie WHERE id_samochodu = {id_samochodu} AND data_zawarcia_ubezpieczenia = "{data_zawarcia}" """
        )
        if self.query.next():
            QMessageBox.warning(
                self,
                "Błąd",
                "Ubezpieczenie tego dnia już istnieje",
                QMessageBox.StandardButton.Ok,
            )
            return None

        self.query.prepare(
            """INSERT INTO ubezpieczenie (id_samochodu, data_zawarcia_ubezpieczenia, okres_waznosci) VALUES (?, ?, ?)"""
        )
        self.query.addBindValue(id_samochodu)
        self.query.addBindValue(data_zawarcia)
        self.query.addBindValue(okres)
        self.query.exec()
        print(self.query.lastError())

        self.close()
