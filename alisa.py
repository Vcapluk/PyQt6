import sys
import pickle


from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt


with open('data/db.txt', 'rb') as file:
    readed_data = pickle.load(file)


'''
print('начнем...')
value = readed_data.get('Присоединение')
print(value) 
print(value[0])
valuelen = len(value)
print(valuelen)# гуд, выдает количество столбиков
'''
qwerty = len(readed_data.get('Присоединение'))
print(qwerty)

print('А сейчас магия не случится')
#qwer1 = readed_data
#print(qwer1)
keys = list(readed_data.keys())
keys1 = keys[1]
print(type(keys1))
print(keys1)


print('А сейчас магия не случится')
print('А сейчас магия не случится')
print('А сейчас магия не случится')
print(type(keys[1]))
print(keys[1])

rowfull = int(len(readed_data))
columnfull = int(len(readed_data.get('Присоединение')))
class MyTable(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.table_widget = QtWidgets.QTableWidget()
        self.setCentralWidget(self.table_widget)

        # Устанавливаем количество строк и столбцов в таблице
        self.table_widget.setRowCount(rowfull) # строки
        self.table_widget.setColumnCount(columnfull) #столбики
        keys = list(readed_data.keys())# говорим пролистать все значения ключей и записать их в список

        # Создаём цикл для добавления чекбоксов в каждую ячейку таблицы
        for row in range(self.table_widget.rowCount()):# в каждую строку
            keysnow = keys[row] #говорю, какую строку списка будем смотреть
            print('------ новые значения ------')
            print(keysnow)
            for column in range(self.table_widget.columnCount()):# для каждого столбца
                qwer = readed_data.get(keysnow)
                value = qwer[column] # предполагаю, что должен смотреть на содержание списка и вставлять его в нужную ячейку

                #print(value)
                #checkbox_item = QtWidgets.QTableWidgetItem(str(row))#пока не понятно...
                checkbox_item = QtWidgets.QTableWidgetItem()#пока не понятно...
                #print(value)
                # здесь проверяем содержимое. если тру или фолс - то чекбокс актив/неактив, иначе просто текст
                if value == True:
                    checkbox_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                    checkbox_item.setCheckState(Qt.CheckState.Checked)
                    #checkbox_item.setText('включен')
                    self.table_widget.setItem(row, column, checkbox_item)
                elif value == False:
                    checkbox_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                    checkbox_item.setCheckState(Qt.CheckState.Unchecked)
                    #checkbox_item.setText('выключен')
                    self.table_widget.setItem(row, column, checkbox_item)
                else:
                    checkbox_item.setText(value)
                    self.table_widget.setItem(row, column, checkbox_item)
                    #print(value)


'''
                if column == 1:#столбиков 3. 0, 1, 2. Здесь во второй столбик добавляем чекбоксы
                    checkbox_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                    checkbox_item.setCheckState(Qt.CheckState.Unchecked)
                    checkbox_item.setText('текст  у чекбокса')
                    self.table_widget.setItem(row, column, checkbox_item)
'''


def eventFilter(self, source, event):
    print(event)


if __name__ == "__main__":
    # Создание объекта приложения
    app = QtWidgets.QApplication(sys.argv)
    # Создание окна
    window = MyTable()
    # Отобразить окно на экране
    window.resize(800, 900)
    window.show()
    sys.exit(app.exec())
