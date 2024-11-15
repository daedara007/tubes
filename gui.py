import getpass, os, sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

USER_DATA_FILE = 'users.txt'

token = ""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ingatin Dong")
        self.setGeometry(100,100,500,500)
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        label1 = QLabel("1",self)
        label2 = QLabel("2",self)
        label3 = QLabel("3",self)

        vbox = QVBoxLayout()

        vbox.addWidget(label1)
        vbox.addWidget(label2)
        vbox.addWidget(label3)

        central_widget.setLayout(vbox)

def dashboard(a):
    print (f"selamat datang {token} di dashboard")
    print (f"selamat datang {a} di dashboard")
    input()

def load_users():
    """Membaca pengguna dari file dan mengembalikannya sebagai dictionary."""
    users = {}
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            for line in file:
                username, password = line.strip().split(',')
                users[username] = password
    return users

def save_user(username, password):
    """Menyimpan pengguna baru ke dalam file."""
    with open(USER_DATA_FILE, 'a') as file:
        file.write(f"{username},{password}\n")

def register():
    users = load_users()
    username = input("Masukkan username: ")
    if username == "":
        print ("Username tidak boleh kosong")
        return
    elif username in users:
        print("Username sudah ada. Silakan pilih username yang berbeda.")
        return

    password = getpass.getpass("Masukkan password: ")
    if len(password) < 8:
        print ("Password minimal 8 karakter")
        return
    save_user(username, password)
    print("Pendaftaran berhasil!")

def login():
    users = load_users()
    username = input("Masukkan username: ")
    password = getpass.getpass("Masukkan password: ")

    if username in users and users[username] == password:
        print("Login berhasil!")
        global token
        token = username
        dashboard(username)
    else:
        print("Username atau password salah.")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    while True:
        print ("1. Login")
        print ("2. Register")
        print ("3. Exit")
        pilih = input("Pilih Menu: ")
        if pilih == "1":
            login()
        elif pilih == "2":
            register()
        elif pilih == "3":
            print ("Bye")
            break
        else:
            print ("Pilihan tidak valid. Ulangi")

if __name__ == "__main__":
    main()