import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QDialog, QLabel, QGridLayout, QMessageBox
from PyQt6.QtCore import Qt


def add_new_record(db_path, table_name):
    """Открывает диалоговое окно для добавления новой записи и добавляет ее в БД."""
    dialog = AddRecordDialog(db_path, table_name)
    result = dialog.exec()
    if result == QDialog.DialogCode.Accepted:
        print("Новая запись добавлена.")
    else:
        print("Добавление записи отменено.")


class AddRecordDialog(QDialog):
    def __init__(self, db_path, table_name):
        super().__init__()
        self.setWindowTitle("Добавить новую запись")
        self.db_path = db_path
        self.table_name = table_name
        self.table_index_for_update = ['id', 'connectionname', 'terra', 'sekciya', 'yach', 'zn', 'pz', 'annotation']
        self.create_widgets()

    def create_widgets(self):
        grid = QGridLayout()
        self.fields = {}

        # Нет необходимости запрашивать информацию о столбцах из базы данных, так как она уже известна
        row_num = 0
        for column_name in self.table_index_for_update:
            label = QLabel(column_name + ":")
            line_edit = QLineEdit()
            grid.addWidget(label, row_num, 0)
            grid.addWidget(line_edit, row_num, 1)
            self.fields[column_name] = line_edit
            row_num += 1


        button_box = QVBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        button_box.addWidget(ok_button)
        button_box.addWidget(cancel_button)
        grid.addLayout(button_box, row_num, 0, 1, 2)

        self.setLayout(grid)

    def accept(self):
        try:
            #Здесь мы используем self.table_index_for_update для корректного порядка значений
            data = tuple(self.fields[field].text() for field in self.table_index_for_update)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            #Строка запроса формируется динамически, без использования ','.join
            placeholders = ','.join(['?'] * len(self.table_index_for_update))
            query = f"INSERT INTO {self.table_name} ({','.join(self.table_index_for_update)}) VALUES ({placeholders})"
            cursor.execute(query, data)
            conn.commit()
            conn.close()
            super().accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении записи: {e}")


class MainWindow(QWidget):
    def __init__(self, db_path, table_name):
        super().__init__()
        self.setWindowTitle("Добавление записи в базу данных")
        self.db_path = db_path
        self.table_name = table_name
        self.layout = QVBoxLayout(self)
        add_button = QPushButton("Добавить запись")
        add_button.clicked.connect(lambda: add_new_record(self.db_path, self.table_name))
        self.layout.addWidget(add_button)
        self.setLayout(self.layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    table_index_for_update = [ 'id', 'connectionname', 'terra', 'sekciya', 'yach', 'zn', 'pz', 'annotation' ]
    db_path = "my_test.db" 
    table_name = "Switch_t"
    window = MainWindow(db_path, table_name)
    window.show()
    sys.exit(app.exec())