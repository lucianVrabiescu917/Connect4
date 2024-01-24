import unittest

from board.board import Board
from game.game import Game
from player.players import Player

class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.board = Board(6, 7)
        self.player1 = Player(self.board, 'luci', 'r')
        self.player2 = Player(self.board, 'computer', 'y')
        self.game = Game(self.board, self.player1, self.player2)

    def test_move_human(self):
        matrix = [[0, 0, 0, 0,  0,   0,   0],
                   [0, 0, 0, 0,  0,   0,   0],
                   [0, 0, 0, 0,  0,   0, 0],
                   [0, 0, 0, 0,  0,  0,  0],
                   [0, 0, 0, 0, 0,  0,  0],
                   ['r', 0, 0, 0, 0, 0, 0]]

        self.game._move_human(self.player1, 0)
        self.assertEqual(self.board._return_board(), matrix)

    def test__check_connections(self):
        # matrix = [[0, 0, 0, 0, 0, 0, 0],
        #           [0, 0, 0, 0, 0, 0, 0],
        #           [0, 0, 0, 0, 0, 0, 0],
        #           [0, 0, 0, 0, 0, 0, 0],
        #           [0, 0, 0, 0, 0, 0, 0],
        #           [0, 0, 0, 0, 0, 0, 0]]
        matrix = [[0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 'r', 0],
                  [0, 0, 0, 0, 'r', 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 'r', 0, 0, 0, 0]]
        last_move = [3, 4]
        self.board._change_board(matrix)
        result1, result2 = self.game._check_connections(last_move, 'r', 4)
        self.assertNotEqual(result1, False)
        print('heree', result1, result2)

        matrix = [[0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  ['r', 0, 0, 0, 0, 0, 0],
                  ['r', 0, 0, 0, 0, 0, 0],
                  ['r', 0, 0, 0, 0, 0, 0],
                  ['r', 0, 0, 0, 0, 0, 0]]
        last_move = [2, 0]
        self.board._change_board(matrix)
        result1, result2 = self.game._check_connections(last_move, 'r', 4)
        self.assertNotEqual(result1, False)

        matrix = [[0, 'r', 0, 0, 0, 0, 0],
                  [0, 'y', 'r', 0, 0, 0, 0],
                  [0, 0, 0, 'y', 'r', 0, 0],
                  [0, 0, 0, 0, 'y', 'r', 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0]]
        last_move = [3, 5]
        self.board._change_board(matrix)
        result1, result2 = self.game._check_connections(last_move, 'r', 4)
        self.assertEqual(result1, False)


        matrix = [[0, 'r', 0, 0, 0, 0, 0],
                  [0, 'y', 'r', 0, 0, 0, 0],
                  [0, 0, 0, 'r', 'y', 0, 0],
                  [0, 0, 0, 0, 'r', 'y', 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0]]
        last_move = [3, 4]
        self.board._change_board(matrix)
        result1, result2 = self.game._check_connections(last_move, 'r', 4)
        print('2', result1, result2)
        self.assertNotEqual(result1, False)

        matrix = [[0, 0, 'y', 0, 0, 0, 0],
                  [0, 0, 0, 'y', 0, 0, 0],
                  [0, 0, 0, 0, 'y', 0, 0],
                  [0, 0, 0, 0, 0, 'y', 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0]]
        last_move = [3, 5]
        self.board._change_board(matrix)
        result1, result2 = self.game._check_connections(last_move, 'r', 4)
        self.assertEqual(result1, False)

        matrix = [[0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0]]
        last_move = [2, 3]
        self.board._change_board(matrix)
        result1, result2 = self.game._check_connections(last_move, 'r', 4)
        print(result1, result2)


    def test_check_if_tie(self):
        matrix = [['r', 0, 'y', 'r', 'y', 'r', 'r'],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0]]
        self.board._change_board(matrix)
        result = self.game._check_if_tie()
        self.assertEqual(result, False)

        matrix = [['r', 'r', 'y', 'r', 'y', 'r', 'r'],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0]]
        self.board._change_board(matrix)
        result = self.game._check_if_tie()
        self.assertEqual(result, True)

    def test_score_positions(self):

        matrix = [[0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 'y', 'y', 'y', 0, 0, 0]]
        self.board._change_board(matrix)
        self.assertEqual(1009, self.game._score_positions(self.board, 'r'))

        matrix = [[0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 'y', 'y', 'y', 0, 0, 0]]
        self.board._change_board(matrix)
        self.assertEqual(8, self.game._score_positions(self.board, 'r'))

        matrix = [[0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 'y', 'y', 'y', 0, 0, 0]]
        self.board._change_board(matrix)
        self.assertEqual(0, self.game._score_positions(self.board, 'r'))

    def test_minimax(self):
        matrix = [[0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 'y', 'y', 'y', 0, 0, 0]]
        self.board._change_board(matrix)
        score, where_to_insert = self.game.minimax(self.board, 4, True, -1000000000, 1000000000)
        self.assertEqual(where_to_insert, 0)

        matrix = [[0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 'y', 'y', 0, 0, 0]]
        self.board._change_board(matrix)
        score, where_to_insert = self.game.minimax(self.board, 4, True, -1000000000, 1000000000)
        self.assertEqual(where_to_insert, 3)

        matrix = [[0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 0, 'r', 0, 0, 0],
                  [0, 0, 'y', 'y', 0, 0, 0]]
        self.board._change_board(matrix)
        score, where_to_insert = self.game.minimax(self.board, 4, True, -1000000000, 1000000000)
        self.assertEqual(where_to_insert, 1)





















    # def test_score_pozitions(self):
    #     empty_matrix = matrix2 = [[0, 0, 0, 0,  0,   0,   0],
    #                [0, 0, 0, 0,  0,   0,   0],
    #                [0, 0, 0, 0,  0,   0, 0],
    #                [0, 0, 0, 0,  0,  0,  0],
    #                [0, 0, 0, 0, 0,  0,  0],
    #                [0, 0, 0, 0, 0, 0, 0]]

    #     matrix = [[0, 0, 0, 0, 0, 0, 0],
    #               [0, 0, 0, 0, 0, 0, 0],
    #               [0, 0, 0, 'r', 0, 0, 0],
    #               [0, 0, 0, 'y', 'y', 'y', 0],
    #               [0, 0, 0, 'y', 'y', 'r', 'r'],
    #               ['y', 0, 0, 'y', 'r', 'r', 'r']]
    #
    #     matrix2 = [[0, 0, 0, 0, 0, 0, 0],
    #                 [0, 0, 'y', 'y', 0, 0, 0],
    #                 [0, 0, 'y', 'r', 0, 0, 0],
    #                 [0, 0, 'y', 'y', 'y', 0, 0],
    #                 ['y' ,0 ,'r' ,'y' ,'r' ,'r' ,0],
    #                 ['r' ,0 ,'r' ,'y' ,'r' ,'r' ,0]]
    #
    #     matrix3 = [[0, 0, 0, 0,  0,   0,   0],
    #                [0, 0, 0, 0,  0,   0,   0],
    #                [0, 0, 0, 0,  0,   'r', 0],
    #                [0, 0, 0, 0,  'r',  0,  0],
    #                [0, 0, 0, 'r', 0,  0,  0],
    #                [0, 0, 0, 0, 0, 0, 0]]
    #
    #     self.board._change_board(matrix3)
    #     print(self.game._score_positions(self.board, 'r')

    # def test_checkings(self):
    #
    #     matrix = [[0, 0, 0, 0,  0,   0,   0],
    #                [0, 0, 0, 0,  0,   0,   0],
    #                [0, 0, 0, 'y',  'y',   0, 0],
    #                [0, 0, 'y', 'y',  'r',  0,  0],
    #                ['y', 0, 'y', 'r', 'r',  'r',  0],
    #                ['y', 0, 'r', 'y', 'r', 'r', 'r']]
    #     matrix2 = [[0, 0, 0, 0,  0,   0,   0],
    #                [0, 0, 'r', 0,  0,   0,   0],
    #                [0, 0, 'y', 'y',  0,   0, 0],
    #                [0, 0, 'y', 'y',  0,  0,  0],
    #                [0, 'y', 'y', 'r', 'r',  0,  0],
    #                ['y', 'r', 'r', 'y', 'r', 'r', 0]]
    #     self.board._change_board(matrix2)
    #     # self.game._score_positions(self.board, 'r')
    #     print(self.game._check_second_digaonal(5, 0, 'y', self.board, 4))












if __name__ == '__main__':
    unittest.main()
