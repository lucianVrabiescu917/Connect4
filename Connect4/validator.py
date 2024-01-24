from custom_exceptions import ColumnException


class Validator:
    def __init__(self, board):
        self.__board = board

    def validate_column(self, column):
        if column < 0 or column >= self.__board.no_columns:
            raise ColumnException
        if not self.__board._check_availability(column):
            raise ColumnException