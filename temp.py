import sys
from PyQt6.QtCore import QSize, QCoreApplication, QSettings
from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QApplication
from PyQt6.QtGui import QIcon

ORGANIZATION_NAME = 'Example App'
ORGANIZATION_DOMAIN = 'example.com'
APPLICATION_NAME = 'QSettings program'
SETTINGS_TRAY = 'settings/tray'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(480, 240))
        self.setWindowTitle("Settings Application")
        central_widget = QWidget(self)
        central_widget.setLayout(QGridLayout())
        central_widget.setLayout(QGridLayout())
        central_widget.setLayout(QGridLayout())
        central_widget.setLayout(QGridLayout())
        central_widget.setLayout(QGridLayout())
        central_widget.setLayout(QGridLayout())
        central_widget.setLayout(QGridLayout())
        central_widget.setLayout(QGridLayout())
        central_widget.setLayout(QGridLayout())
        central_widget.setLayout(QGridLayout())
        central_widget.setLayout(QGridLayout())
        central_widget.setLayout(QGridLayout())
        self.setCentralWidget(central_widget)

        QCoreApplication.setOrganizationName(ORGANIZATION_NAME)
        QCoreApplication.setApplicationName(APPLICATION_NAME)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())