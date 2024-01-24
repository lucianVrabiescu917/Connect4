class BoardException(Exception):
    pass

class ColumnException(BoardException):
    def __str__(self):
        return 'Column not right'

class InputException(Exception):
    pass