from PyQt5.QtWidgets import QApplication
from database_setting.widget_coffee_setting import coffee_widget


if __name__ == "__main__":
    app = QApplication([])
    w = coffee_widget()
    app.exec_()