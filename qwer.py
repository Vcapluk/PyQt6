import sys
import sqlite3 
from PyQt6.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QVBoxLayout, QAbstractItemView
from PyQt6.QtCore import Qt, QModelIndex


def create_table_from_db(db_path, table_name, parent):
    conn = sqlite3.connect(db_path) 
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    column_names = [description[2] for description in cursor.description] 
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
                checkbox.stateChanged.connect(lambda state, r=row, c=col, cb=checkbox: checkbox_changed(state, r, c, table, cb))
                table.setCellWidget(row, col, checkbox)
            elif cell_data == "Off":
                checkbox = QCheckBox()
                checkbox.setChecked(False) 
                checkbox.stateChanged.connect(lambda state, r=row, c=col, cb=checkbox: checkbox_changed(state, r, c, table, cb))
                table.setCellWidget(row, col, checkbox)
            else:
                item = QTableWidgetItem(str(cell_data)) 
                table.setItem(row, col, item)

    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
    return table

def checkbox_changed(state, row, col, table, checkbox):
    previous_state = Qt.CheckState.Checked if checkbox.isChecked() else Qt.CheckState.Unchecked
    action = "проставлен" if state == Qt.CheckState.Checked else "снят"
    print(f"Состояние чекбокса в строке {row + 1}, столбце {col + 1}: {action} (было: {'проставлен' if previous_state == Qt.CheckState.Checked else 'снят'})")



class MainWindow(QWidget):
    def __init__(self, db_path, table_name):
        super().__init__()
        self.setWindowTitle("Данные из базы данных")
        self.table = create_table_from_db(db_path, table_name, self)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)


    db_path = "my_test.db"  
    table_name = "Switch_t"  

    window = MainWindow(db_path, table_name)
    window.show()
    sys.exit(app.exec())