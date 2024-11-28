import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDateEdit, QComboBox, QMessageBox
from PyQt5.QtCore import QDate

tf = "wak"
token = "data/" + (tf) + "tasks.txt"

class TaskManager(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Task Manager')
        self.setGeometry(100, 100, 300, 250)

        layout = QVBoxLayout()

        # Input untuk nama tugas
        self.task_name_label = QLabel('Nama Tugas:')
        self.task_name_input = QLineEdit()
        layout.addWidget(self.task_name_label)
        layout.addWidget(self.task_name_input)

        # Input untuk nama mata kuliah
        self.course_name_label = QLabel('Nama Mata Kuliah:')
        self.course_name_input = QLineEdit()
        layout.addWidget(self.course_name_label)
        layout.addWidget(self.course_name_input)

        # Input untuk deadline
        self.deadline_label = QLabel('Deadline:')
        self.deadline_input = QDateEdit()
        self.deadline_input.setCalendarPopup(True)
        self.deadline_input.setDate(QDate.currentDate()) #buat defaultnya hari ini
        layout.addWidget(self.deadline_label)
        layout.addWidget(self.deadline_input)

        # Input untuk status tugas
        self.status_label = QLabel('Status Tugas:')
        self.status_input = QComboBox()
        self.status_input.addItems(['Belum Dikerjakan', 'Sedang Dikerjakan', 'Selesai'])
        layout.addWidget(self.status_label)
        layout.addWidget(self.status_input)

        # Tombol untuk menambahkan tugas
        self.add_task_button = QPushButton('Tambah Tugas')
        self.add_task_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_task_button)

        self.setLayout(layout)

    def add_task(self):
        task_name = self.task_name_input.text()
        course_name = self.course_name_input.text()
        deadline = self.deadline_input.date().toString('yyyy-MM-dd')
        status = self.status_input.currentText()

        if not task_name or not course_name:
            QMessageBox.warning(self, 'Input Error', 'Nama Tugas dan Nama Mata Kuliah tidak boleh kosong!')
            return

        # Simpan tugas ke dalam file
        with open(token, 'a') as file:
            file.write(f"{task_name},{course_name},{deadline},{status}\n")

        QMessageBox.information(self, 'Success', 'Tugas berhasil ditambahkan!')

        # Reset input
        self.task_name_input.clear()
        self.course_name_input.clear()
        self.deadline_input.clear()
        self.status_input.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    task_manager = TaskManager()
    task_manager.show()
    sys.exit(app.exec_())