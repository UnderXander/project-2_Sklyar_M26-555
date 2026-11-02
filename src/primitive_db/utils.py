import json

from .constants import BASE


def load_metadata(filepath):
    '''Выгружает метаданные из файла db_meta.json
    и передаёт словарь в переменную
    Если файла нет или он пуст - передаёт пустой словарь'''
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return dict()


def save_metadata(filepath, data):
    '''Сохраняет обновлённый словарь metadata
    в файл db_meta.json'''
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except FileNotFoundError:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("")
            json.dump(data, f, indent=2)


def load_table_data(table_name):
    table = BASE / "data" / f"{table_name}.json"
    try:
        with open(table, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f'Ошибка: Таблицы с именем {table_name} не существует.')


def save_table_data(table_name, data):
    table = BASE / "data" / f"{table_name}.json"
    try:
        with open(table, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except FileNotFoundError:
        print(f'Ошибка: Таблицы с именем {table_name} не существует.')

def get_ids(where_clause, table_data):
    '''Функция возвращает id искомых
    элементов в таблицы и используется в
    функция update и delete'''
    for key, value in where_clause.items():
        key, value
    ids = []
    if value in table_data[key]:
        ids = [
            i for i, cell in enumerate(table_data[key])
            if cell == value
        ]
        return ids, key, value
    else:
        print(f'Ошибка: значение {value}'
              f' не найдено в столбце {key}')
        return

def get_table(table_name):
    '''Функция возвращает содержимое таблицы
    Создана для сокращения дублирования кода'''
    table_path = BASE / "data" / f"{table_name}.json"
    try:
        with open(table_path, "r", encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f'Ошибка: Таблицы с названием {table_name} не существует.')
        return

