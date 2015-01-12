"""
the play module for tic tac toe.
"""
import random

__author__ = 'Debojeet_Chatterjee'
import tic_tac_toe_art

ROSTER = ['PLAYER', 'CPU']
# The size of one dimension of tic tac toe board [IDEALLY AN ODD INTEGER]
DIMENSION = 3


class Board(object):

    """
    the board class contains all info about the game board.
    """
    def __init__(self, dim):
        self.dim = dim
        self.content = [' '] * self.dim ** 2
        self.player = ""
        self.cpu = ""
        # columns, rows, diagonals
        self.track_moves = [[0, 0] for i in range((self.dim+1)*2)]
        # left to right diagonal indices
        lr_diagonal_list = [i for i in range(self.dim**2) if i % self.dim == i / self.dim]
        # right to left diagonal indices
        rl_diagonal_list = [i for i in range(self.dim**2) if self.dim-1-(i % self.dim) == i / self.dim]
        self.diagonal_indices = (lr_diagonal_list, rl_diagonal_list)

    def load_symbols(self, symbols):
        """
        load the game symbols into the respective locations.
        """
        self.player, self.cpu = symbols

    def move_possible(self, position):
        """
        return true if the position[1-DIMENSION^2] can be occupied.
        """
        if self.content[position-1] == ' ':
            return True
        else:
            return False

    def column_members(self, column_id):
        """
        Returns the indices of members of given column.
        """
        members = []
        member_id = column_id
        for i in range(self.dim):
            members.append(member_id)
            member_id += self.dim
        return members

    def row_members(self, row_id):
        """
        Returns the indices of members of given row.
        """
        members = []
        member_id = row_id * self.dim
        for i in range(self.dim):
            members.append(member_id)
            member_id += 1
        return members

    def make_move(self, position, who):
        """
        make a move by 'who' on the requested position[1-DIMENSION^2].
        update the move tracker accordingly.
        """
        i = (position-1) % self.dim
        j = (position-1) / self.dim
        if who == ROSTER[1]:
            self.content[position-1] = self.cpu
            # update the tracker for column
            self.track_moves[i][1] += 1
            # update the tracker for row
            self.track_moves[j+self.dim][1] += 1
            # update the tracker for diagonals
            if position-1 in self.diagonal_indices[0]:
                self.track_moves[-2][1] += 1
            if position-1 in self.diagonal_indices[1]:
                self.track_moves[-1][1] += 1
        else:
            self.content[position-1] = self.player
            # update the tracker for column
            self.track_moves[i][0] += 1
            # update the tracker for row
            self.track_moves[j+self.dim][0] += 1
            # update the tracker for diagonals
            if position-1 in self.diagonal_indices[0]:
                self.track_moves[-2][0] += 1
            if position-1 in self.diagonal_indices[1]:
                self.track_moves[-1][0] += 1
        # print self.track_moves

    def game_won(self, last_position):
        """
        checks if the game is won and returns the winner.
        to narrow down the evaluation, the last position played is used.
        """
        i = (last_position-1) % self.dim
        j = (last_position-1) / self.dim
        for who in range(2):
            if self.track_moves[i][who] == self.dim:  # column win
                self.repaint_win(i)
                return who
            if self.track_moves[j+self.dim][who] == self.dim:  # row win
                self.repaint_win(j+self.dim)
                return who
            if self.track_moves[-2][who] == self.dim:  # lr diagonal win
                self.repaint_win(-2)
                return who
            if self.track_moves[-1][who] == self.dim:  # rl diagonal win
                self.repaint_win(-1)
                return who
        return False

    def draw(self, turn):
        """
        return true if the game is a draw.
        slightly intuitive: doesn't wait for game to end.
        """
        moves_left = "".join(self.content).count(' ')
        for move in self.track_moves:
            if 0 in move:
                if moves_left == 1 and move[turn] == 0:
                    return True
                # if game can be won in subsequent moves.
                return False
            # predict a draw
        return True

    def win_likely(self, who):
        """
        returns the tracker id if game can be won in next turn by 'who'.
        return -1 otherwise.
        """
        who = ROSTER.index(who)
        for i in range(len(self.track_moves)):
            if self.track_moves[i][who] == self.dim - 1 and self.track_moves[i][(who+1) % 2] == 0:
                return i
        return -1

    def repaint_win(self, tracker_id):
        """
        uses the tracker id to change the winning sequence
        so that it is shown in a different color.
        """
        if tracker_id == -2:
            members = self.diagonal_indices[0]
        elif tracker_id == -1:
            members = self.diagonal_indices[1]
        elif tracker_id < self.dim:
            members = self.column_members(tracker_id)
        elif tracker_id < 2*self.dim:
            members = self.row_members(tracker_id - self.dim)
        for member in members:
            self.content[member] = self.content[member].upper()


def who_plays_first():
    """
    randomly picks who makes the first move.
    """
    return random.randint(0, 1)


def get_player_symbol():
    """
    ask the player which symbol they'd like to use.
    """
    while True:
        symbol = raw_input("X or O? ").lower()
        if symbol == 'x':
            return 'x', 'o'
        elif symbol == 'o':
            return 'x', 'o'
        print "Invalid Input."


def player_input():
    """
    accept a position[1-DIMENSION^2] from the player.
    """
    while True:
        try:
            position = int(raw_input("Enter position[1-%d]: " % DIMENSION**2))
            if 0 < position < DIMENSION**2+1:
                return position
        except ValueError:
            pass


def cpu_critical_move(board, tracker_id):
    """
    CPU's critical move for when it can either win or lose in the next turn.
    """
    if tracker_id < board.dim:
        # column victory
        members = board.column_members(tracker_id)
    elif tracker_id < 2*board.dim:
        # row victory
        members = board.row_members(tracker_id-board.dim)
    else:
        # diagonal victory
        tracker_id -= 2*board.dim
        members = board.diagonal_indices[tracker_id]
    return cpu_standard_move(board, members)


def cpu_standard_move(board, position_list):
    """
    CPU's standard move for the game.
    """
    for member in position_list:
        position = member + 1
        if board.move_possible(position):
            board.make_move(position, ROSTER[1])
            return position


def cpu_turn(board):
    """
    The "AI" code of the game.
    """
    tracker_id = board.win_likely('CPU')
    if tracker_id != -1:
        # go ftw
        return cpu_critical_move(board, tracker_id)

    tracker_id = board.win_likely('PLAYER')
    if tracker_id != -1:
        # interfere
        return cpu_critical_move(board, tracker_id)

    # take priority positions:
    # take center
    if board.dim % 2 == 1:
        center = (board.dim**2)/2
        if cpu_standard_move(board, [center]):
            return center + 1
    # take diagonal_positions
    diagonal_positions = []
    diagonal_positions.extend(board.diagonal_indices[0])
    diagonal_positions.extend(board.diagonal_indices[1])
    diagonal_positions = set(diagonal_positions)
    try:
        # don't check center again.
        diagonal_positions.remove(center-1)
    except Exception:
        # for even dimension size(no center).
        pass
    move_position = cpu_standard_move(board, diagonal_positions)
    if move_position:
        # if move has been made, return position.
        return move_position

    # take anything
    remaining_positions = set(range(1, len(board.content)+1))
    # don't check diagonal elements again
    remaining_positions.difference(diagonal_positions)
    return cpu_standard_move(board, remaining_positions)


def main():
    """
    main function
    """
    board = Board(DIMENSION)
    symbols = get_player_symbol()
    board.load_symbols(symbols)
    turn = who_plays_first()
    print '%s goes first.' % ROSTER[turn]
    while True:
        if turn == 0:
            tic_tac_toe_art.draw_game_board(board)
            print "Your Turn."
            while True:
                position = player_input()
                if board.move_possible(position):
                    board.make_move(position, ROSTER[turn])
                    break
                print "Move not possible."
            if board.game_won(position):
                tic_tac_toe_art.draw_game_board(board)
                print "Congrats! You win."
                break
        else:
            print "CPU's Turn.",
            position = cpu_turn(board)
            print "[%d]" % position
            if board.game_won(position):
                tic_tac_toe_art.draw_game_board(board)
                print "Game Over! You lose."
                break
        turn = (turn + 1) % 2
        if board.draw(turn):
            tic_tac_toe_art.draw_game_board(board)
            print "Game's a Draw!"
            break
    raw_input("Press ENTER.")


if __name__ == "__main__":
    main()
