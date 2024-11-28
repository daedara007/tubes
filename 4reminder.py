import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from datetime import datetime

tf = ""
token = "data/" + (tf) + "tasks.txt"

class ReminderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reminder")
        self.setGeometry(100, 100, 650, 400)

        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nama Tugas", "Mata Kuliah", "Deadline", "Status"])

        self.table.setColumnWidth(0, 200)  # kolom nama Tugas
        self.table.setColumnWidth(1, 100)  # kolom mata Kuliah
        self.table.setColumnWidth(2, 150)  # kolom deadline
        self.table.setColumnWidth(3, 150)  # kolom status

        layout.addWidget(self.table)
        self.setLayout(layout)

        self.load_tasks()

    def load_tasks(self):
        tasks = []
        with open(token, 'r') as file:
            for line in file:
                name, subject, deadline, status = line.strip().split(',')
                if status != "Selesai":  # Hanya ambil yang belum selesai
                    tasks.append((name, subject, deadline, status))

        # Urutkan berdasarkan deadline
        tasks.sort(key=lambda x: datetime.strptime(x[2], "%Y-%m-%d"))

        self.table.setRowCount(len(tasks))
        for row, (name, subject, deadline, status) in enumerate(tasks):
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(subject))
            self.table.setItem(row, 2, QTableWidgetItem(deadline))
            self.table.setItem(row, 3, QTableWidgetItem(status))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ReminderApp()
    window.show()
    sys.exit(app.exec_())