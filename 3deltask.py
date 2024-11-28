import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QMessageBox

tf = ""
token = "data/" + (tf) + "tasks.txt"

class TaskManager(QWidget):
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

        self.delete_button = QPushButton('Hapus Tugas')
        self.delete_button.clicked.connect(self.delete_task)
        self.layout.addWidget(self.delete_button)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    task_manager = TaskManager()
    task_manager.show()
    sys.exit(app.exec_())