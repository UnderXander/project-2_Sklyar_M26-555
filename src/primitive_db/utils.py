import json


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
            json.dump(data, f)
    except FileNotFoundError:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f)