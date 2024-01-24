import unittest

from board.board import Board
from custom_exceptions import BoardException


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.board = Board(6, 7)

    def test_create_board(self):
        self.assertEqual(self.board._return_board_as_str(), '0 0 0 0 0 0 0 \n'
                                                             '0 0 0 0 0 0 0 \n'
                                                             '0 0 0 0 0 0 0 \n'
                                                             '0 0 0 0 0 0 0 \n'
                                                             '0 0 0 0 0 0 0 \n'
                                                             '0 0 0 0 0 0 0 \n')

    def test_move(self):
        self.board._insert_checker(1, 'r')
        self.assertEqual(self.board._return_board_as_str(), '0 0 0 0 0 0 0 \n'
                                                            '0 0 0 0 0 0 0 \n'
                                                            '0 0 0 0 0 0 0 \n'
                                                            '0 0 0 0 0 0 0 \n'
                                                            '0 0 0 0 0 0 0 \n'
                                                            '0 r 0 0 0 0 0 \n')
        self.board._insert_checker(1, 'r')
        self.assertEqual(self.board._return_board_as_str(), '0 0 0 0 0 0 0 \n'
                                                            '0 0 0 0 0 0 0 \n'
                                                            '0 0 0 0 0 0 0 \n'
                                                            '0 0 0 0 0 0 0 \n'
                                                            '0 r 0 0 0 0 0 \n'
                                                            '0 r 0 0 0 0 0 \n')
        self.board._insert_checker(1, 'r')
        self.board._insert_checker(1, 'r')
        self.board._insert_checker(1, 'r')
        self.board._insert_checker(1, 'r')
        with self.assertRaises(BoardException):
            self.board._insert_checker(1, 'r')

    def test_return_available_columns(self):
        for i in range(6):
            self.board._insert_checker(6, 'r')
            self.board._insert_checker(3, 'r')

        self.assertEqual([0, 1, 2, 4, 5], self.board._return_available_columns())

    def test_remove_upper_checker(self):
        self.board._insert_checker(1, 'r')
        self.board._insert_checker(1, 'r')
        self.board._remove_upper_checker(1)
        self.assertEqual(self.board._return_board_as_str(), '0 0 0 0 0 0 0 \n'
                                                            '0 0 0 0 0 0 0 \n'
                                                            '0 0 0 0 0 0 0 \n'
                                                            '0 0 0 0 0 0 0 \n'
                                                            '0 0 0 0 0 0 0 \n'
                                                            '0 r 0 0 0 0 0 \n')

    def test_peak_of_column(self):
        matrix = [[0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0]]
        self.board._change_board(matrix)
        peak = self.board._return_peak_of_column(3)
        self.assertEqual(peak, 2)

        matrix = [[0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0]]
        self.board._change_board(matrix)
        peak = self.board._return_peak_of_column(3)
        self.assertEqual(peak, 0)

        matrix = [[0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0]]
        self.board._change_board(matrix)
        peak = self.board._return_peak_of_column(3)
        self.assertEqual(peak, 5)

        matrix = [[0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  ['y', 0, 0, 0, 0, 0, 0],
                  ['y', 0, 0, 0, 0, 0, 0],
                  ['y', 0, 0, 0, 0, 0, 0],
                  ['y', 0, 0, 0, 0, 0, 0]]
        self.board._change_board(matrix)
        peak = self.board._return_peak_of_column(0)
        self.assertEqual(peak, 2)
    def test_mark_winner(self):

        matrix = [[0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  ['r', 'r', 'r', 'r', 0, 0, 0]]

        matrix_w = [[0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  ['rw', 'rw', 'rw', 'rw', 0, 0, 0]]

        self.board._change_board(matrix)
        self.board._mark_winner([5, 3], [5, 0])
        self.assertEqual(self.board._return_board(), matrix_w)





if __name__ == '__main__':
    unittest.main()
