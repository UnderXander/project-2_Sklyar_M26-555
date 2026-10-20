import prompt
import shlex
import core

def get_command():
    name = prompt.string('Введите команду: ')
    command = shlex.split(name)
    match command[0]:
        case create_table:
            table_name = command[1]
            columns = command[2:]
        # case list_tables:
        # pass
        # case drop_table:
        # pass
        # case exit:
        # pass
        # case help:
        # pass
        case _:
            print(f'Функции <{shlex.split(name)[0]}> нет. Попробуйте снова.')
            get_command()
def welcome():
    print('***База данных***\n')
    print('Функции:\n')

    print('<\033[32mcommand\033[0m>'
          ' create_table -  <имя_таблицы> <столбец1:'
          ' тип> <столбец2:тип> .. показать все таблицы')
    print('<\033[32mcommand\033[0m>'
          ' list_tables -  '
          'показать все таблицы')
    print('<\033[32mcommand\033[0m>'
          ' drop_table <имя_таблицы> -  '
          'удалить таблицу')
    print('<\033[32mcommand\033[0m>'
          ' \033[32mexit\033[0m -  '
          'выйти из программы')
    print('<\033[32mcommand\033[0m>'
          ' \033[32mhelp\033[0m -  '
          'справочная информация\n')
    get_command()

welcome()