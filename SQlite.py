import sqlite3

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


cursor.execute('SELECT connectionname, zn FROM Switch WHERE zn = ?', ('off',))
results = cursor.fetchall()

for row in results:
    print(row) # в результате выдает все записи с zn = off, но по connectionname очень много дубликатов. 
    # Надо их как то сортировать и выдавать только послдние. прогонять через лист?

cursor.execute('SELECT * FROM Switch')
switch = cursor.fetchall()
for user in switch:
    print('*****')
    print(user)

# Обновим запись про БН-1
# ЗН выключили, и об этом сделали запись в БД
cursor.execute('UPDATE Switch SET zn = ? WHERE connectionname = ?', ('off', 'БН-1'))

cursor.execute('SELECT * FROM Switch')
switch = cursor.fetchall()
for user in switch:
    print('-----')
    print(user)

# Удаляем запись "БН-1"
cursor.execute('DELETE FROM Switch WHERE connectionname = ?', ('БН-1',))


# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()


# открывать БД надо только по необходимости. После выполнения действий надо ее закрывать. 
