import json
import shlex
from json import JSONDecodeError

import prompt
from prettytable import PrettyTable

from .constants import BASE, TYPES
from .decorators import confirm_action, handle_db_errors, log_time
from .utils import get_ids, get_table, save_metadata, save_table_data


def get_command(metadata):
    ''' Запрашивает у пользователя команду
    create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу
    list_tables - показать список всех таблиц
    drop_table <имя_таблицы> - удалить таблицу
    exit - выход из программы
    help - справочная информация
    В случае введения некорректной команды сообщает об ошибке'''
    user_input = prompt.string('Введите команду: ')
    return user_input, shlex.split(user_input)


def welcome():
    print('***База данных***\n')
    print('Функции:\n')

    print('<command>'
          ' create_table <имя_таблицы> <столбец1:'
          ' тип> <столбец2:тип> .. - создать таблицу.')
    print('<command>'
          ' list_tables - '
          'показать все таблицы.')
    print('<command>'
          ' drop_table <имя_таблицы>'
          ' - удалить таблицу.')
    print('<command>'
          ' insert into <имя_таблицы>'
          ' values (<значение1>, <значение2>...'
          ' - создать запись.')
    print('<command> select from'
          ' <имя_таблицы> where'
          ' <столбец> = <значение>'
          ' - прочитать записи по условию.')
    print('<command> select from'
          ' <имя_таблицы>'
          ' - прочитать все записи.')
    print('<command> update <имя_таблицы>'
          ' set <столбец1> = <новое_значение1>'
          ' where <столбец_условия>'
          '= <значение_условия> - обновить запись.')
    print('<command> info <имя_таблицы> -'
          ' вывести информацию о таблице.')
    print("\nОбщие команды:")
    print('<command> exit -'
          ' выйти из программы.')
    print('<command> help'
          ' - справочная информация.\n')


def create_table(metadata, table_name, columns):
    '''Проверяет, нет ли в базе данных таблицы с введённым именем
    если есть - выводит сообщение об ошибке
    если нет - добавляет столбец ID и создаёт словарь
    с имя_столбца:тип данных
    вызывает ошибку, если введён некорректный тип данных'''
    filepath = BASE / "db_meta.json"
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return
    else:
        pass
    dict_ = {"ID": "int"}
    table_data = {"ID": []}
    for column in columns:
        key, val = column.split(sep=':')
        table_data[key] = []
        if val in ["str", "int", "bool"]:
            dict_[key] = val
        else:
            print(f'Ошибка: тип данных "{val}" не поддерживается,'
            'используйте только int, str, bool.')
            return
    metadata[table_name] = dict_
    save_metadata(filepath, metadata)
    table = BASE / "data" / f"{table_name}.json"
    table.parent.mkdir(parents=True, exist_ok=True)
    if table.exists():
        table.unlink()
    else:
        with open(table, "w", encoding="utf-8") as t:
            t.write("")
            json.dump(table_data, t, indent=2)
    save_table_data(table_name, data=table_data)
    print(f'Таблица "{table_name}" успешно создана со столбцами: {dict_}.')
    return metadata

def list_tables(metadata):
    '''Выводит перечень таблиц в БД на экран
    если таблиц нет - выводт сообщение'''
    if metadata == {}:
        print('В базе данных таблиц нет.')
    else:
        for table in list(metadata.keys()):
            print(f'- {table}')


@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    '''Проверяет существование таблицы с
    переданным именем
    Выводит сообщение об ошибке, если таблицы нет
    Удаляет таблицу из метаданных в обратном случае'''
    filepath = BASE / "db_meta.json"
    table = BASE / "data" / f"{table_name}.json"
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return
    else:
        del metadata[table_name]
    table.unlink()
    save_metadata(filepath=filepath, data=metadata)
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


def print_help():
    '''Выводет сообщение со списком команд'''

    print('***База данных***\n')
    print('Функции:\n')

    print('<command>'
          ' create_table <имя_таблицы> <столбец1:'
          ' тип> <столбец2:тип> .. - создать таблицу.')
    print('<command>'
          ' list_tables - '
          'показать все таблицы.')
    print('<command>'
          ' drop_table <имя_таблицы>'
          ' - удалить таблицу.')
    print('<command>'
          ' insert into <имя_таблицы>'
          ' values (<значение1>, <значение2>...'
          ' - создать запись.')
    print('<command> select from'
          ' <имя_таблицы> where'
          ' <столбец> = <значение>'
          ' - прочитать записи по условию.')
    print('<command> select from'
          ' <имя_таблицы>'
          ' - прочитать все записи.')
    print('<command> update <имя_таблицы>'
          ' set <столбец1> = <новое_значение1>'
          ' where <столбец_условия>'
          '= <значение_условия> - обновить запись.')
    print('<command> info <имя_таблицы> -'
          ' вывести информацию о таблице.')
    print("\nОбщие команды:")
    print('<command> exit -'
          ' выйти из программы.')
    print('<command> help'
          ' - справочная информация.\n')


@log_time
def insert(metadata, table_name, values):
    '''Вставляет в существующую таблицу
    переданные в скобках значение'''
    if table_name not in metadata:
        print(f'Ошибка: Таблицы с названием {table_name} не существует.')
        return
    table_data = get_table(table_name)
    ind = len(table_data["ID"]) + 1
    try:
        values = json.loads(f'[{values}]')
    except JSONDecodeError:
        print('Ошибка: значения типа str олжны быть переданы в кавычках ""')
        return
    columns = list(metadata[table_name].items())[1:]
    if len(values) != len(columns):
        print("Ошибка: количество значений не совпадает с количеством столбцов")
        return
    for value, (column_name, type_name) in zip(values, columns):
        expected_type = TYPES[type_name]
        if type(value) is not expected_type:
            print(
                f"Ошибка: значение {value} в столбце {column_name} "
                f"должно иметь тип {type_name}"
            )
            return
    table_data["ID"].append(ind)
    for value, (column_name, _) in zip(values, columns):
        table_data[column_name].append(value)
    print(f'Запись с ID = {ind} успешно добавлена '
          f' в таблицу "{table_name}"')
    save_table_data(table_name, data=table_data)


@handle_db_errors
@log_time
def select(table_name, where_clause):
    '''Выводит на экран при помощи prettytable
    содержимое таблицы по запросу where'''
    table = PrettyTable()
    table_data = get_table(table_name)
    if table_data is None:
        return
    if where_clause is None:
        table.field_names = table_data.keys()
        for i in range(0, len(table_data["ID"])):
            row = []
            for key in table_data:
                row.append(table_data[key][i])
            table.add_row(row)
        print(table)
    else:
        ids, key, value = get_ids(where_clause, table_data)

        table.field_names = table_data.keys()
        for id_ in ids:
            row = []
            for k in table_data:
                row.append(table_data[k][id_])
            table.add_row(row)
        print(table)

@handle_db_errors
@confirm_action("удаление строки")
def delete(table_name, where_clause):
    '''Удаляет строку содержащую
    условие where'''
    table_data = get_table(table_name)
    if table_data is None:
        return
    if where_clause is None:
        print('Ошибка: введите условие <столбец> = <значение>')
        return
    ids, key, value = get_ids(where_clause, table_data)
    for id_ in ids:
        for k in table_data:
            table_data[k].pop(id_)
        print(f'Запись с ID = {id_ + 1} успешно удалена из '
              f'таблицы "{table_name}"')
    table_data["ID"] = list(range(1, len(table_data["ID"]) + 1))
    save_table_data(table_name, data=table_data)


@handle_db_errors
def update(table_name, set_clause, where_clause):
    '''Меняет значение в ячейке set
    по условию в where'''
    table_data = get_table(table_name)
    if table_data is None:
        return
    for key_s, value_s in set_clause.items():
        key_s, value_s
    ids_w, key_w, value_w = get_ids(where_clause, table_data)
    for id_ in ids_w:
        for k in table_data:
            table_data[key_s][id_] = value_s
        print(f'Запись с ID = {id_ + 1} успешно обновлена.')
    save_table_data(table_name, data=table_data)

def info(table_name, metadata):
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return
    else:
        table_data = get_table(table_name)
        print(f'Таблица: {table_name}')
        print(f'Столбцы: {metadata[table_name]}')
        print(f'Количество записей: {len(table_data["ID"])}')
