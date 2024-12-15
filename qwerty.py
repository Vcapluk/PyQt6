import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QCheckBox

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_data()

    def initUI(self):
        self.table = QTableWidget(self)
        self.table.setColumnCount(7)  # 6 столбцов для данных
        self.table.verticalHeader().setVisible(False)
        #self.table.cellChanged.connect(self.cell_changed)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.setWindowTitle("Таблица с чекбоксами")
        self.show()

    def load_data(self):
        connection = sqlite3.connect('my_test.db')
        cursor = connection.cursor()

        readed_data = {}
        cursor.execute('SELECT * FROM Switch_t')
        switch = cursor.fetchall()

        for cnnctnm in switch:
            znach = [cnnctnm[1]]
            spis = [ 
                cnnctnm[2],
                cnnctnm[3],
                cnnctnm[4],
                cnnctnm[5],
                cnnctnm[6],
                cnnctnm[7]
            ]

            cnnctnm_dict = dict.fromkeys(znach, spis)    
            #print(cnnctnm_dict)
            readed_data.update(cnnctnm_dict)
        
        data = readed_data


        rowfull = int(len(readed_data))
        columnfull = int(len(readed_data['Присоединение']))
        keys = list(readed_data.keys())# говорим пролистать все значения ключей и записать их в список

        self.table.setRowCount(len(data))

        for row in range(self.table.rowCount()):# в каждую строку
            keysnow = keys[row] #говорю, какую строку списка будем смотреть
            for column in range(self.table.columnCount()):# для каждого столбца
                self.table.setRowCount(rowfull) # строки
                self.table.setColumnCount(columnfull) #столбики
                
                qwer = readed_data.get(keysnow)
                value = qwer[column]
                #print(value)
                
                checkbox = QCheckBox()
                
                self.table.setCellWidget(row, column+1, checkbox)
                #checkbox.stateChanged.connect(lambda state, r=row, c=column: self.checkbox_clicked(r, c))
                #checkbox.setChecked(value == "On")
                
                if value == 'On':
                    
                    checkbox.setChecked(True)
                    #checkbox.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                    #checkbox.setCheckState(Qt.CheckState.Checked) # Говорим, 
                    checkbox.stateChanged.connect(lambda state, row=row, col=column: self.checkbox_state_changed(state, row, col))
                    #checkbox.setText('включен')
                    #self.table.setItem(row, column, checkbox)
                elif value == 'Off':
                    checkbox.setChecked(False)
                    #checkbox.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                    #checkbox.setCheckState(Qt.CheckState.Unchecked)
                    checkbox.stateChanged.connect(lambda state, row=row, col=column: self.checkbox_state_changed(state, row, col))
                    #checkbox.setText('выключен')
                    #self.table.setItem(row, column, checkbox)
                else:
                    print(f'add',row,column)
                    checkbox.setText(value)
                    #self.table.setItem(row, column, QTableWidgetItem()).setText(value)

                    #textnow.setText(value)
                    #self.table.setItem(row, column, textnow)
                                 
        
        connection.close()

    def checkbox_clicked(self, row, col):
        print(f"Checkbox clicked at Row: {row}, Column: {col}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())




'''import sys
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
        if state == 0:# здесь еще можт быть 1 и 2. 2 - это включили. 1 - промжуточное состояние
            qwerty = 'выключили off'
        else:
            qwerty = 'включили on'
        print(qwerty)

app = QApplication(sys.argv)
window = CheckboxTable()
window.show()
sys.exit(app.exec())
'''

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