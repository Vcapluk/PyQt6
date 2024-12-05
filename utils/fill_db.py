import pickle


_DB_PATH = 'data/db.txt'
_DB_DUMP = {
    'Присоединение': ['Территория','Секция','Ячейка вкачена', 'ЗН включены', 'ПЗ установлено', 'Примечание' ],
    'БН-1' : [ 'БН-II','Секция №1', True, True, True,'ТН'],
    'БН-2':[ 'БН-II','Секция №1', True, True, False,'Ввод'],
    'БН-3':[ 'БН-II','Секция №2', True, False, True,'масло ф.А'],
    'БН-4':[ 'БН-II','Секция №2', True, False, False,'Блокировка'],
    'БН-5':[ 'БН-II','Секция №3', False, True, True,''],
    'БН-6':[ 'БН-II','Секция №3', False, True, False,''],
    'БН-7':[ 'БН-II','Секция №4', False, False, True,''],
    'БН-8':[ 'БН-II','Секция №4', False, False, False,''],
    'ВЛ-1':[ 'Золоотвал №2','-', False, False, False,''],
    'ВЛ-2':[ 'Золоотвал №2','-', False, False, False,''],
    'ВЛ-3':[ 'Золоотвал №2','-', False, False, False,''],
    'ВЛ-4':[ 'Золоотвал №2','-', False, False, False,''],
    'ВЛ-5':[ 'Золоотвал №2','-', False, False, False,''],
    'ВЛ-6':[ 'Золоотвал №2','-', False, False, False,''],
    'ВЛ-7':[ 'Золоотвал №2','-', False, False, False,''],
    'ВЛ-8':[ 'Золоотвал №2','-', False, False, False,''],
    'ЛР-1':[ 'ВЛ-1','-', False, False, False,''],
    'ЛР-2':[ 'ВЛ-2','-', False, False, False,''],
    'ЛР-3':[ 'ВЛ-3','-', False, False, False,''],
    'ЛР-4':[ 'ВЛ-4','-', False, False, False,''],
    'ЛР-5':[ 'ВЛ-1','-', False, True, False,''],
    'ЛР-6':[ 'ВЛ-2','-', False, True, False,''],
    'ЛР-7':[ 'ВЛ-3','-', False, False, False,''],
    'ЛР-8':[ 'ВЛ-4','-', False, False, False,''],

}


with open(_DB_PATH, 'wb') as fd:
    pickle.dump(_DB_DUMP, fd)
    print(f'DB was saved to {_DB_PATH}')
    print(_DB_DUMP)
