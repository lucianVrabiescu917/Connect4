
from custom_exceptions import ColumnException



class Console:
    def __init__(self, board, player1, player2, game, validator):
        self.__board = board
        self.__player1 = player1
        self.__player2 = player2
        self.__game = game
        self.__validator = validator

    def run_game(self):
        first_move = True
        while True:
            print(self.__board._return_board_as_str())
            while True:
                column = None
                try:
                    column = int(input('Enter the column in which you want to put the checker: '))
                    self.__validator.validate_column(column)
                    break
                except ColumnException as ce:
                    print(ce)
                except ValueError:
                    print('Please enter a number')


            result = self.__game._move_human(self.__player1, column)
            if result != None:
                if result != 'tie':
                    print(self.__board._return_board_as_str())
                    print('The winner is', self.__player1.name)
                else:
                    print('Tie')
                break

            if first_move:
                self.__game._move_human(self.__player2, int(self.__board.no_columns / 2))
                first_move = False
            else:
                result, columne = self.__game._move_computer(self.__player2)
                print(result)
                if result != None:
                    if result != 'tie':
                        print(self.__board._return_board_as_str())
                        print('The winner is', self.__player2.name)
                    else:
                        print('Tie')
                    break
