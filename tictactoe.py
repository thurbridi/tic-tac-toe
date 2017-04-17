from ast import literal_eval as make_tuple


class Game(object):

    def __init__(self, board=None):
        self.player1 = 'X'  # min
        self.player2 = 'O'  # max

        self.range = range(3)
        if board is None:
            self.board = {}
            for y in self.range:
                for x in self.range:
                    self.board[(x, y)] = ' '
        else:
            self.board = board

    def game_loop(self, starter):
        print(self)

        current_player = starter
        while (not self.won(self.player1, self.board) and
               not self.won(self.player2, self.board) and
               not self.tied(self.board)):
            if current_player == self.player1:
                self.move(current_player, self.user_input(current_player))
            else:
                self.move(current_player,
                          self.minimax(current_player, self.board)[0])

            print(self)

            if current_player == self.player1:
                current_player = self.player2
            else:
                current_player = self.player1

        return

    def minimax(self, player, board):
        moves = []

        if self.won(self.player1, board):
            return [None, -1]
        elif self.won(self.player2, board):
            return [None, 1]
        elif self.tied(board):
            return [None, 0]
        else:

            for pos, mark in board.items():
                if mark == ' ':
                    move = [pos, None]

                    board[pos] = player

                    if player == self.player1:
                        move[1] = self.minimax(self.player2, board)[1]
                    else:
                        move[1] = self.minimax(self.player1, board)[1]

                    board[pos] = ' '

                    moves.append(move)

            # print(board)
            # print("available moves for {}: ".format(player))
            # print(moves)
            # print('')
            if player == self.player1:
                best_score = 2

                for move in moves:
                    if move[1] < best_score:
                        best_score = move[1]
                        best_move = move
            else:
                best_score = -2

                for move in moves:
                    if move[1] > best_score:
                        best_score = move[1]
                        best_move = move

            # print("best move: ")
            # print(best_move)
            # print('')
            return best_move

    def move(self, player, pos):
        # print("{} marked pos: {}".format(player, pos))
        if pos:
            self.board[pos] = player
        else:
            return

    # def move(self, player):
    #     print(self)

    #     if not self.tied():
    #         if not self.won(player, self.board):
    #             if player == self.player1:
    #                 self.move(self.player2)
    #             else:
    #                 self.move(self.player1)
    #         else:
    #             print("Player {} won!".format(player))
    #             return
    #     else:
    #         print("It's a tie!")

    def won(self, player, board):
        # check lines
        for y in self.range:
            winning = []
            for x in self.range:
                if board[(x, y)] == player:
                    winning.append((x, y))
            if len(winning) == 3:
                return True

        # check columns
        for x in self.range:
            winning = []
            for y in self.range:
                if board[(x, y)] == player:
                    winning.append((x, y))
            if len(winning) == 3:
                return True

        # check diagonals
        winning = []
        for y in self.range:
            x = y
            if board[(x, y)] == player:
                winning.append((x, y))
        if len(winning) == 3:
            return True

        winning = []
        for y in self.range:
            x = (3 - y) - 1
            if board[(x, y)] == player:
                winning.append((x, y))
        if len(winning) == 3:
            return True

        # no win
        return False

    def tied(self, board):
        for pos, mark in board.items():
            if mark == " ":
                return False
        return True

    def user_input(self, player):
        mark = input("Type where you want to mark as \"x,y\": ")
        if (len(mark) == 3 and
                mark[0].isdigit() and
                mark[1] == "," and
                mark[2].isdigit()):
            mark = make_tuple(mark)
        else:
            print("Invalid input format, try again!")
            return self.user_input(player)

        if mark[0] not in self.range or mark[1] not in self.range:
            print("Invalid position, try again!\n")
            return self.user_input(player)

        if self.board[mark] != " ":
            print("Can't mark here, try again!\n")
            return self.user_input(player)

        return mark

    def __str__(self):
        string = ''
        for y in self.range:
            string += "{} ".format(y)
            for x in self.range:
                string += self.board[(x, y)]
                if x != 2:
                    string += " | "
            if y != 2:
                string += "\n" + ("  --" + "+" + "---" + "+" + "--") + "\n"
        string += "\n"
        string += "  0   1   2"
        string += "\n"
        return string


if __name__ == "__main__":
    board = {
        (0, 0): ' ', (1, 0): ' ', (2, 0): ' ',
        (0, 1): ' ', (1, 1): ' ', (2, 1): ' ',
        (0, 2): ' ', (1, 2): ' ', (2, 2): ' '
    }

    game = Game(board)
    game.game_loop('O')
