import shlex
from pathlib import Path

import prompt

from .utils import save_metadata


def get_command(metadata):
    ''' Запрашивает у пользователя команду
    create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу
    list_tables - показать список всех таблиц
    drop_table <имя_таблицы> - удалить таблицу
    exit - выход из программы
    help - справочная информация
    В случае введения некорректной команды сообщает об ошибке'''
    name = prompt.string('Введите команду: ')
    command = shlex.split(name)
    match command[0]:
        case "create_table":
            if len(command) < 3:
                print('Ошибка: В таблице должен быть хотя бы один столбец')
                return
            else:
                table_name = command[1]
                columns = command[2:]
                create_table(metadata=metadata, table_name=table_name, columns=columns)
        case "list_tables":
            list_tables(metadata=metadata)
        case "drop_table":
            table_name = command[1]
            drop_table(metadata=metadata, table_name=table_name)
        case "help":
            print_help()
            pass
        case "exit":
            print('До свидания')
            return "exit"
        case _:
            print(f'Ошибка: Функции <{shlex.split(name)[0]}> нет. Попробуйте снова.')


def welcome():
    print('***База данных***\n')
    print('Функции:\n')

    print('<command>'
          ' create_table <имя_таблицы> <столбец1:'
          ' тип> <столбец2:тип> .. - создать таблицу')
    print('<command>'
          ' list_tables - '
          'показать все таблицы')
    print('<command>'
          ' drop_table <имя_таблицы>'
          ' - удалить таблицу')
    print('<command> exit -  '
          'выйти из программы')
    print('<command> help'
          ' - справочная информация\n')


def create_table(metadata, table_name, columns):
    '''Проверяет, нет ли в базе данных таблицы с введённым именем
    если есть - выводит сообщение об ошибке
    если нет - добавляет столбец ID и создаёт словарь
    с имя_столбца:тип данных
    вызывает ошибку, если введён некорректный тип данных'''
    filepath = Path(__file__).resolve().parent / "db_meta.json"
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return
    else:
        pass
    dict_ = {"ID":"int"}
    for column in columns:
        key, val = column.split(sep=':')
        if val in ["str", "int", "bool"]:
            dict_[key] = val
        else:
            print(f'Ошибка: тип данных "{val}" не поддерживается,'
            'используйте только int, str, bool.')
            return
    metadata[table_name] = dict_
    save_metadata(filepath=filepath, data=metadata)
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


def drop_table(metadata, table_name):
    '''Проверяет существование таблицы с
    переданным именем
    Выводит сообщение об ошибке, если таблицы нет
    Удаляет таблицу из метаданных в обратном случае'''
    filepath = Path(__file__).resolve().parent / "db_meta.json"
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return
    else:
        del metadata[table_name]
    save_metadata(filepath=filepath, data=metadata)
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


def print_help():
    '''Выводет сообщение со списком команд'''

    print("\n***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")

    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")