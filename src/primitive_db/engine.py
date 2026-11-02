from pathlib import Path

from .core import (
    create_table,
    delete,
    drop_table,
    get_command,
    info,
    insert,
    list_tables,
    print_help,
    select,
    update,
    welcome,
)
from .parser import parser_update, parser_where
from .utils import load_metadata


def run():
    welcome()
    filepath = Path(__file__).resolve().parent / "db_meta.json"
    metadata = load_metadata(filepath=filepath)
    while True:
        user_input, command = get_command(metadata=metadata)
        match command[0]:
            case "create_table":
                if len(command) < 3:
                    print('Ошибка: В таблице должен быть хотя бы один столбец')
                    return
                else:
                    table_name = str(command[1])
                    create_table(metadata, table_name, command[2:])
            case "list_tables":
                list_tables(metadata)
            case "drop_table":
                table_name = str(command[1])
                drop_table(metadata, table_name)
            case "help":
                print_help()
                pass
            case "exit":
                print('До свидания')
                break
            case "insert":
                s, p, c = user_input[:-1].partition('(')
                insert(metadata=metadata,
                       table_name=command[2],
                       values=c)
            case "select":
                try:
                    where_clause = parser_where(command, user_input)
                    select(table_name=command[2],
                           where_clause=where_clause)
                except IndexError:
                    print('Ошибка: неверный синтаксис команды '
                          '(введите help для помощи)')
            case "delete":
                try:
                    where_clause = parser_where(command, user_input)
                    delete(table_name=command[2],
                           where_clause=where_clause)
                except IndexError:
                    print('Ошибка: неверный синтаксис команды '
                          '(введите help для помощи)')
                except KeyError:
                    print('Ошибка: введено неверное имя столбца или параметра')
            case "update":
                try:
                    set_clause, where_clause = parser_update(command, user_input)
                    update(table_name=command[1],
                           set_clause=set_clause,
                           where_clause=where_clause)
                except IndexError:
                    print('Ошибка: неверный синтаксис команды '
                          '(введите help для помощи)')
                except KeyError:
                    print('Ошибка: введено неверное имя столбца или параметра')
            case "info":
                info(table_name=command[1], metadata=metadata)
            case _:
                print(f'Ошибка: Функции <{command[0]}> нет. Попробуйте снова.')

