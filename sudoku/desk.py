import random
import util


class Desk:
    subtract_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    size = 9
    cells = [[0] * size] * size
    # Тут хранятся индексы ячеек, которые можно менять:
    free_cells_numbers = [] * 0

    # Проверяем на количество введенных полей
    def __init__(self, remove_cells):
        if remove_cells >= 81:
            raise AttributeError

        self.cells = [[0] * self.size] * self.size
        self._init_desk(remove_cells)

    def _init_desk(self, remove_cells):
        self.cells = [[((i * 3 + i // 3 + j) % (3 * 3) + 1) for j in range(3 * 3)] for i in range(3 * 3)]
        # Случайно перемешиваем:
        for i in range(10):
            rnd = random.randint(0, 3)
            if rnd == 0:
                self._transposing()
            elif rnd == 1:
                self._swap_rows()
            elif rnd == 2:
                self._swap_row_blocks()
            elif rnd == 3:
                self._transposing()
                self._swap_rows()
                self._swap_row_blocks()
                self._transposing()

        # Удаляем случайные ячейки и доавбляем их координаты в список свободных ячеек
        non_empty_cells = [i + 1 for i in range(81)]
        for i in range(remove_cells):
            cell = non_empty_cells.pop(random.randint(0, len(non_empty_cells) - 1))
            self.free_cells_numbers.append(cell - 1)
            self.cells[(cell - 1) // self.size][(cell - 1) % self.size] = 0

    def _transposing(self):
        self.cells = list(map(list, zip(*self.cells)))

    # Меняем строки местами
    def _swap_rows(self):
        index_block = random.randint(0, 2)
        rows = [0, 1, 2]
        row1 = rows.pop(random.randint(0, len(rows) - 1))
        row2 = rows.pop(random.randint(0, len(rows) - 1))

        self.cells[row1 + index_block * 3], self.cells[row2 + index_block * 3] = self.cells[row2 + index_block * 3], self.cells[
            row1 + index_block * 3]

    # Меняем блоки местами
    def _swap_row_blocks(self):
        blocks = [0, 1, 2]
        block1 = blocks.pop(random.randint(0, len(blocks) - 1))
        block2 = blocks.pop(random.randint(0, len(blocks) - 1))

        for i in range(3):
            self.cells[i + block1 * 3], self.cells[i + block2 * 3] = self.cells[i + block1 * 3], self.cells[i + block2 * 3]

    def is_correct_cell(self, row_index, column_index):
        return (row_index * 9 + column_index) in self.free_cells_numbers

    # Проверяем на корректность числа в ячейках
    def is_correct_num(self, n):
        if n > self.size or n < 1:
            return False
        return True

    # Проверяем на корректность блок 3x3:
    def _is_correct_block(self, index_block):
        i_min = 0
        if index_block > 5:
            i_min = 6
        elif index_block > 2:
            i_min = 3

        j_min = 0

        if index_block % 3 == 1:
            j_min = 3
        elif index_block % 3 == 2:
            j_min = 6

        mult = 1
        for i in range(i_min, i_min + 2):
            for j in range(j_min, j_min + 2):
                mult *= self.cells[i][j]
        if mult != 81:
            return False
        return True

    # Меняем значение по ИНДЕКСУ строки, колонки.
    def change_value(self, row, column, key):
        self.cells[row][column] = key


    # Выводим доступные ячейки для изменений
    def get_available_cells(self):
        return list(map(self.to_pair, self.free_cells_numbers))

    def to_pair(self, num):
        return "[Row: " + str((num) // self.size + 1) + ". Column: " + str((num) % self.size + 1) + "]"

    def is_finish(self):
        # Проверка на столбцы и ряды:
        for i in range(self.size):
            # Проверяем ряд:
            if util.multiply_list(self.cells[i]) != 81:
                return False
            # Создаём колонку и проверяем её (если факториал чисел в колонке не равен 81, то судоку не считается законченным):
            column = []
            for j in range(self.size):
                column.append(self.cells[j][i])
            if util.multiply_list(column) != 81:
                return False
        # Проверка на блоки:
        for i in range(9):
            if not self._is_correct_block(i):
                return False
        return True

    def __str__(self):
        outputLine = "\t # # #   # # #   # # #\n\r"
        outputLine += "\t 1 2 3   4 5 6   7 8 9\n\r"
        outputLine += "\t========================\n\r"
        for i in range(self.size):
            outputLine += "#" + str(i + 1) + " | "
            for j in range(len(self.cells[i])):
                if self.cells[i][j] == 0:
                    outputLine += "E"
                else:
                    outputLine += self.cells[i][j].__str__()
                if j % 3 == 2:
                    outputLine += " | "
                else:
                    outputLine += " "
            outputLine += "\n\r"
            if i == 2 or i == 5:
                outputLine += "\t========================\n\r"
        return outputLine

