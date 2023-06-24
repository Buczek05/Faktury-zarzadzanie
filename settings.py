from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from layout.ustawienia_ui import Ui_Dialog
from add_remember import Add_Remember
import json


class Settings(QDialog, Ui_Dialog):
    def __init__(self):
        super(Settings, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Ustawienia")
        self.setLayout(self.main_layout)
        self.powiadomienia.setLayout(self.powiadomienia_main_layout)

        self.powiadomienia_table.setColumnWidth(0, 30)
        self.powiadomienia_table.setColumnWidth(1, 30)
        self.powiadomienia_table.setColumnWidth(2, 30)
        self.powiadomienia_table.setColumnWidth(3, 30)
        self.powiadomienia_table.setColumnWidth(4, 30)
        self.powiadomienia_table.setColumnWidth(5, 30)
        self.powiadomienia_table.setColumnWidth(6, 30)
        self.powiadomienia_table.setColumnWidth(7, 60)

        self.powiadomienia_table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        # switch off clickable column
        self.powiadomienia_table.horizontalHeader().setSectionsClickable(False)
        # switch off row
        self.powiadomienia_table.verticalHeader().setVisible(False)
        # switch off edit
        self.powiadomienia_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.powiadomienia_add.clicked.connect(self.evt_add_remember)
        self.powiadomienia_delete.clicked.connect(self.evt_delete_remember)

        self.populating_notification_table()

    def evt_add_remember(self):
        Add_Remember().exec()
        self.populating_notification_table()

    def evt_delete_remember(self):
        current_row = self.powiadomienia_table.currentRow()
        if current_row == -1:
            QMessageBox.warning(
                self,
                "Błąd",
                "Nie wybrano przypomnienia",
                QMessageBox.StandardButton.Ok,
            )
            return

        try:
            data = json.load(open("data/remember_data.json", "r"))
        except:
            data = []
        time_to_delete = self.powiadomienia_table.item(current_row, 7).text()
        new_data = []
        for i in range(len(data)):
            if data[i][1] != time_to_delete:
                new_data.append(data[i])
        print(new_data)
        with open("data/remember_data.json", "w") as f:
            json.dump(new_data, f)
        self.populating_notification_table()

    def populating_notification_table(self):
        self.powiadomienia_table.clearContents()
        try:
            data = json.load(open("data/remember_data.json", "r"))
        except:
            data = []
        # collect same time in one list
        new_data = []
        for i in range(len(data)):
            if i == 0:
                new_data.append([data[i]])
            else:
                for j in range(len(new_data)):
                    if data[i][1] == new_data[j][0][1]:
                        new_data[j].append(data[i])
                        break
                    elif j == len(new_data) - 1:
                        new_data.append([data[i]])
        # sort by time
        new_data.sort(key=lambda x: x[0][1])
        # populate table
        self.powiadomienia_table.setRowCount(len(new_data))
        for i in range(len(new_data)):
            time = QTableWidgetItem(new_data[i][0][1])
            time.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.powiadomienia_table.setItem(i, 7, time)
            for day, time in new_data[i]:
                match day:
                    case "Monday":
                        # set bird icon
                        self.powiadomienia_table.setItem(i, 0, QTableWidgetItem("✓"))
                    case "Tuesday":
                        self.powiadomienia_table.setItem(i, 1, QTableWidgetItem("✓"))
                    case "Wednesday":
                        self.powiadomienia_table.setItem(i, 2, QTableWidgetItem("✓"))
                    case "Thursday":
                        self.powiadomienia_table.setItem(i, 3, QTableWidgetItem("✓"))
                    case "Friday":
                        self.powiadomienia_table.setItem(i, 4, QTableWidgetItem("✓"))
                    case "Saturday":
                        self.powiadomienia_table.setItem(i, 5, QTableWidgetItem("✓"))
                    case "Sunday":
                        self.powiadomienia_table.setItem(i, 6, QTableWidgetItem("✓"))


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = Settings()
    window.show()
    sys.exit(app.exec())
