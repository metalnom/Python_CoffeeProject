from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QMessageBox
from db_connection.coffee_init_service import BackupRestore, Dbint


class MyCoffee(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("database_setting/coffee.ui")
        self.ui.btn_init.clicked.connect(self.db_init)
        self.ui.btn_restore.clicked.connect(self.db_restore)
        self.ui.btn_backup.clicked.connect(self.db_backup)
        self.ui.show()

    def db_init(self):
        db = Dbint()
        db.service()
        if db.idx_database * db.idx_table * db.idx_trigger * db.idx_procedure * db.idx_user == 1:
            QMessageBox.about(self, "알림", "초기화가 성공했습니다.")
        else:
            QMessageBox.about(self, "알림", "초기화가 실패했습니다.")

    def db_restore(self):
        backup_restore = BackupRestore()
        backup_restore.data_restore('product')
        backup_restore.data_restore('sale')
        if backup_restore.idx_restore == 1:
            QMessageBox.about(self, "알림", "복원이 성공했습니다.")
        else:
            QMessageBox.about(self, "알림", "복원이 실패했습니다.")

    def db_backup(self):
        backup_restore = BackupRestore()
        backup_restore.data_backup('product')
        backup_restore.data_backup('sale')
        if backup_restore.idx_backup == 1:
            QMessageBox.about(self, "알림", "백업이 성공했습니다.")
        else:
            QMessageBox.about(self, "알림", "백업이 실패했습니다.")