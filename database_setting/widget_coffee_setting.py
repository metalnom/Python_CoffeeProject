import os
from configparser import ConfigParser
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from mysql.connector import Error, errorcode
from db_connection.db_connection import ConnectionPool


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

    def db_restore(self):
        backup_restore = BackupRestore()
        backup_restore.data_restore('product')
        backup_restore.data_restore('sale')

    def db_backup(self):
        backup_restore = BackupRestore()
        backup_restore.data_backup('product')
        backup_restore.data_backup('sale')


class Dbint:
    def __init__(self):
        self._db = read_ddl_file()

    def __create_database(self):
        try:
            sql = read_ddl_file()
            conn = ConnectionPool().get_instance().get_connection()
            cursor = conn.cursor()
            cursor.execute("create database {} default character set 'utf8'".format(self._db['database_name']))
            print("create database {}".format(self._db['database_name']))
        except Error as err:
            if err.errno == errorcode.ER_DB_CREATE_EXISTS:
                cursor.execute("drop database {} ".format(self._db['database_name']))
                print("drop database {}".format(self._db['database_name']))
                cursor.execute("create database {} default character set 'utf8'".format(self._db['database_name']))
                print("create database {}".format(self._db['database_name']))
            else:
                print(err.msg)
        finally:
            cursor.close()
            conn.close()

    def __create_table(self):
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            cursor.execute("use {}".format(self._db['database_name']))
            for table_name, table_sql in self._db['sql'].items():
                try:
                    print("creating table {}: ".format(table_name), end='')
                    cursor.execute(table_sql)
                except Error as err:
                    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                        print("already exists.")
                    else:
                        print(err.msg)
                else:
                    print("OK")
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()

    def __create_trigger(self):
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            cursor.execute("use {}".format(self._db['database_name']))
            for trigger_name, trigger_sql in self._db['trigger'].items():
                try:
                    print("creating trigger {}: ".format(trigger_name), end='')
                    cursor.execute(trigger_sql)
                except Error as err:
                    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                        print("already exists.")
                    else:
                        print(err.msg)
                else:
                    print("OK")
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()

    def __create_procedure(self):
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            cursor.execute("use {}".format(self._db['database_name']))
            for procedure_name, procedure_sql in self._db['procedure'].items():
                try:
                    print("creating procedure {}: ".format(procedure_name), end='')
                    cursor.execute(procedure_sql)
                except Error as err:
                    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                        print("already exists.")
                    else:
                        print(err.msg)
                else:
                    print("OK")
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()

    def __create_user(self):
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            print("creating user: ", end='')
            cursor.execute(self._db['user_sql'])
            print("OK")
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()

    def service(self):
        self.__create_database()
        self.__create_table()
        self.__create_trigger()
        self.__create_procedure()
        self.__create_user()


class BackupRestore:
    OPTION = """
        CHARACTER SET 'UTF8'
        FIELDS TERMINATED by ','
        LINES TERMINATED by '\r\n'
        """

    def __init__(self, source_dir='data/', data_dir='data/'):
        self.source_dir = os.path.abspath(source_dir) + "/"
        self.data_dir = os.path.abspath(data_dir) + "/"

    def data_backup(self, table_name):
        filename = table_name + '.txt'
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            source_path = self.source_dir + filename
            if os.path.exists(source_path):
                os.remove(source_path)

            backup_sql = "SELECT * FROM {} INTO OUTFILE '{}' {}".format(table_name, source_path, BackupRestore.OPTION)
            cursor.execute(backup_sql)
            print(table_name, "backup complete!")
        except Error as err:
            print(err)
            print(table_name, "backup fail!")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def data_restore(self, table_name):
        filename = table_name + '.txt'
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            data_path = os.path.abspath(self.source_dir + filename).replace('\\', '/')
            cursor.execute("use coffee")
            if not os.path.exists(data_path):
                print("file '{}' does not exist.".format(data_path))
                return
            restore_sql = "LOAD DATA INFILE '{}' INTO TABLE {} {}".format(data_path, table_name, BackupRestore.OPTION)
            cursor.execute(restore_sql)
            conn.commit()
            print(table_name, "restore complete!")
        except Error as err:
            print(err)
            print(table_name, "restore fail!")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


def read_ddl_file(filename='database_setting/coffee_ddl.ini'):
    parser = ConfigParser()
    parser.read(filename, encoding='UTF8')

    db = {}
    for sec in parser.sections():
        items = parser.items(sec)
        if sec == 'name':
            for key, value in items:
                db[key] = value
        if sec == 'sql':
            sql = {}
            for key, value in items:
                sql[key] = "".join(value.splitlines())
            db['sql'] = sql
        if sec == 'trigger':
            trigger = {}
            for key, value in items:
                trigger[key] = " ".join(value.splitlines())
            db['trigger'] = trigger
        if sec == 'procedure':
            procedure = {}
            for key, value in items:
                procedure[key] = " ".join(value.splitlines())
            db['procedure'] = procedure
        if sec == 'user':
            for key, value in items:
                db[key] = value
    return db