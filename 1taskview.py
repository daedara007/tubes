import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QComboBox
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
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
        self.load_data_from_file('tasks.txt')

        # Mengatur ukuran kolom
        self.table_widget.setColumnWidth(0, 150)
        self.table_widget.setColumnWidth(1, 150)
        self.table_widget.setColumnWidth(2, 100)
        self.table_widget.setColumnWidth(3, 150)

        # Mengatur layout
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

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
        self.save_data_to_file('tasks.txt')
        
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

# Menjalankan aplikasi
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())