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

    def game_loop(self, starter, mode):
        print(self)

        current_player = starter
        while (not self.won(self.player1, self.board) and
               not self.won(self.player2, self.board) and
               not self.tied(self.board)):
            print("{}'s turn:".format(current_player))
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

        if self.tied(self.board):
            print("It's a tie!")

        elif self.won(self.player1, self.board):
            print("Player {} won".format(self.player1))

        else:
            print("Player {} won".format(self.player2))

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

            return best_move

    def move(self, player, pos):
        if pos:
            self.board[pos] = player
            print("{} marked pos: {}".format(player, pos))

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
        while True:
            pos = input("Type where you want to mark as \"x,y\": ")

            if (len(pos) == 3 and
                    pos[0].isdigit() and
                    pos[1] == "," and
                    pos[2].isdigit()):
                pos = make_tuple(pos)
            else:
                print("Invalid input format, try again!")
                continue

            if pos[0] not in self.range or pos[1] not in self.range:
                print("Invalid position, try again!\n")
                continue

            if self.board[pos] != " ":
                print("Can't mark here, try again!\n")
                continue

            break

        return pos

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
    game.game_loop('X', None)
