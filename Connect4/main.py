from board.board import Board
from custom_exceptions import InputException
from game.game import Game
from player.players import Player
from ui.GUI import GUI
from ui.console import Console
from validator import Validator


def main():
    board = Board(6, 7)
    name_human = input('Enter human player name')
    name_computer = input('Enter computer  player name')
    player1 = Player(board, name_human, 'r')
    player2 = Player(board, name_computer, 'y')
    game = Game(board, player1, player2)
    validator = Validator(board)
    interface = input('Enter the user interface to be used: gui or console')
    try:
        if interface == 'gui':
            gui = GUI(board, player1, player2, game)
            gui.run_menu()
        elif interface == 'console':
            console = Console(board, player1, player2, game, validator)
            console.run_game()
        else:
            raise InputException
    except InputException:
        print("Enter proper interface")

if __name__ == '__main__':
    main()
