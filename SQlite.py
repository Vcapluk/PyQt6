import sqlite3
import sys

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QCheckBox, QTableWidget, QTableWidgetItem


connection = sqlite3.connect('my_test.db') # подключаюсь к БД
cursor = connection.cursor() # создаем курсор, нужен для соединения программы и БД

# Создаем таблицу 
# вот это и пойдет в конфиг, полюбому.

cursor.execute('''
CREATE TABLE IF NOT EXISTS Switch (
id INTEGER PRIMARY KEY,
connectionname TEXT NOT NULL,
yach TEXT NOT NULL,
zn TEXT NOT NULL
)
''')

# создать БД, если ее все еще нет, под названием "Connection", если БД есть - едем дальше
# id делаем первичным ключем. Наверняка надо править на что то дургое
# connectionname и pz будет текст, не пустое значение (не NULL)

# !!!!!! Вызов функции создания записи надо делать только 1 раз! !!!!!!
# потом используем функции апгрейда. и надо отдельно создать БД для лога изменений?

# создаем новую запись про БН-1, ячейка выкачена, ЗН включены
#cursor.execute('INSERT INTO Switch (connectionname, yach, zn) VALUES (?, ?, ?)', ('БН-1', 'on', 'on'))
#cursor.execute('INSERT INTO Switch (connectionname, yach, zn) VALUES (?, ?, ?)', ('БН-2', 'off', 'on'))
#cursor.execute('INSERT INTO Switch (connectionname, yach, zn) VALUES (?, ?, ?)', ('БН-3', 'on', 'off'))
#cursor.execute('INSERT INTO Switch (connectionname, yach, zn) VALUES (?, ?, ?)', ('БН-4', 'off', 'off'))
# по этому коду можно добавлять самостоятельно что то из формы обратной связи

# Обновим запись про БН-1
# ЗН включили, и об этом сделали запись в БД
cursor.execute('UPDATE Switch SET zn = ? WHERE connectionname = ?', ('on', 'БН-1'))

'''
# выбираем только столбик zn со значением off
cursor.execute('SELECT connectionname, zn FROM Switch WHERE zn = ?', ('off',))
results = cursor.fetchall()

for row in results:
    print(row) # в результате выдает все записи с zn = off, но по connectionname очень много дубликатов. 
    # Надо их как то сортировать и выдавать только послдние. прогонять через лист?

cursor.execute('SELECT * FROM Switch')
switch = cursor.fetchall()
for cnnctnm in switch:
    print('*****')
    print(cnnctnm)
'''
    
# сделаем запрос к бд, и все данные занесем в список. а по этому списку сделаем табличку...
cursor.execute('SELECT * FROM Switch')
switch = cursor.fetchall()

cnnctnm_list = []
for cnnctnm in switch:
    cnnctnm_dict = {
        'connectionname': cnnctnm[1],
        'yach': cnnctnm[2],
        'zn': cnnctnm[3]
    }
    cnnctnm_list.append(cnnctnm_dict)

#for cnnctnm in cnnctnm_list:
    #print(cnnctnm)

# Обновим запись про БН-1
# ЗН выключили, и об этом сделали запись в БД
cursor.execute('UPDATE Switch SET zn = ? WHERE connectionname = ?', ('off', 'БН-1'))

'''
cursor.execute('SELECT * FROM Switch')
switch = cursor.fetchall()
for cnnctnm in switch:
    print('-----')
    print(cnnctnm)
'''


'''
# Удаляем запись "БН-1"
cursor.execute('DELETE FROM Switch WHERE connectionname = ?', ('БН-1',))
# удаляем 2 3 4
cursor.execute('DELETE FROM Switch WHERE connectionname = ?', ('БН-2',))
cursor.execute('DELETE FROM Switch WHERE connectionname = ?', ('БН-3',))
cursor.execute('DELETE FROM Switch WHERE connectionname = ?', ('БН-4',))
'''

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()

# открывать БД надо только по необходимости. После выполнения действий надо ее закрывать. 

# пробую создать цикл, который из списка(списка ли?) сдлает 24 записи в БД

# вставляем словарь сюда:
dict_spisok1 = {
    'Присоединение': ['Территория','Секция','Ячейка вкачена', 'ЗН включены', 'ПЗ установлено', 'Примечание' ],
    'БН-1' : [ 'БН-II','Секция №1', 'On', 'On', 'On','ТН'],
    'БН-2':[ 'БН-II','Секция №1', 'On', 'On', 'Off','Ввод'],
    'БН-3':[ 'БН-II','Секция №2', 'On', 'Off', 'On','масло ф.А'],
    'БН-4':[ 'БН-II','Секция №2', 'On', 'Off', 'Off','Блокировка'],
    'БН-5':[ 'БН-II','Секция №3', 'Off', 'On', 'On',''],
    'БН-6':[ 'БН-II','Секция №3', 'Off', 'On', 'Off',''],
    'БН-7':[ 'БН-II','Секция №4', 'Off', 'Off', 'On',''],
    'БН-8':[ 'БН-II','Секция №4', 'Off', 'Off', 'Off',''],
    'ВЛ-1':[ 'Золоотвал №2','-', 'Off', 'Off', 'Off',''],
    'ВЛ-2':[ 'Золоотвал №2','-', 'Off', 'Off', 'Off',''],
    'ВЛ-3':[ 'Золоотвал №2','-', 'Off', 'Off', 'Off',''],
    'ВЛ-4':[ 'Золоотвал №2','-', 'Off', 'Off', 'Off',''],
    'ВЛ-5':[ 'Золоотвал №2','-', 'Off', 'Off', 'Off',''],
    'ВЛ-6':[ 'Золоотвал №2','-', 'Off', 'Off', 'Off',''],
    'ВЛ-7':[ 'Золоотвал №2','-', 'Off', 'Off', 'Off',''],
    'ВЛ-8':[ 'Золоотвал №2','-', 'Off', 'Off', 'Off',''],
    'ЛР-1':[ 'ВЛ-1','-', 'Off', 'Off', 'Off',''],
    'ЛР-2':[ 'ВЛ-2','-', 'Off', 'Off', 'Off',''],
    'ЛР-3':[ 'ВЛ-3','-', 'Off', 'Off', 'Off',''],
    'ЛР-4':[ 'ВЛ-4','-', 'Off', 'Off', 'Off',''],
    'ЛР-5':[ 'ВЛ-1','-', 'Off', 'On', 'Off',''],
    'ЛР-6':[ 'ВЛ-2','-', 'Off', 'On', 'Off',''],
    'ЛР-7':[ 'ВЛ-3','-', 'Off', 'Off', 'Off',''],
    'ЛР-8':[ 'ВЛ-4','-', 'Off', 'Off', 'Off',''],
}


connection = sqlite3.connect('my_test.db') # подключаюсь к БД
cursor = connection.cursor() # создаем курсор, нужен для соединения программы и БД
#'Присоединение': ['Территория','Секция','Ячейка вкачена', 'ЗН включены', 'ПЗ установлено', 'Примечание' ],
cursor.execute('''
CREATE TABLE IF NOT EXISTS Switch_t (
id INTEGER PRIMARY KEY,
connectionname TEXT NOT NULL,
terra TEXT NOT NULL,
sekciya TEXT NOT NULL,
yach TEXT NOT NULL,
zn TEXT NOT NULL,
pz TEXT NOT NULL,
annotation TEXT NOT NULL
)
''')


'''
# только 1!!!! раз для добавления в БД!!!
connection.commit()
connection.close()


for key in dict_spisok1:
    connectionname = key
    qwerty  = dict_spisok1[key]
    terra = qwerty[0]
    sekciya = qwerty[1]
    yach = qwerty[2]
    zn = qwerty[3]
    pz = qwerty[4]
    annotation = qwerty[5]
    
    connection = sqlite3.connect('my_test.db') # подключаюсь к БД
    cursor = connection.cursor() # создаем курсор, нужен для соединения программы и БД
    cursor.execute('INSERT INTO Switch_t (connectionname, terra, sekciya, yach, zn, pz, annotation ) VALUES (?, ?, ?, ?, ?, ?, ?)', (connectionname, terra, sekciya, yach, zn, pz, annotation))
    connection.commit()
    connection.close()

'''

#пробуем напечатать то, что получилось...
readed_data = {} #пустой словарь для записей
connection = sqlite3.connect('my_test.db') # подключаюсь к БД
cursor = connection.cursor() # создаем курсор, нужен для соединения программы и БД

cursor.execute('SELECT * FROM Switch_t')
switch = cursor.fetchall()

for cnnctnm in switch:
    znach = [cnnctnm[1]]
    spis = [ 
        cnnctnm[1],
        cnnctnm[2],
        cnnctnm[3],
        cnnctnm[4],
        cnnctnm[5],
        cnnctnm[6],
        cnnctnm[7]
    ]
 
    cnnctnm_dict = dict.fromkeys(znach, spis)    
    readed_data.update(cnnctnm_dict)

rowfull = int(len(readed_data)) #сколько будет строк?
columnfull = int(len(readed_data['Присоединение']))#сколько будет столбиков. Потерялся столбик с именем присоединения. Занесем ка имя в словарь в качестве значения
class MyTable(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.table_widget = QtWidgets.QTableWidget()
        self.setCentralWidget(self.table_widget)

        # Устанавливаем количество строк и столбцов в таблице
        self.table_widget.setRowCount(rowfull) # строки
        self.table_widget.setColumnCount(columnfull) #столбики
        keys = list(readed_data.keys())# говорим пролистать все значения ключей и записать их в список

        # Создаём цикл для добавления чекбоксов в каждую ячейку таблицы, где будут определенные значения
        for row in range(self.table_widget.rowCount()):# в каждую строку
            keysnow = keys[row] #говорю, какую строку списка будем смотреть
            for column in range(self.table_widget.columnCount()):# для каждого столбца
                qwer = readed_data.get(keysnow)
                value = qwer[column] # предполагаю, что должен смотреть на содержание списка и вставлять его в нужную ячейку
                checkbox_item = QtWidgets.QTableWidgetItem()#пока не понятно...
                
                # здесь проверяем содержимое. если on или off - то чекбокс актив/неактив, иначе просто текст
                if value == 'On':
                    checkbox_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                    checkbox_item.setCheckState(Qt.CheckState.Checked) # Говорим, что чекбокс включен
                    self.table_widget.setItem(row, column, checkbox_item)
                elif value == 'Off':
                    checkbox_item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                    checkbox_item.setCheckState(Qt.CheckState.Unchecked) # Говорим, что чекбокс выключен
                    self.table_widget.setItem(row, column, checkbox_item)
                else:
                    checkbox_item.setText(value)
                    self.table_widget.setItem(row, column, checkbox_item)

# бъемся над проблемой отслеживания нажатия на чекбокс. пока не растет. 3 дня прошло.    
# В примерах от ИИ все как бы работает... Но как???? Наверняка надо переписывать заполнение таблицы данными...
        
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

connection.commit()
connection.close()

if __name__ == "__main__":
    # Создание объекта приложения
    app = QtWidgets.QApplication(sys.argv)
    # Создание окна
    window = MyTable()
    # Отобразить окно на экране
    window.resize(800, 900)
    window.show()
    sys.exit(app.exec())

