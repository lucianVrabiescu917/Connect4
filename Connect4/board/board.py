from custom_exceptions import BoardException


class Board:
    def __init__(self, no_rows, no_columns):
        self.__no_rows = no_rows
        self.__no_columns = no_columns
        self.__board = self.__create_board()

    @property
    def no_columns(self):
        return self.__no_columns

    @property
    def no_rows(self):
        return self.__no_rows

    def __create_board(self):
        '''
        create a matrix of rowxcolumn size and return it
        :return: the created matrix
        '''
        return [[0 for column in range(self.__no_columns)]
                for row in range(self.__no_rows)]

    def _return_board(self):
        '''
        return the board
        :return: the board
        '''
        return self.__board

    def _return_board_as_str(self):
        '''
        return the board as a string
        :return: the board (string)
        '''
        res = ""
        for row in range(self.__no_rows):
            for column in range(self.__no_columns):
                aux = str(self.__board[row][column])
                res += aux
                res += ' '
            res += '\n'
        return res

    def _insert_checker(self, column, value):
        '''
        insert the checker value in the specified column
        :param column: in which column the checker must be inserted
        :param value: the value of the checker
        :return: -
        :exception: BoardException raised if the specified column is full or doesn't exist
        '''
        for i in range(self.__no_rows - 1, -1, -1):
            if self.__board[i][column] == 0:
                self.__board[i][column] = value
                return [i, column]
        raise BoardException

    def _remove_upper_checker(self, column):
        '''
        removes the upper most checker from the specified column
        :param column: the specified column
        :return: -
        '''
        for i in range(self.__no_rows):
            if self.__board[i][column] != 0:
                self.__board[i][column] = 0
                break

    def _check_availability(self, column):
        '''
        check if the specified column is available
        :param column: the column to be checked
        :return: True if it's available or False if it's not
        '''
        if self.__board[0][column] != 0:
            return False
        return True

    def _return_available_columns(self):
        '''
        returns a list of available columns
        :return: list of available columns (int)
        '''
        available_col = []
        for i in range(self.__no_columns):
            if self._check_availability(i):
                available_col.append(i)
        return available_col

    def _mark_winner(self, poz1, poz2):
        '''
        marks all the checkers from poz1 to poz2 with the existing value + 'w'
        :param poz1: begining position ([row, column])
        :param poz2: end position ([row, column])
        :return: -
        '''
        board = self._return_board()
        directions_dict = {'bigger': -1, 'smaller': +1, 'equal': 0}

        row_direction = None
        column_direction = None
        board = self._return_board()
        if poz1[0] > poz2[0]:
            row_direction = 'bigger'
        elif poz1[0] < poz2[0]:
            row_direction = 'smaller'
        else:
            row_direction = 'equal'

        if poz1[1] > poz2[1]:
            column_direction = 'bigger'
        elif poz1[1] < poz2[1]:
            column_direction = 'smaller'
        else:
            column_direction = 'equal'

        while poz1[0] != poz2[0] or poz1[1] != poz2[1]:
            board[poz1[0]][poz1[1]] += 'w'
            poz1[0] += directions_dict[row_direction]
            poz1[1] += directions_dict[column_direction]

        board[poz2[0]][poz2[1]] += 'w'
        self._change_board(board)

    def _return_peak_of_column(self, column):
        '''
        returns the row in which the upmost checker exists
        :param column: the column in from which the row peak should be returned
        :return: the row in which the peak exists (int)
        '''
        poz = -1
        for i in range(self.__no_rows - 1, -1, -1):
            if self.__board[i][column] == 0:
                poz = i
                break
        if poz == self.__no_rows - 1:
            return poz
        return poz + 1

    def _change_board(self, matrix):
        '''
        change the matrix of the board with a specified matrix
        :param matrix: the matrix the board will become (list of lists)
        :return: -
        '''
        self.__board = matrix


