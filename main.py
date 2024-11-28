import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt,QDate
from PyQt5.QtGui import QPixmap

#file akun2 pengguna
USER_DATA_FILE = 'datausers/users.txt'
#buat token tasks
user = ""
token = "data/" + (user) + "task.txt"

class TaskView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lihat Tugas")
        self.setGeometry(150, 150, 300, 200)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ini adalah jendela untuk melihat tugas."))
        self.setLayout(layout)

class AddTask(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tambah Tugas")
        self.setGeometry(150, 150, 300, 200)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ini adalah jendela untuk melihat tugas."))
        self.setLayout(layout)

class DelTask(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lihat Tugas")
        self.setGeometry(150, 150, 300, 200)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ini adalah jendela untuk menghapus tugas."))
        self.setLayout(layout)

class ReminderTask(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lihat Tugas")
        self.setGeometry(150, 150, 300, 200)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ini adalah jendela untuk reminder tugas."))
        self.setLayout(layout)

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
            global user
            user = username
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