import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt,QDate
from PyQt5.QtGui import *
from datetime import datetime

#file akun2 pengguna
USER_DATA_FILE = 'datausers/users.txt'
#buat token tasks
token = ""

class TaskView(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Daftar Tugas")
        self.setGeometry(100, 100, 600, 400)  # Set ukuran jendela

        # Membuat widget tabel
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(0)  # Awalnya tidak ada baris
        self.table_widget.setColumnCount(4)  # Jumlah kolom
        self.table_widget.setHorizontalHeaderLabels(["Nama Tugas", "Nama Mata Kuliah", "Deadline", "Status Tugas"])

        # Membaca data dari file
        self.load_data_from_file(token)

        # Mengatur ukuran kolom
        self.table_widget.setColumnWidth(0, 150)
        self.table_widget.setColumnWidth(1, 150)
        self.table_widget.setColumnWidth(2, 100)
        self.table_widget.setColumnWidth(3, 150)

        # Membuat tombol Kembali
        self.back_button = QPushButton("Kembali")
        self.back_button.clicked.connect(self.close)  # Menghubungkan tombol dengan fungsi close

        # Mengatur layout
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        layout.addWidget(self.back_button)  # Menambahkan tombol ke layout

        self.setLayout(layout)  # Mengatur layout pada QWidget

    def load_data_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    # Menghapus karakter newline dan memisahkan berdasarkan koma
                    data = line.strip().split(',')
                    if len(data) == 4:  # Pastikan ada 4 elemen
                        self.add_row_to_table(data)
        except Exception as e:
            print(f"Error reading file: {e}")

    def add_row_to_table(self, data):
        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)

        # Menambahkan QComboBox untuk kolom status tugas
        status_combo = QComboBox()
        status_combo.addItems(["Belum Dikerjakan", "Sedang Dikerjakan", "Selesai"])
        status_combo.setCurrentText(data[3])  # Set status yang ada di file
        status_combo.currentTextChanged.connect(lambda: self.update_status(row_position, status_combo.currentText()))

        # Menambahkan item ke tabel
        self.table_widget.setItem(row_position, 0, QTableWidgetItem(data[0]))  # Nama Tugas
        self.table_widget.setItem(row_position, 1, QTableWidgetItem(data[1]))  # Nama Mata Kuliah
        self.table_widget.setItem(row_position, 2, QTableWidgetItem(data[2]))  # Deadline
        self.table_widget.setCellWidget(row_position, 3, status_combo)  # Status Tugas sebagai QComboBox

    def update_status(self, row, status):
        # Update file tasks.txt setiap kali status diubah
        self.save_data_to_file(token)
        
    def save_data_to_file(self, filename):
        try:
            with open(filename, 'w') as file:
                for row in range(self.table_widget.rowCount()):
                    tugas = self.table_widget.item(row, 0).text()
                    mata_kuliah = self.table_widget.item(row, 1).text()
                    deadline = self.table_widget.item(row, 2).text()
                    status_combo = self.table_widget.cellWidget(row, 3)  # Mengambil QComboBox
                    status = status_combo.currentText() if status_combo else ""
                    file.write(f"{tugas},{mata_kuliah},{deadline},{status}\n")
        except Exception as e:
            print(f"Error writing to file: {e}")

class AddTask(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Task Manager')
        self.setGeometry(100, 100, 300, 300)

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

        # Tombol untuk kembali
        self.kembali_button = QPushButton('Kembali')
        self.kembali_button.clicked.connect(self.close)
        layout.addWidget(self.kembali_button)

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

class DelTask(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_tasks()

    def initUI(self):
        self.setWindowTitle('Task Manager')
        self.setGeometry(100, 100, 300, 400)

        self.layout = QVBoxLayout()

        self.label = QLabel('Daftar Tugas:')
        self.layout.addWidget(self.label)

        self.task_list = QListWidget()
        self.layout.addWidget(self.task_list)

        #tombol hapus tugas
        self.delete_button = QPushButton('Hapus Tugas')
        self.delete_button.clicked.connect(self.delete_task)
        self.layout.addWidget(self.delete_button)

        #tombol kembali
        self.kembali_button = QPushButton("Kembali")
        self.kembali_button.clicked.connect(self.close)
        self.layout.addWidget(self.kembali_button)

        self.setLayout(self.layout)

    def load_tasks(self):
        try:
            with open(token, 'r') as file:
                tasks = file.readlines()
                for task in tasks:
                    self.task_list.addItem(task.strip())
        except FileNotFoundError:
            QMessageBox.warning(self, 'Error', 'File tasks.txt tidak ditemukan.')

    def delete_task(self):
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Error', 'Pilih tugas yang ingin dihapus.')
            return

        for item in selected_items:
            self.task_list.takeItem(self.task_list.row(item))

        # Simpan perubahan ke file
        self.save_tasks()

    def save_tasks(self):
        with open(token, 'w') as file:
            for index in range(self.task_list.count()):
                file.write(self.task_list.item(index).text() + '\n')

class ReminderTask(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reminder")
        self.setGeometry(100, 100, 650, 400)

        layout = QVBoxLayout()

        #buat widget table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nama Tugas", "Mata Kuliah", "Deadline", "Status"])

        #buat ukuran kolom table
        self.table.setColumnWidth(0, 200)  # kolom nama Tugas
        self.table.setColumnWidth(1, 100)  # kolom mata Kuliah
        self.table.setColumnWidth(2, 150)  # kolom deadline
        self.table.setColumnWidth(3, 150)  # kolom status

        layout.addWidget(self.table)

        #buat tombol kembali
        self.kembali_button = QPushButton("Kembali")
        self.kembali_button.clicked.connect(self.close)
        layout.addWidget(self.kembali_button)

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

class DashboardWindow(QMainWindow):
    def __init__(self,username):
        super().__init__()
        self.setWindowTitle("Dashboard Ingatin Dong")
        self.setGeometry (300,250,400,290)
        
        #label buat selamat datang
        welcome = QLabel(f"Selamat datang, {username}",self)
        font = welcome.font()
        font.setPointSize(15)
        welcome.setFont(font)
        welcome.setGeometry(0,0,400,70)
        welcome.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        #tombol lihat tugas
        self.lihat = QPushButton("Lihat Tugas",self)
        self.lihat.setGeometry (30,90,150,30)
        self.lihat.clicked.connect(self.lihattugas)

        #tombol tambah tugas
        self.tambah = QPushButton("Tambah Tugas",self)
        self.tambah.setGeometry (30,140,150,30)
        self.tambah.clicked.connect(self.tambahtugas)

        #tombol hapus tugas
        self.hapus = QPushButton("Hapus Tugas",self)
        self.hapus.setGeometry (30,190,150,30)
        self.hapus.clicked.connect(self.hapustugas)

        #tombol reminder tugas
        self.reminder = QPushButton("Reminder",self)
        self.reminder.setGeometry (30,240,150,30)
        self.reminder.clicked.connect(self.remindertugas)

    def lihattugas(self):
        self.viewtask_window = TaskView()
        self.viewtask_window.show()

    def tambahtugas(self):
        self.addtask_window = AddTask()
        self.addtask_window.show()

    def hapustugas(self):
        self.deltask_window = DelTask()
        self.deltask_window.show()

    def remindertugas(self):
        self.reminder_window = ReminderTask()
        self.reminder_window.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome")
        self.setGeometry(300,250,350,300)
        self.initUI()

    def initUI(self):
        #Widget buat label login
        labelsapa = QLabel("Login", self)
        labelsapa.setStyleSheet("font-weight: bold")
        font = labelsapa.font()
        font.setPointSize(10)
        labelsapa.setFont(font)
        labelsapa.setGeometry(0,0,350,50)
        labelsapa.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        #Widget buat line username
        self.lineusername = QLineEdit(self)
        self.lineusername.setMaxLength(50)
        self.lineusername.setPlaceholderText("Masukkan Username")
        self.lineusername.setGeometry(50,65,250,30)

        #Widget buat line password
        self.linepassword = QLineEdit(self)
        self.linepassword.setMaxLength(50)
        self.linepassword.setPlaceholderText("Masukkan Password")
        self.linepassword.setGeometry(50,110,250,30)
        self.linepassword.setEchoMode(QLineEdit.Password)

        #Widget untuk tombol login
        self.loginbutton = QPushButton("Login",self)
        self.loginbutton.setGeometry(50,190,250,30)
        self.loginbutton.clicked.connect(self.login)
    
        #Widget untuk tombol register
        self.loginbutton = QPushButton("Register",self)
        self.loginbutton.setGeometry(50,230,250,30)
        self.loginbutton.clicked.connect(self.register)

    def load_users(self):
        """Membaca pengguna dari file dan mengembalikannya sebagai dictionary."""
        users = {}
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, 'r') as file:
                for line in file:
                    username, password = line.strip().split(',')
                    users[username] = password
        return users
    
    def save_user(self, username, password):
        """Menyimpan pengguna baru ke dalam file."""
        with open(USER_DATA_FILE, 'a') as file:
            file.write(f"{username},{password}\n")
        
    def login(self):
        username = self.lineusername.text()
        password = self.linepassword.text()

        users = self.load_users()
        if username in users and users[username] == password:
            global token
            token = "data/" + username + "tasks.txt"
            QMessageBox.information(self, "Success", "Login berhasil!")
            self.open_dashboard(username)
        else:
            QMessageBox.warning(self, "Error", "Username atau password salah.")
    
    def register(self):
        username = self.lineusername.text()
        password = self.linepassword.text()

        if username == "":
            QMessageBox.warning(self, "Error", "Username tidak boleh kosong.")
            return

        users = self.load_users()
        if username in users:
            QMessageBox.warning(self, "Error", "Username sudah ada. Silakan pilih username yang berbeda.")
            return

        if len(password) < 8:
            QMessageBox.warning(self, "Error", "Password minimal 8 karakter.")
            return

        self.save_user(username, password)
        data = open ("data/" + username + "tasks.txt","w")
        data.close()
        QMessageBox.information(self, "Success", "Pendaftaran berhasil!")

    def open_dashboard(self,username):
        self.dashboard_window = DashboardWindow(username)
        self.dashboard_window.show()
        self.close() #buat nutup jendela login

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())