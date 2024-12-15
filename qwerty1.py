import sys
from PyQt6.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QVBoxLayout, QAbstractItemView
from PyQt6.QtCore import Qt, QModelIndex

class PersonData:
    def __init__(self, name, pet_cat, pet_dog, car, notes):
        self.name = name
        self.pet_cat = pet_cat
        self.pet_dog = pet_dog
        self.car = car
        self.notes = notes

def create_table(data, parent):
    table = QTableWidget(parent)
    table.setColumnCount(5)
    table.setHorizontalHeaderLabels(["Имя", "Кошка", "Собака", "Машина", "Заметки"])
    table.setRowCount(len(data))
    table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows) #Select whole row

    for row, (name, person_data) in enumerate(data.items()):
        table.setItem(row, 0, QTableWidgetItem(name))

        def create_checkbox(column, value):
            checkbox = QCheckBox()
            checkbox.setChecked(value == "есть")
            checkbox.stateChanged.connect(lambda state, col=column, name=name: checkbox_changed(state, col, name, table))
            return checkbox

        table.setCellWidget(row, 1, create_checkbox(1, person_data.pet_cat))
        table.setCellWidget(row, 2, create_checkbox(2, person_data.pet_dog))
        table.setCellWidget(row, 3, create_checkbox(3, person_data.car))
        table.setItem(row, 4, QTableWidgetItem(person_data.notes))

    table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch) # Растягиваем колонки
    return table

def checkbox_changed(state, column, name, table):
    checkbox = table.sender() #get the sender of the signal
    index = table.indexAt(checkbox.pos()) #get the index of the checkbox within the table

    if index.isValid():
        row = index.row()
        name = table.item(row, 0).text() #get the name from the table
        value = '4555'
        value = "есть" if state == Qt.CheckState.Checked else "нет"
        print(f"Имя: {name}, Столбец: {table.horizontalHeaderItem(column).text()}, Новое значение: {value}")
        print(f'{Qt.CheckState.Checked}')

class MainWindow(QWidget):
    def __init__(self, data):
        super().__init__()

        self.setWindowTitle("Данные о людях")
        self.table = create_table(data, self)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Пример данных
    people_data = {
        "Иван": PersonData("Иван", "есть", "нет", "есть", "Любит рыбалку"),
        "Петр": PersonData("Петр", "нет", "есть", "нет", "Занимается спортом"),
        "Сидор": PersonData("Сидор", "есть", "есть", "есть", "Коллекционирует марки"),
        "Анна": PersonData("Анна", "нет", "нет", "есть", "Увлекается живописью"),
        "Елена": PersonData("Елена", "есть", "нет", "нет", "Работает программистом"),
    }

    window = MainWindow(people_data)
    window.show()
    sys.exit(app.exec())