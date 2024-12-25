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
        #print(f"Создана база данных: {db_path}")
    else:
        conn = sqlite3.connect(db_path)
        #print(f"База данных уже существует: {db_path}")

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
    #print("Таблица 'Switch_t' проверена или создана.")
# Вызов функции
create_database_and_table('my_test.db')


def create_table_from_db_full(db_path, table_name, filter_condition=None): # Добавили filter_condition
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
    header.setMaximumSectionSize(100) # Максимальная ширина - 100 пикселей
    return table

def create_table_from_db(db_path, table_name, filter_condition=None): # Добавили filter_condition
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
    table.setHorizontalHeaderLabels(column_names)
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
        print(f"Обновлено в базе данных: {stat}")
        
    except sqlite3.Error as error:
        QMessageBox.critical(None, "Ошибка", f"Ошибка при обновлении базы данных: {error}")
    finally:
        if conn:
            conn.close()


class EditRecordDialog(QDialog):
    def __init__(self, db_path, table_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Редактировать запись")
        self.db_path = db_path
        self.table_name = table_name
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Введите ID записи")
        self.form_layout = QFormLayout()
        self.data_fields = {} # Словарь для хранения полей ввода данных
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.id_input)
        main_layout.addLayout(self.form_layout)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

    def load_data(self):
        try:
            record_id = int(self.id_input.text())
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = ?", (record_id,))
            record = cursor.fetchone()
            conn.close()
            if record:
                columns = self.get_columns()
                # Удаляем старые поля, если они есть
                for i in reversed(range(self.form_layout.rowCount())):
                    self.form_layout.removeRow(i)
                self.data_fields = {} # Очищаем словарь
                for i, value in enumerate(record):
                    if i == 0:
                        continue # пропускаем ID
                    label = QLabel(columns[i] + ":")
                    input_field = QLineEdit(str(value))
                    self.form_layout.addRow(label, input_field)
                    self.data_fields[columns[i]] = input_field
                return True
            else:
                QMessageBox.warning(self, "Ошибка", "Запись не найдена")
                return False
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Неверный формат ID")
            return False
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", str(e))
            return False

    def get_data(self):
        data = {}
        for column, field in self.data_fields.items():
            data[column] = field.text() #Теперь всегда берем текст из поля ввода
        return data

    def get_columns(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {self.table_name}")
        columns = [description[0] for description in cursor.description]
        conn.close()
        return columns




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
        options = ['Off', 'On', '-']

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
        if record:
            info_text = "Информация о записи:\n"
            for key, value in record.items():
                info_text += f"{key}: {value}\n"
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
    
    
    def create_tabs(self):
        self.tab_widget = QTabWidget(self)
        self.main_table = create_table_from_db_full(self.db_path, self.table_name)
        self.tab_widget.addTab(self.main_table, "Присоединения")
        self.off_table = create_table_from_db(self.db_path, self.table_name, "yach = 'Off'")
        self.tab_widget.addTab(self.off_table, "Отключенные присоединения")
        
        self.main_table.cellClicked.connect(self.redact_record)

    def refresh_table(self):
        self.layout.removeWidget(self.tab_widget)
        self.create_tabs()
        self.layout.addWidget(self.tab_widget)


    def populate_table(self, table, filter_condition=None):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query = f"SELECT * FROM {self.table_name}"
        if filter_condition:
            query += f" WHERE {filter_condition}"
        cursor.execute(query)
        data = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        conn.close()
        row_count = len(data)
        table.setRowCount(row_count)
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                table.setItem(i, j, item)
        table.setHorizontalHeaderLabels(columns) #обновляем заголовки после добавления строк








        '''self.on_table = None
        self.off_table = None
        self.main_table = None
        self.create_tabs()
        self.layout.addWidget(self.tab_widget)

        #Добавляем тулбар
        toolbar = QToolBar("Мой тулбар")
        self.addToolBar(toolbar)
        button_action = QAction("Добавить", self)
        button_action.setStatusTip("Добавить присоединение в основную таблицу")
        button_action.triggered.connect(self.add_record)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)
        button_action1 = QAction("Редактировать", self)
        button_action1.setStatusTip("Редактировать существующее присоединение")
        button_action1.triggered.connect(self.redact_record)
        button_action1.setCheckable(True)
        toolbar.addAction(button_action1)
        button_action2 = QAction("Удалить", self)
        button_action2.setStatusTip("Удалить присоединение из основной таблицы")
        button_action2.triggered.connect(self.delete_record)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)
        self.show()


        self.setWindowTitle("База данных")
        self.db_path = db_path
        self.table_name = table_name

        self.layout = QHBoxLayout() # Создаем layout
        self.create_tabs() # Создаем вкладки СНАЧАЛА
        self.layout.addWidget(self.tab_widget) # Добавляем вкладки в layout
        self.setLayout(self.layout) # Устанавливаем layout в самом конце
        self.setFixedSize(1050, 600)
        self.show()'''
        
    
    '''def create_tabs(self):
        self.tab_widget = QTabWidget()
        full_table = create_table_from_db_full(self.db_path,self.table_name, self.tab_widget)
        off_table = create_table_from_db(self.db_path, self.table_name, self.tab_widget, "yach = 'Off'")
        self.tab_widget.addTab(off_table, "Отключено")
        self.tab_widget.addTab(full_table,"Присоединения")'''

    
    def add_record(self):
        dialog = AddRecordDialog(self.db_path, self.table_name, self) # Передаем self как родителя
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_table()
    
    def redact_record(self):
        dialog = EditRecordDialog(self.db_path, self.table_name, self)
        if dialog.exec() == QDialog.DialogCode.Accepted and dialog.load_data():
            data = dialog.get_data()
            record_id = int(dialog.id_input.text())
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                update_query = f"UPDATE {self.table_name} SET "
                update_query += ", ".join([f"{k} = ?" for k in data])
                update_query += f" WHERE id = ?"
                cursor.execute(update_query, tuple(data.values()) + (record_id,))
                conn.commit()
                conn.close()
                self.refresh_table()
                QMessageBox.information(self, "Успех", "Запись успешно обновлена")
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Ошибка базы данных", str(e))
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))
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
    table_index_for_update = [ 'id', 'connectionname', 'terra', 'sekciya', 'yach', 'zn', 'pz', 'annotation' ]
    db_path = "my_test.db" 
    table_name = "Switch_t"

    window = MainWindow(db_path, table_name)
    window.show()
    sys.exit(app.exec())