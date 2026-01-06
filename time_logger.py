import datetime
import os
import sys

# Имя файла для хранения записей
DATA_FILE = "time_records.txt"

def get_current_time():
    """Получает текущую дату и время в формате строки"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def write_time_to_file():
    """Записывает текущую дату и время в файл"""
    current_time = get_current_time()
    with open(DATA_FILE, "a", encoding="utf-8") as file:
        file.write(current_time + "\n")
    print(f"Текущее время и дата записаны в файл: {current_time}")

def read_time_records():
    """Читает и отображает все записи из файла"""
    if not os.path.exists(DATA_FILE):
        print("Файл с записями не найден.")
        return
    
    print("Предыдущие записи времени и даты:")
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        records = file.readlines()
        if records:
            for i, record in enumerate(records, 1):
                print(f"{i}. {record.strip()}")
        else:
            print("Записи отсутствуют.")

def main():
    """Основная функция программы"""
    # Установка кодировки UTF-8 для консоли на Windows
    if sys.platform.startswith('win'):
        os.system('chcp 65001 > nul')
    
    print("Программа для записи и просмотра времени и даты")
    print("1. Записать текущее время и дату")
    print("2. Просмотреть предыдущие записи")
    
    choice = input("Выберите действие (1 или 2): ")
    
    if choice == "1":
        write_time_to_file()
    elif choice == "2":
        read_time_records()
    else:
        print("Некорректный выбор. Пожалуйста, выберите 1 или 2.")

if __name__ == "__main__":
    main()