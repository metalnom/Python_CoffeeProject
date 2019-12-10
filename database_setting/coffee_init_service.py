from mysql.connector import Error, errorcode

from database_setting.read_ddl import read_ddl_file
from db_connection.db_connection import ConnectionPool


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

