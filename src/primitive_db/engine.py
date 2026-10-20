import prompt


def welcome():
    print('Первая попытка запустить проект!\n')
    print('***\n')
    print('<\033[32mcommand\033[0m>'
          ' \033[32mexit\033[0m -  '
          'выйти из программы'
          '\n<\033[32mcommand\033[0m>'
          ' \033[32mhelp\033[0m -  '
          'справочная информация\n'
          )
    name = prompt.string('Введите команду: ')