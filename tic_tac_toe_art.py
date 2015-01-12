"""
the game art module for tic tac toe
"""
__author__ = 'Debojeet_Chatterjee'
from colorama import init, Fore, Style

init()


def print_content(content):
    """
    print a cell content
    """
    if content == 'x':
        print Fore.RED + Style.BRIGHT + "X",
    elif content == 'o':
        print Fore.GREEN + Style.BRIGHT + "O",
    elif content == 'X':
        print Fore.CYAN + Style.BRIGHT + "X",
    elif content == 'O':
        print Fore.CYAN + Style.BRIGHT + "O",
    else:
        print " ",


def print_content_row(content_row):
    """
    print a row of the board
    """
    dim = len(content_row)
    print "\t",
    print "",
    for i in range(dim-1):
        print_content(content_row[i])
        print Fore.YELLOW + Style.DIM + "|",

    print_content(content_row[dim-1]),
    print ""


def draw_game_board(board):
    """
    draws the tic tac toe board.
    need to generalise for n dim.
    """
    separator_length = 4 * board.dim - 1
    separator_row = Fore.YELLOW + Style.DIM + "\t" + "-" * separator_length
    filler_row = Fore.YELLOW + Style.DIM + "\t" + ("   " + "|") * (board.dim-1) + "   "
    print "\n\tTIC TAC TOE"
    print "\t(c) debowin\n"

    for i in range(board.dim-1):
        print filler_row
        print_content_row(board.content[i*board.dim:(i+1)*board.dim])
        print filler_row

        print separator_row

    print filler_row
    print_content_row(board.content[board.dim*(board.dim-1):])
    print filler_row

    print Fore.RESET + Style.RESET_ALL