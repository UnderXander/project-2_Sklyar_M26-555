import time
from functools import wraps


def handle_db_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден."
                  " Возможно, база данных не инициализирована.")
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
    return wrapper

def log_time(func):
    """Печатает время выполнения функции."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            print(f"Функция {func.__name__} выполнилась"
                  f" за {elapsed:.4f} c")
    return wrapper


def confirm_action(action_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            i = input(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]:')
            if i == 'y':
                return func(*args, **kwargs)
            else:
                print(f'Операция "{action_name}" отменена')
                return
        return wrapper
    return decorator