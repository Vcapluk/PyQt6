import sys
import sqlite3
from PyQt6.QtWidgets import QApplication,QLabel,QComboBox, QLineEdit,QGridLayout, QDialog, QWidget, QTabWidget, QCheckBox, QVBoxLayout, QAbstractItemView, QHeaderView, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import Qt


def create_table_from_db(db_path, table_name, filter_value, parent):
    """Создает таблицу PyQt6, отфильтрованную по значению второго столбца."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = f"SELECT * FROM {table_name} WHERE terra = ?" # Предполагаем, что второй столбец - column2
    cursor.execute(query, (filter_value,))
    data = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]  
    conn.close()

    table = QTableWidget(parent)
    table.setColumnCount(len(column_names))
    table.setHorizontalHeaderLabels(column_names)
    table.setRowCount(len(data))

    for row, row_data in enumerate(data):
        for col, cell_data in enumerate(row_data):
            if cell_data == "On":
                checkbox = QCheckBox()
                checkbox.setChecked(True)
                checkbox.stateChanged.connect(lambda state, r=row, c=col, cb=checkbox: checkbox_changed(r, c, cb))
                table.setCellWidget(row, col, checkbox)
            elif cell_data == "Off":
                checkbox = QCheckBox()
                checkbox.setChecked(False) 
                checkbox.stateChanged.connect(lambda state, r=row, c=col, cb=checkbox: checkbox_changed(r, c, cb))
                table.setCellWidget(row, col, checkbox)
            else:
                item = QTableWidgetItem(str(cell_data)) 
                table.setItem(row, col, item)

    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    return table


def create_tabs_from_db(db_path, table_name, parent):
    """Создает вкладки с таблицами, отфильтрованными по уникальным значениям второго столбца."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f"SELECT DISTINCT terra FROM {table_name}") # Получаем уникальные значения второго столбца
    unique_values = [row[0] for row in cursor.fetchall()]
    conn.close()

    tabs = QTabWidget(parent)

    for value in unique_values:
        table = create_table_from_db(db_path, table_name, value, tabs)
        tabs.addTab(table, value)

    return tabs


def checkbox_changed(row, col, checkbox):
    previous_state = Qt.CheckState.Checked if checkbox.isChecked() else Qt.CheckState.Unchecked
    stat = ''
    if previous_state == Qt.CheckState.Checked:
        stat = 'On'
    else:
        stat = 'Off'
    update_checkbox(row,col,stat)

def update_checkbox(row,col,stat):
    try:
        conn = sqlite3.connect(db_path) 
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        connectionname = data[row][1]
        print(connectionname)
        chb = table_index_for_update[col]
        print(chb)
        cursor.execute(f'UPDATE {table_name} SET {chb} = ? WHERE connectionname = ?', (stat, connectionname))
        conn.commit() 
        conn.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if conn:
            conn.close()
            print("Соединение с SQLite закрыто")


class MainWindow(QWidget):
    def __init__(self, db_path, table_name): # Исправлено: __init__
        super().__init__()
        self.setWindowTitle("Данные из базы данных")
        self.setFixedSize(1200, 600)
        self.db_path = db_path # Добавлено: сохраняем путь к базе данных
        self.table_name = table_name # Добавлено: сохраняем имя таблицы

        self.tabs = create_tabs_from_db(db_path, table_name, self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.tabs)

        # Добавляем кнопку
        add_button = QPushButton("Добавить запись")
        add_button.clicked.connect(lambda: add_new_record(self.db_path, self.table_name))
        layout.addWidget(add_button)

        self.setLayout(layout)


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
        options = ['On', 'Off', '-']

        row_num = 0
        for column_name in self.table_index_for_update:
            label = QLabel(column_name + ":")
            if column_name in ['yach', 'zn', 'pz']:
                combo_box = QComboBox()
                combo_box.addItems(options)
                grid.addWidget(label, row_num, 0)
                grid.addWidget(combo_box, row_num, 1)
                self.fields[column_name] = combo_box
            else:
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
            data = []
            for field in self.table_index_for_update:
                if field in ['yach', 'zn', 'pz']:
                    data.append(self.fields[field].currentText())
                else:
                    data.append(self.fields[field].text())
            data = tuple(data) # Преобразуем в кортеж

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            placeholders = ','.join(['?'] * len(self.table_index_for_update))
            query = f"INSERT INTO {self.table_name} ({','.join(self.table_index_for_update)}) VALUES ({placeholders})"
            cursor.execute(query, data)
            conn.commit()
            conn.close()
            super().accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении записи: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    table_index_for_update = ['id', 'connectionname', 'terra', 'sekciya', 'yach', 'zn', 'pz', 'annotation']
    db_path = "my_test.db"
    table_name = "Switch_t"

    window = MainWindow(db_path, table_name)
    window.show()
    sys.exit(app.exec())