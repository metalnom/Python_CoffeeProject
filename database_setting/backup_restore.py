import os
from mysql.connector import Error
from db_connection.db_connection import ConnectionPool


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