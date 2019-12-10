from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from database_setting.backup_restore import BackupRestore
from database_setting.coffee_init_service import Dbint


class coffee_widget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("database_setting/coffee.ui")
        DBinit = self.ui.btn_init.clicked.connect(self.db_init)
        DBrestore = self.ui.btn_restore.clicked.connect(self.db_restore)
        DBbackup = self.ui.btn_backup.clicked.connect(self.db_backup)
        self.ui.show()

    def db_init(self):
        db = Dbint()
        db.service()

    def db_restore(self):
        backup_restore = BackupRestore()
        backup_restore.data_restore('product')
        backup_restore.data_restore('sale')

    def db_backup(self):
        backup_restore = BackupRestore()
        backup_restore.data_backup('product')
        backup_restore.data_backup('sale')