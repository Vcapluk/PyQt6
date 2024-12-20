import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QTabWidget, QCheckBox, QVBoxLayout, QAbstractItemView, QHeaderView, QTableWidget, QTableWidgetItem, QVBoxLayout
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
        id = data[row]
        print(id)
        #print(data)
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

def checkbox_changed(row, col, checkbox):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Получаем ID из первого столбца по индексу строки row
        cursor.execute(f"SELECT id FROM {table_name} LIMIT 1 OFFSET ?", (row,))
        id_value = cursor.fetchone()[0] # Получаем значение id
        conn.close()

        previous_state = Qt.CheckState.Checked if checkbox.isChecked() else Qt.CheckState.Unchecked
        stat = 'On' if previous_state == Qt.CheckState.Checked else 'Off'
        update_checkbox(id_value, col, stat, db_path, table_name) # Передаем id вместо row

    except (sqlite3.Error, IndexError) as error:
        QMessageBox.critical(None, "Ошибка", f"Ошибка при получении ID: {error}")
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


class MainWindow(QWidget):
    def __init__(self, db_path, table_name):
        super().__init__()
        self.setWindowTitle("Данные из базы данных")
        self.setFixedSize(1200, 600)
        self.tabs = create_tabs_from_db(db_path, table_name, self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.tabs)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    table_index_for_update = [ 'id', 'connectionname', 'terra', 'sekciya', 'yach', 'zn', 'pz', 'annotation' ]
    db_path = "my_test.db" 
    table_name = "Switch_t"

    window = MainWindow(db_path, table_name)
    window.show()
    sys.exit(app.exec())