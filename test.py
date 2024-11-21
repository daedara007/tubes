import getpass, os

USER_DATA_FILE = 'users.txt'

token = ""

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
    while True:
        users = load_users()
        username = input("Masukkan username: ")
        if username == "":
            print ("Username tidak boleh kosong")
        elif username in users:
            print ("Username telah terdaftar")
        else:
            while True:
                password = getpass.getpass("Masukkan password: ")
                if len(password)<8:
                    print ("Password minimal 8 Karakter")
                else:
                    save_user(username, password)
                    print("Pendaftaran berhasil!")
                    break
            break

def login():
    while True:
        users = load_users()
        username = input("Masukkan username: ")
        password = getpass.getpass("Masukkan password: ")

        if username in users and users[username] == password:
            print("Login berhasil!")
            global token
            token = username
            dashboard(username)
            break
        else:
            print("Username atau password salah.")

def main():
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

main()