from configparser import ConfigParser


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