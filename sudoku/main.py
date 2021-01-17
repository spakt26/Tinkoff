import desk
import pickle

from solver import solve_sudoku

path = 'save.bin'

# Сохраняем нашу доску в файл
def save(_desk):
    with open(path, 'wb') as f:
        pickle.dump(_desk, f)

# Загружаем доску с предыдущей игры
def load():
    with open(path, 'rb') as f:
        return pickle.load(f)


def input_desk():
    full = int(input("Введите количество заполненных клеток: "))
    _desk = desk.Desk(81 - full)

    return _desk


def game():
    print("Привет! Введите 'YES', если хочешь продолжить предыдущую игру - иначе что-нибудь другое: ")
    ans = input()

    if ans.upper() == "YES":
        try:
            _desk = load()
        except IOError:
            _desk = input_desk()
    else:
        _desk = input_desk()

    while not _desk.is_finish():
        save(_desk)
        print(_desk)
        print("Доступные ячейки для изменения: ")
        print(*_desk.get_available_cells())
        ans = input("\nВведите номер ряда, колонки и число, которое хотите вcтавить (Например: \"3 2 9\").\nЕсли хочешь посмотреть решение "
                    "- напиши SOLVE:\n")

        if ans.upper() == "SOLVE":
            for solution in solve_sudoku((3, 3), _desk.cells):
                print(*solution, sep='\n')
            print("В следующий раз получится. Попробуйте еще раз!")
            return 0

        row, column, key = map(int, ans.split())
        while not _desk.is_correct_cell(row - 1, column - 1) or not _desk.is_correct_num(key):
            if not _desk.is_correct_cell(row - 1, column - 1):
                print("Вы ввели неверный номер ячейки. Попробуйте ещё раз: ")
            else:
                print("Вы ввели неверную цифру для вставки. Попробуйте ещё раз: ")
            row, column, key = map(int, input().split())
        _desk.change_value(row - 1, column - 1, key)
    print(_desk)
    print("Ура, вы победили!")


game()