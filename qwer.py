import sys
import sqlite3 
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QVBoxLayout, QAbstractItemView, QTabWidget
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
    
    
class MainWindow(QWidget):
    def __init__(self, db_path, table_name):
        super().__init__()
        self.setWindowTitle("Главное окно")
        self.db_path = db_path
        self.table_name = table_name
        self.table_index_for_update = ['id', 'connectionname', 'terra', 'sekciya', 'yach', 'zn', 'pz', 'annotation']
        self.create_tabs()
        self.setFixedSize(900, 600)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Это длинная надпись, которая определяет минимальную ширину окна."))
        layout.addWidget(QPushButton("Кнопка"))
        self.setLayout(layout)

        # Получаем предпочтительный размер окна
        size_hint = self.sizeHint()
        # Устанавливаем минимальный размер, используя горизонтальную составляющую size_hint
        self.setMinimumSize(size_hint.width(), 0) # 0 для вертикальной составляющей, она будет регулироваться автоматически

    def create_tabs(self):
        tabs = QTabWidget(self)
        main_table = create_table_from_db(self.db_path, self.table_name, tabs)
        tabs.addTab(main_table, "Присоединения")

        off_table = create_table_from_db(self.db_path, self.table_name, tabs, "yach = 'Off'")
        tabs.addTab(off_table, "Отключенные присоединения")


        layout = QVBoxLayout(self)
        layout.addWidget(tabs)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # это и надо выносить в конфиг?
    table_index_for_update = [ 'id', 'connectionname', 'terra', 'sekciya', 'yach', 'zn', 'pz', 'annotation' ]
    db_path = "my_test.db" 
    table_name = "Switch_t"

    window = MainWindow(db_path, table_name)
    window.show()
    sys.exit(app.exec())