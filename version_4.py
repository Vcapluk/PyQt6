import sys
import os
import sqlite3
from PyQt6.QtWidgets import (
    QApplication,
    QWidget, 
    QTableWidget, 
    QTableWidgetItem, 
    QHeaderView, 
    QCheckBox,
    QVBoxLayout, 
    QAbstractItemView, 
    QTabWidget, 
    QPushButton, 
    QDialog, 
    QLabel, 
    QLineEdit,
    QGridLayout, 
    QComboBox, 
    QMessageBox, 
    QFormLayout, 
    QHBoxLayout, 
    QDialogButtonBox, 
    QApplication,
    QCheckBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,)
from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex, QVariant, QSize
from PyQt6.QtGui import QFont
from PyQt6.QtCore import  Qt
from PyQt6.QtGui import QAction, QIcon



def create_database_and_table(db_path):
    # Проверяем, существует ли база данных
    if not os.path.exists(db_path):
        # Создаем новую базу данных
        conn = sqlite3.connect(db_path)
    else:
        conn = sqlite3.connect(db_path)
        
    cursor = conn.cursor()

    # Проверяем, существует ли таблица "Switch_t"
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Switch_t (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            connectionname TEXT,
            terra TEXT,
            sekciya TEXT,
            yach TEXT,
            zn TEXT,
            pz TEXT,
            annotation TEXT
        )
    """)

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
    
# Вызов функции
create_database_and_table('my_test.db')


def create_table_from_db_full(db_path, table_name, filter_condition=None): # Добавили filter_condition
    table_index_ru_id = ['ID','присоединение', 'территория', 'секция', 'ячейка вкачна', 'ЗН включены', 'ПЗ установлено', 'примечание']
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = f"SELECT * FROM {table_name}"
    if filter_condition:
        query += f" WHERE {filter_condition}"
    cursor.execute(query)
    data = cursor.fetchall()
    column_names = [description[0] for description in cursor.description] # Исправлено: description[0]
    conn.close()
    

    table = QTableWidget()
    table.setColumnCount(len(column_names))
    table.setHorizontalHeaderLabels(table_index_ru_id)#русифицировали
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
    header.setMaximumSectionSize(100) # Максимальная ширина - 100 пикселей
    return table

def create_table_from_db(db_path, table_name, filter_condition=None): # Добавили filter_condition
    table_index_ru_id = ['ID','присоединение', 'территория', 'секция', 'ячейка вкачна', 'ЗН включены', 'ПЗ установлено', 'примечание']
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = f"SELECT * FROM {table_name}"
    if filter_condition:
        query += f" WHERE {filter_condition}"
    cursor.execute(query)
    data = cursor.fetchall()
    column_names = [description[0] for description in cursor.description] # Исправлено: description[0]
    conn.close()

    table = QTableWidget()
    table.setColumnCount(len(column_names))
    table.setHorizontalHeaderLabels(table_index_ru_id)#русифицировали
    table.setRowCount(len(data))
    table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

    for row, row_data in enumerate(data):
        for col, cell_data in enumerate(row_data):
            if cell_data == "On":
                item = QTableWidgetItem(str('Вкл')) 
                table.setItem(row, col, item)
            elif cell_data == "Off":
                item = QTableWidgetItem(str('Отключено')) 
                table.setItem(row, col, item)
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


class EditRecordDialog(QDialog):
    def __init__(self, db_path, table_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Введите ID")
        conn = sqlite3.connect(db_path)
        self.conn = conn
        self.db_path = db_path
        self.table_name = table_name
        self.id_input = QLineEdit()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.get_data)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Введите ID:"))
        layout.addWidget(self.id_input)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

    def get_data(self):
        id_value = self.id_input.text()
        if id_value:
            self.accept() # Закрываем диалог и передаем ID дальше
            self.data_window = DataEditWindow(self, self.conn, self.table_name,self.db_path, id_value)
            self.data_window.exec()
        else:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите ID.")


# почему то в одном классе EditRecordDialog все сделать не получается. Поэтому делаю еще один класс как подкласс

class DataEditWindow(QDialog):
    def __init__(self, parent=None, conn=None, table_name=None, db_path=None, id_value=None):
        super().__init__(parent)
        self.setWindowTitle("Редактирование данных")
        self.conn = conn
        self.table_name = table_name
        self.id_value = id_value
        self.table_index_for_update = table_index_for_update
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = ?", (self.id_value,))
        row = self.cursor.fetchone()
        if row:
            self.create_widgets(row)
        else:
            QMessageBox.warning(self, "Ошибка", f"Строка с ID {self.id_value} не найдена.")
            self.close()

    def create_widgets(self, row):
        layout = QVBoxLayout()
        self.inputs = {}
        # Используем имена столбцов из нашей таблицы
        for i, (name, value) in enumerate(zip(self.table_index_for_update[1:], row[1:])): # Начинаем со второго элемента, пропускаем ID
            label = QLabel(f"{name}:")
            line_edit = QLineEdit(str(value))
            self.inputs[name] = line_edit
            h_layout = QHBoxLayout()
            h_layout.addWidget(label)
            h_layout.addWidget(line_edit)
            layout.addLayout(h_layout)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.save_changes)
        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def save_changes(self):
        new_data = {}
        #new_data['id'] = self.id_value
        for key, value in self.inputs.items():
            new_data[key] = value.text()
        new_data['id'] = self.id_value
        try:
            # Динамически генерируем UPDATE запрос
            query = f"UPDATE {self.table_name} SET "
            set_clause = ", ".join([f"{key} = ?" for key in self.inputs]) #Используем имена из словаря
            query += set_clause + f" WHERE id = ?"
            self.cursor.execute(query, tuple(new_data.values())) #Передаем значения
            self.conn.commit()
            QMessageBox.information(self, "Успех", "Данные успешно сохранены!")
            self.accept()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении данных: {e}")
            self.conn.rollback()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Общая ошибка: {e}")
            self.conn.rollback()


class AddRecordDialog(QDialog):
    def __init__(self, db_path, table_name, parent=None): # Добавили parent=None
        super().__init__(parent) # Теперь передаем parent корректно
        self.setWindowTitle("Добавить новое присоединение")
        self.db_path = db_path
        self.table_name = table_name
        self.table_index_for_update = ['connectionname', 'terra', 'sekciya', 'yach', 'zn', 'pz', 'annotation']
        self.table_index_ru = ['присоединение', 'территория', 'секция', 'ячейка вкачна', 'ЗН включены', 'ПЗ установлено', 'примечание']
        self.create_widgets()

    def create_widgets(self):
        grid = QGridLayout()
        self.fields = {}
        options = ['Off', 'On', '-']

        row_num = 0
        for column_name in self.table_index_for_update:
            column_name_ru = self.table_index_ru[self.table_index_for_update.index(column_name)]
            label = QLabel(column_name_ru + ":")
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


class DeleteRecordDialog(QDialog):
    def __init__(self, db_path, table_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Удалить запись")
        self.db_path = db_path
        self.table_name = table_name
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Введите ID записи")
        self.record_info = QLabel("") # Для отображения информации о записи
        self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("ID записи:"))
        layout.addWidget(self.id_input)
        layout.addWidget(self.record_info)
        layout.addWidget(self.buttons)

    def get_id(self):
        return self.id_input.text()

    def show_record_info(self, record):
        table_index_ru_id_slov = {
            'id':'ID',
            'connectionname':'присоединение', 
            'terra':'территория', 
            'sekciya':'секция', 
            'yach':'ячейка вкачна', 
            'zn':'ЗН включены', 
            'pz':'ПЗ установлено', 
            'annotation':'примечание'}# русифицируем еще разик
    
        if record:
            info_text = "Информация о записи:\n"
            for key, value in record.items():
                info_text += f"{table_index_ru_id_slov[key]}: {value}\n"
            self.record_info.setText(info_text)
        else:
            self.record_info.setText("Запись не найдена.")

    def exec(self):
        result = super().exec()
        return result


class MainWindow(QMainWindow):
    def __init__(self, db_path, table_name):
        super().__init__()
        self.setWindowTitle("База данных")
        self.db_path = db_path
        self.table_name = table_name

        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget) # Layout для central_widget

        self.create_tabs() # Создаем вкладки ПЕРЕД установкой layout
        self.layout.addWidget(self.tab_widget)

        

        toolbar = QToolBar("Мой тулбар")
        self.addToolBar(toolbar)
        toolbar.addAction("Добавить запись", self.add_record)
        toolbar.addAction("Удалить запись", self.delete_record)
        toolbar.addAction("Обновить таблицу", self.refresh_table)
        toolbar.addAction("Редактировать запись", self.redact_record)

        self.setFixedSize(900, 600)
    
    
    def create_tabs(self):
        self.tab_widget = QTabWidget(self)
        
        self.off_table = create_table_from_db(self.db_path, self.table_name, "yach = 'Off'")
        self.tab_widget.addTab(self.off_table, "Отключенные присоединения")
        self.main_table = create_table_from_db_full(self.db_path, self.table_name)
        self.tab_widget.addTab(self.main_table, "Присоединения")
        

    def refresh_table(self):
        self.layout.removeWidget(self.tab_widget)
        self.create_tabs()
        self.layout.addWidget(self.tab_widget)

    
    def add_record(self):
        dialog = AddRecordDialog(self.db_path, self.table_name, self) # Передаем self как родителя
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_table()
    
    def redact_record(self):
        dialog = EditRecordDialog(self.db_path, self.table_name, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_table()


    def delete_record(self):
        dialog = DeleteRecordDialog(self.db_path, self.table_name)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            selected_id = dialog.get_id()
            if not selected_id:
                QMessageBox.warning(self, "Предупреждение", "Введите ID для удаления.")
                return

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = ?", (selected_id,))
            record = cursor.fetchone()
            conn.close()

            if record:
                # Преобразуем кортеж в словарь для удобства отображения
                record_dict = dict(zip([description[0] for description in cursor.description], record))
                dialog.show_record_info(record_dict) # Показываем информацию о записи
                if QMessageBox.question(self, "Подтверждение", f"Вы действительно хотите удалить запись с ID {selected_id}?\n{dialog.record_info.text()}",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == \
                        QMessageBox.StandardButton.Yes:
                    try:
                        conn = sqlite3.connect(self.db_path)
                        cursor = conn.cursor()
                        cursor.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (selected_id,))
                        conn.commit()
                        conn.close()
                        QMessageBox.information(self, "Успех", f"Запись с ID {selected_id} успешно удалена!")
                        self.refresh_table()
                    except Exception as e:
                        QMessageBox.critical(self, "Ошибка", f"Ошибка при удалении записи: {e}")
            else:
                QMessageBox.warning(self, "Предупреждение", f"Запись с ID {selected_id} не найдена.")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # это и надо выносить в конфиг?
    # возможно сюда бы еще надо добавить переменные для русификации... но я их оставил в коде
    table_index_for_update = [ 'id', 'connectionname', 'terra', 'sekciya', 'yach', 'zn', 'pz', 'annotation' ]
    db_path = "my_test.db" 
    table_name = "Switch_t"

    window = MainWindow(db_path, table_name)
    window.show()
    sys.exit(app.exec())