from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from nieoplacone import Nieoplacone
import time, json, os, sys


class Remember_system(QThread):
    show_not_paid = pyqtSignal()
    get_data_not_paid_info = pyqtSignal()

    def run(self):
        while True:
            remember_data = json.load(open("data/remember_data.json", "r"))
            self.this_day_times = []
            for week_day, stime in remember_data:
                if week_day == QDate.currentDate().toString("dddd"):
                    self.this_day_times.append(stime)
            self.this_day_times.sort()
            for stime in self.this_day_times:
                if stime > QTime.currentTime().toString("hh:mm"):
                    notification_time = QTime.fromString(stime, "hh:mm")
                    current_time = QTime.currentTime()
                    remaining_time = current_time.msecsTo(notification_time)
                    time.sleep(remaining_time / 1000)
                    self.check_time()

    def check_time(self):
        self.get_data_not_paid_info.emit()


class Worker_wait_x_min(QThread):
    waited_emit = pyqtSignal()
    time = 0

    def run(self):
        time.sleep(self.time)
        self.waited_emit.emit()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    remember_system = Remember_system()
    remember_system.start()
    sys.exit(app.exec())
