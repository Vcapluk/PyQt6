import sys
from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QCheckBox

class CheckboxTable(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Checkbox Table")

        self.table = QTableWidget(5, 5)  # Создаём таблицу 5 на 5
        self.init_table()

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def init_table(self):
        # Заполняем таблицу
        for i in range(5):
            for j in range(5):
                if j % 2 == 0:  # Добавляем чекбоксы только в четные столбцы
                    checkbox = QCheckBox()
                    checkbox.stateChanged.connect(lambda state, row=i, col=j: self.checkbox_state_changed(state, row, col))
                    self.table.setCellWidget(i, j, checkbox)
                else:
                    item = QTableWidgetItem(f'Item {i},{j}')
                    self.table.setItem(i, j, item)

    def checkbox_state_changed(self, state, row, col):
        print(f'Чекбокс изменён на строке {row}, столбце {col}')

app = QApplication(sys.argv)
window = CheckboxTable()
window.show()
sys.exit(app.exec())


'''import sys
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QCheckBox, QTableWidget, QTableWidgetItem

class TableWidget(QTableWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.table_widget.setRowCount(10)
        for row in range(self.table_widget.rowCount()):
            item = QTableWidgetItem()
            item.setText(f"Строка {row + 1}")
            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
            self.table_widget.setItem(row, 2, item)

        self.table_widget.clicked.connect(self.on_click)

def on_click(self, item):
    print(f"Пользователь выбрал строку {item.text()}.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    table_widget = TableWidget()
    table_widget.show()
    sys.exit(app.exec())'''