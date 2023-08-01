from layout.dodawanie_samochodu_ui import Ui_Dialog
from PyQt6.QtWidgets import *
from PyQt6.QtSql import *
from PyQt6.QtCore import *
import os, shutil
from openfile import open_file


class Dodawanie_Edytowanie_Samochodu(QDialog, Ui_Dialog):
    def __init__(self, id=None):
        super(Dodawanie_Edytowanie_Samochodu, self).__init__()
        self.setupUi(self)
        self.id = id

        self.setup_data()
        if id:
            self.setWindowTitle("Karta pojazdu")
            self.btn_submit.setText("Zapisz")
            self.load_files_and_data()

        self.btn_submit.clicked.connect(self.evt_submit)
        self.btn_cancel.clicked.connect(self.close)
        self.toolbtn_add_file.clicked.connect(self.evt_add_file)
        self.date_edit_data_zakupu.setDate(QDate.currentDate())
        self.btn_submit.setDefault(True)
        self.setLayout(self.verticalLayout)
        self.resize(self.sizeHint())

    def setup_data(self):
        if not QSqlDatabase.database().isValid():
            self.db = QSqlDatabase.addDatabase("QSQLITE")
            path = os.path.join(os.path.dirname(__file__), "data", "database.db")
            self.db.setDatabaseName(path)
            self.db.open()
        else:
            self.db = QSqlDatabase.database()
        self.query = QSqlQuery()

    def load_files_and_data(self):
        self.query.exec(
            "SELECT pliki, marka, model, nr_rejestracyjny FROM samochody WHERE id = {}".format(
                self.id
            )
        )
        self.query.next()
        files = self.query.value(0)
        self.line_edit_marka.setText(self.query.value(1))
        self.line_edit_model.setText(self.query.value(2))
        self.line_edit_nr_rejestracyjny.setText(self.query.value(3))
        if not files:
            return
        files = files.split(" || ")
        for file in files:
            prefix_len = len(str(self.id)) + 1
            file_name = file[prefix_len:]  # remove prefix
            file_name = "".join(file_name.split(".")[:-1])  # remove extension
            file = os.path.join(os.path.dirname(__file__), "data", "car_files", file)
            self.evt_add_file(file_name, file)

    def evt_add_file(self, file_name=None, file_path=None):
        row_count = self.grid_layout_files.rowCount()

        btn_open_file = QPushButton("Zobacz plik")

        line_edit_name = QLineEdit()
        line_edit_name.setPlaceholderText("Opis pliku")
        line_edit_path = QLineEdit()
        line_edit_path.setReadOnly(True)
        toolbtn_chose_file = QToolButton()
        toolbtn_chose_file.setText("...")

        toolbtn_remove = QToolButton()
        toolbtn_remove.setText("X")

        if file_name:
            line_edit_name.setText(file_name)
        if file_path:
            line_edit_path.setText(file_path)

        self.grid_layout_files.addWidget(btn_open_file, row_count, 0)
        self.grid_layout_files.addWidget(line_edit_name, row_count, 1)
        self.grid_layout_files.addWidget(line_edit_path, row_count, 2)
        self.grid_layout_files.addWidget(toolbtn_chose_file, row_count, 3)
        self.grid_layout_files.addWidget(toolbtn_remove, row_count, 4)

        btn_open_file.clicked.connect(lambda: self.evt_open_file(line_edit_path))
        toolbtn_chose_file.clicked.connect(lambda: self.evt_chose_file(line_edit_path))
        toolbtn_remove.clicked.connect(lambda: self.evt_remove_file(row_count))

        self.resize(self.sizeHint())

    def evt_open_file(self, line_edit_path):
        path = line_edit_path.text()
        if path:
            open_file(path)
        else:
            QMessageBox.critical(
                self, "Błąd", "Nie dodano pliku", QMessageBox.StandardButton.Ok
            )

    def evt_chose_file(self, line_edit_path):
        path = QFileDialog.getOpenFileName(self, "Wybierz plik", "", "")
        if path[0]:
            line_edit_path.setText(path[0])

    def evt_remove_file(self, row_count):
        # ask
        answer = QMessageBox()
        answer.setIcon(QMessageBox.Icon.Question)
        answer.setWindowTitle("Usuwanie pliku")
        answer.setText("Czy na pewno chcesz usunąć plik?")
        # add btn Tak and Nie
        answer.addButton("Tak", QMessageBox.ButtonRole.YesRole)
        answer.addButton("Nie", QMessageBox.ButtonRole.NoRole)
        answer.exec()

        if answer.clickedButton().text() == "Nie":
            return

        for i in range(5):
            item = self.grid_layout_files.itemAtPosition(row_count, i)
            self.grid_layout_files.removeItem(
                self.grid_layout_files.itemAtPosition(row_count, i)
            )
            if item:
                item.widget().deleteLater()

        self.resize(self.sizeHint())

    def evt_submit(self):
        all_nr_rejestracyjny = []
        self.query.exec("SELECT nr_rejestracyjny FROM samochody")
        while self.query.next():
            all_nr_rejestracyjny.append(self.query.value(0))

        marka = self.line_edit_marka.text()
        model = self.line_edit_model.text()
        data_zakupu = self.date_edit_data_zakupu.date().toString("yyyy-MM-dd")
        nr_rejestracyjny = self.line_edit_nr_rejestracyjny.text().upper()
        firma = self.combo_box_firma.currentText()

        all_files = []

        for i in range(1, self.grid_layout_files.rowCount()):
            try:
                file_name = self.grid_layout_files.itemAtPosition(i, 1).widget().text()
                path = self.grid_layout_files.itemAtPosition(i, 2).widget().text()
            except:
                continue
            if path:
                all_files.append((file_name, path))

        if (
            not marka
            or not model
            or not data_zakupu
            or not nr_rejestracyjny
            or not firma
        ):
            QMessageBox.warning(
                self,
                "Błąd",
                "Uzupełnij wszystkie pola",
                QMessageBox.StandardButton.Ok,
            )
            return None
        if not self.id and nr_rejestracyjny in all_nr_rejestracyjny:
            QMessageBox.warning(
                self,
                "Błąd",
                "Samochód o podanym numerze rejestracyjnym już istnieje",
                QMessageBox.StandardButton.Ok,
            )
            return None

        if not os.path.exists(
            os.path.join(os.path.dirname(__file__), "data", "car_files")
        ):
            os.mkdir(os.path.join(os.path.dirname(__file__), "data", "car_files"))

        files_names = []

        if not self.id:
            try:
                self.query.exec("SELECT id FROM samochody ORDER BY id DESC LIMIT 1")
                car_id = self.query.next()
                car_id = self.query.value(0)
                car_id += 1
            except:
                car_id = 1
        else:
            car_id = self.id
        for file_name, file_path in all_files:
            extension = file_path.split(".")[-1]
            file_name = str(car_id) + "_" + file_name
            file_name += "." + extension
            files_names.append(file_name)
            try:
                shutil.copy(
                    file_path,
                    os.path.join(
                        os.path.dirname(__file__), "data", "car_files", file_name
                    ),
                )
            except shutil.SameFileError:
                pass

        files_str = " || ".join(files_names)

        if self.id:
            self.query.exec(
                "UPDATE samochody SET marka = '{}', model = '{}', data_zakupu = '{}', nr_rejestracyjny = '{}', firma = '{}', pliki='{}' WHERE id = {}".format(
                    marka,
                    model,
                    data_zakupu,
                    nr_rejestracyjny,
                    firma,
                    files_str,
                    self.id,
                )
            )
        else:
            self.query.exec(
                "INSERT INTO samochody (marka, model, data_zakupu, nr_rejestracyjny, firma, pliki) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(
                    marka, model, data_zakupu, nr_rejestracyjny, firma, files_str
                )
            )
        self.close()
