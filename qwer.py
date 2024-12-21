import sys
import sqlite3 
from PyQt6.QtWidgets import (QApplication, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox,
                             QVBoxLayout, QAbstractItemView, QTabWidget, QPushButton, QDialog, QLabel, QLineEdit,
                             QGridLayout, QComboBox, QMessageBox, QHBoxLayout)
from PyQt6.QtCore import Qt




def create_table_from_db(db_path, table_name, parent, filter_condition=None): # Добавили filter_condition
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = f"SELECT * FROM {table_name}"
    if filter_condition:
        query += f" WHERE {filter_condition}"
    cursor.execute(query)
    data = cursor.fetchall()
    column_names = [description[0] for description in cursor.description] # Исправлено: description[0]
    conn.close()

    table = QTableWidget(parent)
    table.setColumnCount(len(column_names))
    table.setHorizontalHeaderLabels(column_names)
    table.setRowCount(len(data))
    table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

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
    # устанавливает ширину столбца в соответствии с содержимым
    header = table.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
    header.setMinimumSectionSize(20) # Минимальная ширина - 20 пикселей
    return table

def checkbox_changed(row, col, checkbox): # Добавили db_path и table_name
#def checkbox_changed(row, col, checkbox, table_name, db_path): # Добавили db_path и table_name
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Получаем ID из первого столбца (предполагаем, что это id)
        cursor.execute(f"SELECT id FROM {table_name} LIMIT 1 OFFSET ?", (row,))
        id_value = cursor.fetchone()[0]

        previous_state = Qt.CheckState.Checked if checkbox.isChecked() else Qt.CheckState.Unchecked
        stat = 'On' if previous_state == Qt.CheckState.Checked else 'Off'
        update_checkbox(id_value, col, stat, db_path, table_name)
        conn.close()

    except (sqlite3.Error, IndexError) as error:
        QMessageBox.critical(None, "Ошибка", f"Ошибка при обработке чекбокса: {error}")
    except Exception as e:
        QMessageBox.critical(None, "Ошибка", f"Неизвестная ошибка: {e}")


    

def update_checkbox(id_value, col, stat, db_path, table_name):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        chb = table_index_for_update[col]
        cursor.execute(f'UPDATE {table_name} SET {chb} = ? WHERE id = ?', (stat, id_value))
        conn.commit()
        conn.close()
    except sqlite3.Error as error:
        QMessageBox.critical(None, "Ошибка", f"Ошибка при обновлении базы данных: {error}")
    finally:
        if conn:
            conn.close()
            print("Соединение с SQLite закрыто")
    
class AddRecordDialog(QDialog):
    def __init__(self, db_path, table_name, parent=None): # Добавили parent=None
        super().__init__(parent) # Теперь передаем parent корректно
        self.setWindowTitle("Добавить новое присоединение")
        self.db_path = db_path
        self.table_name = table_name
        self.table_index_for_update = ['connectionname', 'terra', 'sekciya', 'yach', 'zn', 'pz', 'annotation']
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

        button_box = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)
        button_box.addWidget(ok_button)
        button_box.addWidget(cancel_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(grid)
        main_layout.addLayout(button_box)
        self.setLayout(main_layout)

    def accept(self):
        try:
            data = [self.fields[field].currentText() if field in ['yach', 'zn', 'pz'] else self.fields[field].text()
                    for field in self.table_index_for_update]
            data = tuple(data)

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            placeholders = ','.join(['?'] * len(self.table_index_for_update))
            query = f"INSERT INTO {self.table_name} ({','.join(self.table_index_for_update)}) VALUES ({placeholders})"
            cursor.execute(query, data)
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Успех", "Запись успешно добавлена!")
            super().accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении записи: {e}")






class MainWindow(QWidget):
    def __init__(self, db_path, table_name):
        super().__init__() # Создаём QWidget без родителя
        self.setWindowTitle("Данные из базы данных")
        self.db_path = db_path # Сохраняем db_path как атрибут класса
        self.table_name = table_name # Сохраняем table_name как атрибут класса
        self.table_index_for_update = ['id', 'connectionname', 'terra', 'sekciya', 'yach', 'zn', 'pz', 'annotation']
        self.create_widgets()
        self.create_tabs()
        self.setFixedSize(900, 600)


    def create_widgets(self):
        add_button = QPushButton("Добавить присоединение")
        add_button.clicked.connect(self.add_record)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(add_button)

    def create_tabs(self):
        tabs = QTabWidget(self)
        main_table = create_table_from_db(self.db_path, self.table_name, tabs)
        tabs.addTab(main_table, "Присоединения")

        off_table = create_table_from_db(self.db_path, self.table_name, tabs, "yach = 'Off'")
        tabs.addTab(off_table, "Отключенные присоединения")


        layout = QVBoxLayout(self)
        layout.addWidget(tabs)
        self.setLayout(layout)
    
    def add_record(self):
        dialog = AddRecordDialog(self.db_path, self.table_name, self) # Передаем self как родителя
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_table()
    
    def refresh_table(self):
        # Здесь нужно пересоздать таблицу, чтобы отобразить новые данные.
        # Простой способ - удалить старую таблицу и создать новую
        self.layout.removeWidget(self.tab_widget)
        self.create_tabs()
        self.setLayout(self.layout)

    def create_tabs(self):
        self.tab_widget = QTabWidget(self) # теперь нужно хранить ссылку на виджет вкладок
        main_table = create_table_from_db(self.db_path, self.table_name, self.tab_widget)
        self.tab_widget.addTab(main_table, "Все записи")

        off_table = create_table_from_db(self.db_path, self.table_name, self.tab_widget, "yach = 'Off'")
        self.tab_widget.addTab(off_table, "Записи с yach = 'Off'")

        self.layout.addWidget(self.tab_widget) # добавить виджет вкладок в layout


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # это и надо выносить в конфиг?
    table_index_for_update = [ 'id', 'connectionname', 'terra', 'sekciya', 'yach', 'zn', 'pz', 'annotation' ]
    db_path = "my_test.db" 
    table_name = "Switch_t"

    window = MainWindow(db_path, table_name)
    window.show()
    sys.exit(app.exec())