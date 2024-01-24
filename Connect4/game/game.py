
class Game:
    def __init__(self, board, player_human, player_computer):
        self.__board = board
        self.__player1 = player_human
        self.__player2 = player_computer
        self.__last_move = [-1, -1]
        self.__computer_tactic = None

    @property
    def computer_tactic(self):
        return self.__computer_tactic

    @computer_tactic.setter
    def computer_tactic(self, computer_tactic):
        self.__computer_tactic = computer_tactic

    #todo check here
    def _move_human(self, player, column):
        '''
        insert the human's checker in the human's specified column
        :param player: the player object (Player)
        :param column: the column in which to insert the checker
        :return: the returned value of self._game_over -> 'tie', player's name or None
        '''
        last_move = self.__board._insert_checker(column, player.value)
        self.__last_move = last_move
        return self._game_over(last_move, player)


    def _move_computer(self, player_computer):
        '''
        calls the minimax function to calculate the best column in which to insert the checker
        :param player_computer: the player object (Player)
        :return: the returned value of self._game_over -> 'tie', player's name or None
        '''
        score, where_to_insert = self.minimax(self.__board, 4, True, -1000000000, 1000000000)
        last_move = self.__board._insert_checker(where_to_insert, player_computer.value)
        return self._game_over(last_move, player_computer), last_move[1]

    def _move_computer_ez(self, player_computer):
        '''
        ai tries to put the checker in the best place by calculating the score for each place the human could
        place his checker next
        :param player_computer: ai player object (Player)
        :return: the returned value of self._game_over -> 'tie', player's name or None
        '''
        max_score, where_to_insert, score, score_human = 0, 0, 0, 0
        for i in self.__board._return_available_columns():
            self.__board._insert_checker(i, player_computer.value)
            score_human = 0
            for j in self.__board._return_available_columns():
                self.__board._insert_checker(j, self.__player1.value)
                this_score = self._score_positions(self.__board, self.__player1.value)
                if this_score > score_human:
                    score_human = this_score
                self.__board._remove_upper_checker(j)

            score = self._score_positions(self.__board, self.__player2.value)
            if score_human > 100 and score < 100:
                score = -1000


            if score > max_score:
                where_to_insert = i
                max_score = score
            self.__board._remove_upper_checker(i)

        last_move = self.__board._insert_checker(where_to_insert, player_computer.value)
        return self._game_over(last_move, player_computer), last_move[1]






    def minimax(self, board, depth, is_maximizing, alpha, beta):
        '''
        recursive minimax algorithm with alpha-beta pruning

        for each move will be computed a score based on the number of connections with the other checkers and the maximizing
        player will be the computer who'll try to obtain a maximal score, the algorithm will predict where the human
        player will try to place his checker for each move the computer makes, the human will be the minimizing player
        who needs to obtain the lowest score

        the alpha beta pruning will help the speed of the program because it will help the program to avoid going on
        branches of the tree that will end up not affecting the score, in other words it'll stop evaluating a move if
        it is found to be worse than the previous one

        the different variations of the board will be represented on a tree
        :param board: the board of the game (Board)
        :param depth: how deep should the tree go, the deeper the slowest but more accurate (int)
        :param is_maximizing: True if the current player maxing a move is maximizing, or False otherwise (bool)
        :param alpha: the minimum score the maximizing player can have (should tend to -infinity when passed in the
        first functiun call) (int)
        :param beta: the maximal score the minimizing player can have (should tend to infinity when passed in the
        first functiun call) (int)
        :return: best score obtained and the column in which to place the checker (int/int)
        '''
        if depth == 0 or self._score_positions(board, self.__player1.value) >= 1000 or self._score_positions(board, self.__player2.value) >= 1000:
            if self._score_positions(board, self.__player1.value) >= 1000:
                return -1000, None
            elif self._score_positions(board, self.__player2.value) >= 1000:
                return 1000, None
            else:
                return self._score_positions(board, self.__player2.value), None


        if is_maximizing:
            best_score = -1000000000
            column = board._return_available_columns()[0]
            for i in board._return_available_columns():
                board._insert_checker(i, self.__player2.value)
                this_score, trash = self.minimax(board, depth - 1, False, alpha, beta)
                board._remove_upper_checker(i)
                if best_score < this_score:
                    best_score = this_score
                    column = i
                alpha = max(this_score, alpha)
                if beta <= alpha:
                    break
            return best_score, column

        else:
            best_score = 1000000000
            column = board._return_available_columns()[0]
            for i in board._return_available_columns():
                board._insert_checker(i, self.__player1.value)
                this_score, trash = self.minimax(board, depth - 1, True, alpha, beta)
                board._remove_upper_checker(i)
                beta = min(this_score, beta)
                if best_score > this_score:
                    best_score = this_score
                    column = i
                if beta <= alpha:
                    break
            # print(best_score)
            return best_score, column

    def _score_window(self, window, value):
        '''
        scores a window based of how many checkers of the same type connect an how many empty cells are left in the window
        :param window: the window that needs to be scored (list)
        :param value: the checker type (anything)
        :return: computed score (int)
        '''
        if value == self.__player1.value:
            opp_value = self.__player2.value
        else:
            opp_value = self.__player1.value
        score = 0

        if window.count(value) == 4:
            score += 1000
        if window.count(value) == 3 and window.count(0) == 1:
            score += 5
        if window.count(value) == 2 and window.count(0) == 2:
            score += 2
        if window.count(opp_value) == 3 and window.count(0) == 1:
            score -= 4
        # if window.count(opp_value) == 2 and window.count(0) == 2:
        #     score -= 3
        return score



    def _score_positions(self, board, value):
        '''
        each group of 4 cells on the board will pe called a window, each window will pe evaluated by _score_window,
        windows will be taken from each row, then from each column, from each positive sloped diagonal and finally from
        each negative sloped diagonal

        the middle column is preferred to be controlled so point will pe given for placing a checker there
        :param board: board of the game (Board)
        :param value: the value of the checkers that need to be scored (anything)
        :return: final computed score
        '''
        board_matrix = board._return_board()
        score = 0

        center_column = []
        for i in range(board.no_rows):
            center_column.append(board_matrix[i][board.no_rows // 2])
        score += center_column.count(value) * 3

        #horizontal
        for i in range(board.no_rows):
            big_horizontal = [i for i in list(board_matrix[i][:])]
            for el in big_horizontal:
                if type(el) is int:
                    el = int(el)
            for i in range(board.no_columns - 3):
                window = big_horizontal[i : i+4]
                score += self._score_window(window, value)

        #vertical
        for i in range(board.no_columns):
            big_vertical = []
            for row in range(board.no_rows):
                big_vertical.append(board_matrix[row][i])
            for el in big_vertical:
                if type(el) is int:
                    el = int(el)
            for i in range(board.no_rows - 3):
                window = big_vertical[i : i+4]
                score += self._score_window(window, value)

        #digaonals from top lefto to bottom right

        #those under and including the first diagonal
        for row in range(board.no_rows - 4, -1, -1):
            k = 0
            r = row
            diagonal = []
            while r + k < board.no_rows and k < board.no_columns:
                diagonal.append(board_matrix[r + k][k])
                k += 1
            for i in range(len(diagonal) - 3):
                window = diagonal[i : i+4]
                score += self._score_window(window, value)


        #those above the first diagonal
        for column in range(board.no_columns - 4, 0, -1):
            k = 0
            c = column
            diagonal = []
            while c + k < board.no_columns and k < board.no_rows:
                diagonal.append(board_matrix[k][c + k])
                k += 1
            for i in range(len(diagonal) - 3):
                window = diagonal[i : i+4]
                score += self._score_window(window, value)

        #diagonals from top right to bottom left

        # those under and including the second diagonal
        for row in range(board.no_rows - 4, -1, -1):
            k = 0
            r = row
            c = board.no_columns - 1
            diagonal = []
            while r + k < board.no_rows and c - k >= 0:
                diagonal.append(board_matrix[r + k][c - k])
                k += 1
            for i in range(len(diagonal) - 3):
                window = diagonal[i: i + 4]
                score += self._score_window(window, value)

        # those above the second diagonal
        for column in range(board.no_columns - 4, board.no_columns - 1):
            k = 0
            c = column
            diagonal = []
            while c - k >= 0 and k < board.no_rows:
                diagonal.append(board_matrix[k][c - k])
                k += 1
            for i in range(len(diagonal) - 3):
                window = diagonal[i: i + 4]
                score += self._score_window(window, value)

        return score


    def _check_horizontal(self, row, column, value, board_obj, n):
        '''
        check if the last inserted checker connects with n - 1 checkers of the same type horizontally
        :param row: the row where the last checker was inserted
        :param column: the column where the last checker was inserted
        :param value: the value of the last inserted checker
        :param board_obj: the board (Board)
        :param n: how many checker should the connection have
        :return: the 2 ends of the n checkers formation or or False, False otherwise
        '''
        count_h = 0
        aux_column = column
        board = board_obj._return_board()
        while aux_column < board_obj.no_columns and board[row][aux_column] == value:
            count_h += 1
            aux_column += 1
        if count_h == n:
            return [row, column], [row, aux_column - 1]
        one_end = [row, aux_column - 1]
        aux_column = column - 1


        while aux_column >= 0 and board[row][aux_column] == value:
            count_h += 1
            aux_column -= 1
        if count_h == n:
            return [row, aux_column + 1], one_end
        return False, False

    def _check_vertical(self, row, column, value, board_obj, n):
        '''
        check if the last inserted checker connects with n - 1 checkers of the same type vertically
        :param row: the row where the last checker was inserted
        :param column: the column where the last checker was inserted
        :param value: the value of the last inserted checker
        :param board_obj: the board (Board)
        :param n: how many checker should the connection have
        :return: the 2 ends of the n checkers formation or or False, False otherwise
        '''
        count_v = 0
        aux_row = row
        board = board_obj._return_board()

        while aux_row < board_obj.no_rows and board[aux_row][column] == value:
            count_v += 1
            aux_row += 1
        if count_v == n:
            return [row, column], [aux_row - 1, column]
        one_end = [aux_row - 1, column]
        aux_row = row - 1

        while aux_row >= 0 and board[aux_row][column] == value:
            count_v += 1
            aux_row -= 1
        if count_v == n:
            return [aux_row + 1, column], one_end
        return False, False

    def _check_first_digaonal(self, row, column, value, board_obj, n):
        '''
        check if the last inserted checker connects with n - 1 checkers of the same type on the first diagonal
        :param row: the row where the last checker was inserted
        :param column: the column where the last checker was inserted
        :param value: the value of the last inserted checker
        :param board_obj: the board (Board)
        :param n: how many checker should the connection have
        :return: the 2 ends of the n checkers formation or or False, False otherwise
        '''
        count_d1 = 0
        aux_row = row
        aux_column = column
        board = board_obj._return_board()

        while aux_row < board_obj.no_rows and aux_column < board_obj.no_columns and \
                board[aux_row][aux_column] == value:
            count_d1 += 1
            aux_row += 1
            aux_column += 1
        if count_d1 == n:
            return [row, column], [aux_row - 1, aux_column - 1]
        one_end = [aux_row - 1, aux_column - 1]
        aux_row = row - 1
        aux_column = column - 1

        while aux_row >= 0 and aux_column >= 0 and board[aux_row][aux_column] == value:
            count_d1 += 1
            aux_row -= 1
            aux_column -= 1

        if count_d1 == n:
            return [aux_row + 1, aux_column + 1], one_end
        return False, False

    def _check_second_digaonal(self, row, column, value, board_obj, n):
        '''
        check if the last inserted checker connects with n - 1 checkers of the same type on the second diagonal
        :param row: the row where the last checker was inserted
        :param column: the column where the last checker was inserted
        :param value: the value of the last inserted checker
        :param board_obj: the board (Board)
        :param n: how many checker should the connection have
        :return: the 2 ends of the n checkers formation or or False, False otherwise
        '''
        count_d2 = 0
        aux_row = row
        aux_column = column
        board = board_obj._return_board()

        while aux_row < board_obj.no_rows and \
                aux_column >= 0 and board[aux_row][aux_column] == value:
            count_d2 += 1
            aux_row += 1
            aux_column -= 1

        if count_d2 == n:
            return [row, column], [aux_row - 1, aux_column + 1]
        one_end = [aux_row - 1, aux_column + 1]
        aux_row = row - 1
        aux_column = column + 1


        while aux_row >= 0 and aux_column < board_obj.no_columns and board[aux_row][aux_column] == value:
            count_d2 += 1
            aux_row -= 1
            aux_column += 1

        if count_d2 == n:
            return [aux_row + 1, aux_column - 1], one_end
        return False, False

    def _check_connections(self, last_move, value, n):
        '''
        check if the last inserted checker connects with n - 1 other checkers on any directions
        :param last_move: where the last checker was inserted [row, column] (list)
        :param value: checker type (anything)
        :param n: how many checker should the connection have
        :return: the 2 ends of the n checkers formation or or False, False otherwise
        '''
        row = last_move[0]
        column = last_move[1]

        checks = [self._check_horizontal, self._check_vertical, self._check_first_digaonal, self._check_second_digaonal]
        for check in checks:
            other_end, one_end = check(row, column, value, self.__board, n)
            if other_end is not False:
                return other_end, one_end
        return False, False

    def _check_if_tie(self):
        '''
        check if the game ended in a tie by checking if there are any columns available
        :return: True if it ended in a tie, False otherwise
        '''
        for i in range(self.__board.no_columns):
            if self.__board._check_availability(i):
                return False
        return True


    #todo show wining checkers
    def _game_over(self, last_move, player):
        '''
        check if the game ended
        :param last_move: where the last checker was inserted [row, column] (list)
        :param player: the player that made the last move (Player)
        :return: 'tie' if it's a tie, player's name if he won or None if not over
        '''
        if list(self._check_connections(last_move, player.value, 4))[0] is not False:
            return player.name

        if self._check_if_tie():
            return 'tie'
        return None













