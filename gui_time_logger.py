import sys
import datetime
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPushButton, QTextEdit, QLabel, QMessageBox, QHBoxLayout)
from PyQt6.QtCore import QTimer, Qt

class TimeLoggerApp(QMainWindow):
    """
    Приложение для логирования времени.
    
    Позволяет записывать текущее время в файл, просматривать записи и очищать их.
    """
    def __init__(self):
        """
        Инициализация приложения.
        
        Создает главное окно, инициализирует пользовательский интерфейс
        и загружает существующие записи из файла.
        """
        super().__init__()
        self.DATA_FILE = "time_records.txt"
        self.initUI()
        self.load_records()
        
    def initUI(self):
        """Инициализация графического интерфейса"""
        self.setWindowTitle('Логгер времени')
        self.setGeometry(100, 100, 500, 400)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Метка с текущим временем
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.time_label)
        
        # Кнопка для записи времени
        self.log_button = QPushButton('Записать текущее время')
        self.log_button.clicked.connect(self.log_current_time)
        layout.addWidget(self.log_button)
        
        # Кнопка для обновления записей
        refresh_layout = QHBoxLayout()
        self.refresh_button = QPushButton('Обновить записи')
        self.refresh_button.clicked.connect(self.load_records)
        refresh_layout.addWidget(self.refresh_button)
        
        # Кнопка для очистки записей
        self.clear_button = QPushButton('Очистить все записи')
        self.clear_button.clicked.connect(self.clear_records)
        refresh_layout.addWidget(self.clear_button)
        
        layout.addLayout(refresh_layout)
        
        # Текстовое поле для отображения записей
        self.records_text = QTextEdit()
        self.records_text.setReadOnly(True)
        layout.addWidget(self.records_text)
        
        # Таймер для обновления времени каждую секунду
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        
        # Инициализация времени
        self.update_time()
        
    def update_time(self):
        """
        Обновление отображения текущего времени.
        
        Получает текущее время и отображает его в метке time_label.
        Вызывается каждую секунду таймером.
        """
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.setText(f"Текущее время: {current_time}")
        
    def log_current_time(self):
        """
        Запись текущего времени в файл.
        
        Получает текущее время и записывает его в файл DATA_FILE.
        После записи отображает сообщение об успехе и обновляет список записей.
        """
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.DATA_FILE, "a", encoding="utf-8") as file:
                file.write(current_time + "\n")
            #QMessageBox.information(self, "Успех", f"Время записано: {current_time}")
            self.load_records()  # Обновляем список записей
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось записать время: {str(e)}")
            
    def load_records(self):
        """
        Загрузка и отображение записей из файла.
        
        Читает записи из файла DATA_FILE и отображает их в текстовом поле records_text.
        Если файл не существует или пуст, отображает сообщение об отсутствии записей.
        """
        if not os.path.exists(self.DATA_FILE):
            self.records_text.setPlainText("Записи отсутствуют.")
            return
            
        try:
            with open(self.DATA_FILE, "r", encoding="utf-8") as file:
                records = file.readlines()
                
            if records:
                # Форматируем записи с номерами
                formatted_records = []
                for i, record in enumerate(records, 1):
                    formatted_records.append(f"{i}. {record.strip()}")
                
                self.records_text.setPlainText("\n".join(formatted_records))
            else:
                self.records_text.setPlainText("Записи отсутствуют.")
        except Exception as e:
            self.records_text.setPlainText(f"Ошибка при чтении файла: {str(e)}")
            
    def clear_records(self):
        """
        Очистка всех записей.
        
        Отображает диалог подтверждения и, при положительном ответе,
        удаляет файл с записями и очищает текстовое поле.
        """
        reply = QMessageBox.question(self, 'Подтверждение',
                                   'Вы уверены, что хотите удалить все записи?',
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if os.path.exists(self.DATA_FILE):
                    os.remove(self.DATA_FILE)
                self.records_text.setPlainText("Записи отсутствуют.")
                QMessageBox.information(self, "Успех", "Все записи удалены.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить записи: {str(e)}")

def main():
    """
    Точка входа в приложение.
    
    Создает экземпляр QApplication, инициализирует главное окно приложения
    и запускает основной цикл обработки событий.
    """
    app = QApplication(sys.argv)
    window = TimeLoggerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()