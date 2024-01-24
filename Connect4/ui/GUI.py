import sys
import math
import pygame

from custom_exceptions import BoardException


class GUI:
    def __init__(self, board, player1, player2, game):
        pygame.init()
        self.__board = board
        self.__player1 = player1
        self.__player2 = player2
        self.__game = game
        self.__grey = (211,211,211)
        self.__blue = (0,0,230)
        self.__red = (230, 0, 0)
        self.__yellow = (230, 230, 0)
        self.__black = (0,0,0)
        self.__pink = (255,20,147)
        self.__square_size = 100
        self.__radius = int(self.__square_size // 2 - 10)
        self.__colors = {'r': self.__red, 'y': self.__yellow, 0: self.__grey}


    def _create_empty_screen(self):
        board_width = self.__board.no_columns * self.__square_size
        board_height = (self.__board.no_rows + 1) * self.__square_size
        screen = pygame.display.set_mode((board_width, board_height))
        screen.fill(self.__grey)
        pygame.display.update()
        return screen

    def _create_board(self):
        screen = self._create_empty_screen()
        for c in range(self.__board.no_columns):
            for r in range(1, self.__board.no_rows + 1):
                pygame.draw.rect(screen, self.__blue, (self.__square_size * c, self.__square_size * r, self.__square_size, self.__square_size))
                value = self.__board._return_board()[r - 1][c]
                if value  in [self.__player1.value, self.__player2.value, 0]:
                    pygame.draw.circle(screen, self.__colors[value], (self.__square_size * c + self.__square_size // 2,
                                                    self.__square_size * r + self.__square_size // 2), self.__radius)
                if value not in [self.__player1.value, self.__player2.value, 0]:
                    pygame.draw.circle(screen, self.__colors[value[:-1]], (self.__square_size * c + self.__square_size // 2,
                                                                      self.__square_size * r + self.__square_size // 2),
                                       self.__radius)
                    pygame.draw.circle(screen, self.__black, (self.__square_size * c + self.__square_size // 2,
                                                              self.__square_size * r + self.__square_size // 2),
                                       self.__radius // 4)
        pygame.display.update()
        return screen

    def _create_menu(self):
        menu = self._create_empty_screen()

        font = pygame.font.Font('freesansbold.ttf', 48)
        font2 = pygame.font.Font('freesansbold.ttf', 30)
        text = 'Choose a checker'
        text = font.render(text, True, self.__blue)
        textRect = text.get_rect()
        textRect.center = (350, 100)
        menu.blit(text, textRect)
        text2 = 'Choose a difficulty'
        text2 = font.render(text2, True, self.__blue)
        textRect2 = text2.get_rect()
        textRect2.center = (350, 400)
        menu.blit(text2, textRect2)


        button_red = pygame.Rect(self.__square_size * 1, self.__square_size * 2, self.__square_size, self.__square_size)
        button_yellow = pygame.Rect(self.__square_size * 5, self.__square_size * 2, self.__square_size, self.__square_size)
        pygame.draw.circle(menu, self.__red, (self.__square_size * 1 + self.__square_size // 2,
                                                       self.__square_size * 2 + self.__square_size // 2), self.__radius)
        pygame.draw.circle(menu, self.__yellow, (self.__square_size * 5 + self.__square_size // 2,
                                              self.__square_size * 2 + self.__square_size // 2), self.__radius)

        button_easy = pygame.Rect(self.__square_size * 1, self.__square_size * 5, self.__square_size, self.__square_size)
        button_hard = pygame.Rect(self.__square_size * 5, self.__square_size * 5, self.__square_size,
                                    self.__square_size)

        pygame.draw.rect(menu, self.__pink,
                         (self.__square_size * 1, self.__square_size * 5, self.__square_size, self.__square_size))

        pygame.draw.rect(menu, self.__black,
                         (self.__square_size * 5, self.__square_size * 5, self.__square_size, self.__square_size))

        text_easy = 'EASY'
        text_easy = font2.render(text_easy, True, self.__blue)
        menu.blit(text_easy, button_easy)

        text_hard = 'HARD'
        text_hard = font2.render(text_hard, True, self.__blue)
        menu.blit(text_hard, button_hard)


        pygame.display.update()
        return menu, button_red, button_yellow, button_easy, button_hard


    def _create_result_screen(self, result):
        result_screen = self._create_empty_screen()
        pygame.draw.rect(result_screen, self.__grey,
                         (self.__square_size * 7, self.__square_size * 7, self.__square_size, self.__square_size))
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = None
        if result == self.__player1.name:
            mess = 'The winner is ' + self.__player1.name
            text = font.render(mess, True, self.__colors[self.__player1.value])
        elif result == self.__player2.name:
            mess = 'The winner is ' + self.__player2.name
            text = font.render(mess, True, self.__colors[self.__player2.value])
        else:
            text = font.render('Tie', True, self.__blue)
        textRect = text.get_rect()
        textRect.center = (350, 350)
        result_screen.fill(self.__grey)
        result_screen.blit(text, textRect)
        pygame.display.update()
        return result_screen

    def _drop_animation(self, column, screen, value):
        color = self.__colors[value]
        pygame.draw.rect(screen, self.__grey, (0, 0, self.__square_size * self.__board.no_columns, self.__square_size))
        pygame.display.update()
        for row in range(self.__board.no_rows):
            if self.__board._return_board()[row][column] == 0:
                row += 1
                pygame.draw.circle(screen, color,
                                   (self.__square_size * column + self.__square_size // 2,
                                    self.__square_size * row + self.__square_size // 2),
                                   self.__radius)
                pygame.display.update()
                pygame.time.wait(100)
                pygame.draw.circle(screen, self.__grey,
                                   (self.__square_size * column + self.__square_size // 2,
                                    self.__square_size * row + self.__square_size // 2),
                                   self.__radius)
                pygame.display.update()
                row -= 1



    def run_menu(self):
        menu, button_red, button_yellow, button_easy, button_hard = self._create_menu()
        click_checker = False
        click_difficulty = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                click = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    if event.button == 1:
                        click = True
                    if button_red.collidepoint((mx, my)):
                        if click and click_checker is False:
                            self.__player1.value = 'r'
                            self.__player2.value = 'y'
                            click_checker = True
                    if button_yellow.collidepoint((mx, my)):
                        if click and click_checker is False:
                            self.__player1.value = 'y'
                            self.__player2.value = 'r'
                            click_checker = True
                    if button_easy.collidepoint((mx, my)):
                        if click and click_difficulty is False:
                            self.__game.computer_tactic = self.__game._move_computer_ez
                            click_difficulty = True
                    if button_hard.collidepoint((mx, my)):
                        if click and click_difficulty is False:
                            self.__game.computer_tactic = self.__game._move_computer
                            click_difficulty = True
                    click = False
                if  click_checker and click_difficulty:
                    self.run_game()
                    running = False




    def run_game(self):
        screen = self._create_board()
        not_over = True
        if self.__player1.value == 'r':
            turn_human = True
        else:
            turn_human = False
        while not_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, self.__grey, (0, 0, self.__square_size * self.__board.no_columns, self.__square_size))
                    posx = event.pos[0]
                    if turn_human == True:
                        pygame.draw.circle(screen, self.__colors[self.__player1.value], (posx, int(self.__square_size / 2)), self.__radius)
                    pygame.display.update()


                if not turn_human:
                    result, column = self.__game.computer_tactic(self.__player2)
                    row = self.__board._return_peak_of_column(column)
                    last_move = [row, column]
                    other_end, one_end = self.__game._check_connections(last_move, self.__player2.value, 4)
                    print(self.__board._return_board_as_str())
                    self._drop_animation(column, screen, self.__player2.value)
                    screen = self._create_board()
                    turn_human = True
                    if result != None:
                        print(other_end, one_end)
                        if other_end is not False:
                            self.__board._mark_winner(other_end, one_end)
                        print(self.__board._return_board_as_str())
                        screen = self._create_board()
                        pygame.display.update()
                        pygame.time.wait(4000)
                        not_over = False
                        result_screen = self._create_result_screen(result)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    column = int(math.floor(posx / self.__square_size))
                    going = True
                    while going:
                        try:
                            going = False
                            result = self.__game._move_human(self.__player1, column)
                            row = self.__board._return_peak_of_column(column)
                            last_move = [row, column]
                            other_end, one_end = self.__game._check_connections(last_move, self.__player1.value, 4)
                            turn_human = False
                            print(self.__board._return_board_as_str())
                            self._drop_animation(column, screen, self.__player1.value)
                            screen = self._create_board()

                            if result != None:
                                print(other_end, one_end)
                                if other_end is not False:
                                    self.__board._mark_winner(other_end, one_end)
                                print(self.__board._return_board_as_str())
                                screen = self._create_board()
                                pygame.display.update()
                                pygame.time.wait(4000)
                                not_over = False
                                result_screen = self._create_result_screen(result)
                        except BoardException:
                            pass

        if not not_over:
            pygame.time.wait(4000)


