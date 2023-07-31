from PyQt6.QtWidgets import *
from layout.add_remember_ui import Ui_Dialog
import json


class Add_Remember(QDialog, Ui_Dialog):
    def __init__(self):
        super(Add_Remember, self).__init__()
        self.setupUi(self)
        self.setLayout(self.main_layout)
        self.setWindowTitle("Dodaj przypomnienie")
        self.setLayout(self.verticalLayout)
        self.Save.clicked.connect(self.evt_save)
        self.Cancel.clicked.connect(self.evt_cancel)

    def evt_save(self):
        self.my_save_list = []
        if self.Monday.isChecked():
            self.my_save_list.append(["Monday", self.timeEdit.time().toString("hh:mm")])
        if self.Tuesday.isChecked():
            self.my_save_list.append(
                ["Tuesday", self.timeEdit.time().toString("hh:mm")]
            )
        if self.Wednesday.isChecked():
            self.my_save_list.append(
                ["Wednesday", self.timeEdit.time().toString("hh:mm")]
            )
        if self.Thursday.isChecked():
            self.my_save_list.append(
                ["Thursday", self.timeEdit.time().toString("hh:mm")]
            )
        if self.Friday.isChecked():
            self.my_save_list.append(["Friday", self.timeEdit.time().toString("hh:mm")])
        if self.Saturday.isChecked():
            self.my_save_list.append(
                ["Saturday", self.timeEdit.time().toString("hh:mm")]
            )
        if self.Sunday.isChecked():
            self.my_save_list.append(["Sunday", self.timeEdit.time().toString("hh:mm")])
        if self.my_save_list == []:
            QMessageBox.warning(
                self, "Błąd", "Nie wybrano dnia tygodnia", QMessageBox.StandardButton.Ok
            )
            return
        try:
            self.data = json.load(open("data/remember_data.json", "r"))
        except:
            self.data = []
        self.data.extend(self.my_save_list)
        # remove duplicated lists
        self.data = list(set(map(tuple, self.data)))
        with open("data/remember_data.json", "w") as f:
            json.dump(self.data, f)
        self.close()

    def evt_cancel(self):
        self.close()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    dlg = Add_Remember()
    dlg.show()
    sys.exit(app.exec())
