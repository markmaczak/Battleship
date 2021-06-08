import os
import string

# os.system('clear')


def clear_screen():
    # if os.name == 'nt':
    #     os.system('cls')
    # else:
    #     os.system('clear')
    
    os.system('cls' if os.name == 'nt' else 'clear')

# a = 10
# b = 0

# def fii():
#     return 10

# def foo():
#     return 10

# if a == 10:
#     fii()
# else:
#     foo()

# b = 100 if a == 10 else -100


def init_board(n):
    board = []
    for i in range(0, n):
        board.append(['0']*n)
    return board

    # return [['0' for _ in range(n)] for _ in range(n)]


def print_board(board, player):
    n = len(board)
    row_id = list(string.ascii_uppercase[:n])
    col_id = [str(number) for number in range(1, n + 1)]
    header = '   ' + '  '.join(col_id).ljust(3 * n + 1)
    separator = '  ' + '-'*(3 * n)
    to_be_printed = ['']

    to_be_printed.append(f'   PLAYER {player}')
    to_be_printed.append('')
    to_be_printed.append(header)
    to_be_printed.append(separator)
    for row_index in range(n):
        line = row_id[row_index] + "| "
        for col_index in range(n):
            line += (board[row_index][col_index] + "  ")
        to_be_printed.append(line)
    to_be_printed.append(separator)

    for i in range(n + 6):
        print(to_be_printed[i])


def print_both_boards(board1, board2):
    n = len(board1)
    row_id = list(string.ascii_uppercase[:n])
    col_id = [str(number) for number in range(1, n + 1)]
    header = '   ' + '  '.join(col_id).ljust(3 * n + 1)
    separator = '  ' + '-'*(3 * n)
    to_be_printed = ['']
    to_be_printed.append('   PLAYER 1'.ljust(3 * n + 6) + '   PLAYER 2')
    to_be_printed.append('')
    to_be_printed.append(header + '  ' + header)
    to_be_printed.append(separator + '    ' + separator)
    for row_index in range(n):
        line = row_id[row_index] + "| "
        for col_index in range(n):
            if board1[row_index][col_index] == 'X':
                line += ('0' + "  ")
            else:
                line += (board1[row_index][col_index] + "  ")
        line += '   ' + row_id[row_index] + "| "
        for col_index in range(n):
            if board2[row_index][col_index] == 'X':
                line += ('0' + "  ")
            else:
                line += (board2[row_index][col_index] + "  ")
        to_be_printed.append(line)
    to_be_printed.append(separator + '    ' + separator)
    for i in range(n + 6):
        print(to_be_printed[i])


def place_ships(board, player, game_options):
    # os.system('clear')
    clear_screen()
    small_ships = game_options["small_ships"]
    large_ships = game_options["large_ships"]

    print(f'\nPlayer {player} please place your ships!\n')
    print_board(board, player)

    for i in range(large_ships):
        direction = ''
        while direction != 'H' and direction != 'V':
            direction = input('\nDo you want to place the large ship horizontally or vertically? Enter H or V! ').upper()
        valid_placement = False
        print('\nLarge ships shall be placed by choosing the upper left position.')
        while not valid_placement:
            row, col = input_coordinates(board, direction)
            if direction == 'H':
                second_row = row
                second_col = col + 1
            elif direction == 'V':
                second_row = row + 1
                second_col = col
            if board[row][col] != '0':
                print(f'\nThere is a ship at {string.ascii_uppercase[row]}{col + 1} already. Please choose a different position')
            elif board[second_row][second_col] != '0':
                print(f'\nThere is a ship at {string.ascii_uppercase[second_row]}{second_col + 1} already. Please choose a different position')
            elif check_neighbours(board, row, col) is None and check_neighbours(board, second_row, second_col) is None:
                board[row][col] = 'X'
                board[second_row][second_col] = 'X'
                valid_placement = True
            else:
                print('\nYou have placed a ship close by! Please leave at least 1 space between ships')
        print_board(board, player)

    for i in range(small_ships):
        valid_placement = False
        while not valid_placement:
            print('\nPlace a small ship!')
            row, col = input_coordinates(board)
            if board[row][col] != '0':
                print(f'\nThere is a ship at {string.ascii_uppercase[row]}{col + 1} already. Please choose a different position')
            elif board[row][col] == '0' and check_neighbours(board, row, col) is None:
                board[row][col] = 'X'
                valid_placement = True
            else:
                print('\nYou have placed a ship close by! Please leave at least 1 space between ships')
        print_board(board, player)
    return board


def input_coordinates(board, direction=None):
    max_x = len(board)
    max_y = len(board)
    if direction == 'H':
        max_x -= 1
    elif direction == 'V':
        max_y -= 1
    valid_coordinates = False
    while not valid_coordinates:
        coordinates = input('\nPlease enter coordinates: ')
        if len(coordinates) >= 2 and coordinates[0].upper() in string.ascii_uppercase[:max_y] and int(coordinates[1:]) in range(1, max_x+1):
            row = string.ascii_uppercase.find(coordinates[0].upper())
            col = int(coordinates[1:]) - 1
            valid_coordinates = True
        else:
            print('\nThese are not valid coordinates.')
    return row, col


def check_neighbours(board, row, col):
    n = len(board[0])
    if row > 0 and (board[row - 1][col] == 'X' or board[row - 1][col] == 'H'):
        return row - 1, col
    if row < n - 1 and (board[row + 1][col] == 'X' or board[row + 1][col] == 'H'):
        return row + 1, col
    if col > 0 and (board[row][col - 1] == 'X' or board[row][col - 1] == 'H'):
        return row, col - 1
    if col < n - 1 and (board[row][col + 1] == 'X' or board[row][col + 1] == 'H'):
        return row, col + 1


def shooting(board, player):
    print(f'\n Player {player}, please, choose target position!')
    valid_target = False
    while not valid_target:
        row, col = input_coordinates(board)
        if board[row][col] == '0' or board[row][col] == 'X':
            valid_target = True
        else:
            print('\nYou have already shot there. Choose another target!')
    # os.system('clear')
    clear_screen()
    if board[row][col] == 'X' and not check_neighbours(board, row, col):
        board[row][col] = 'S'
        print('\nYou have sunk a ship!')
    elif board[row][col] == 'X':
        nrow, ncol = check_neighbours(board, row, col)
        if board[nrow][ncol] == 'H':
            board[row][col] = 'S'
            board[nrow][ncol] = 'S'
            print('\nYou have sunk a ship!')
        else:
            board[row][col] = 'H'
            print('\nYou have hit a ship!')
    else:
        board[row][col] = 'M'
        print('\nYou have missed!')
    return board


def check_winner(board, player):
    winner = player
    for row in board:
        if 'X' in row:
            winner = -1
    return winner


def battle(board1, board2, turn):
    # os.system('clear')
    clear_screen()
    winner = -1
    countdown = int(turn)
    while countdown > 0:
        print_both_boards(board1, board2)
        shooting(board2, 1)
        print(f'\nTurns left: {countdown}')
        winner = check_winner(board2, 1)
        if winner >= 0:
            print_both_boards(board1, board2)
            return winner
        print_both_boards(board1, board2)
        shooting(board1, 2)
        countdown = countdown - 1
        print(f'\nTurns left: {countdown}')
        winner = check_winner(board1, 2)
        if winner >= 0:
            print_both_boards(board1, board2)
            return winner
    winner = 0
    return winner


def game_logic(game_options):
    n = game_options["size"]
    turn = game_options["turn"]
    board1 = place_ships(init_board(n), 1, game_options)
    input('\nPress ENTER for player2 to place the ships!')
    board2 = place_ships(init_board(n), 2, game_options)
    input('\nPress ENTER to start the battle!')
    winner = battle(board1, board2, turn)
    if winner == 0:
        print("\nIt's a tie.")
    else:
        print(f'\nPlayer {winner} wins')


def menu():
    print('\n                         WELCOME TO')
    print('''
    ____  ___  ______________    ___________ __  __________
   / __ )/   |/_  __/_  __/ /   / ____/ ___// / / /  _/ __ \\
  / __  / /| | / /   / / / /   / __/  \\__ \\/ /_/ // // /_/ /
 / /_/ / ___ |/ /   / / / /___/ /___ ___/ / __  // // ____/
/_____/_/  |_/_/   /_/ /_____/_____//____/_/ /_/___/_/
⚓ ⚓ ⚓ ⚓ ⚓ ⚓ ⚓ ⚓ ⚓ ⚓ ⚓ ⚓ ⚓ ⚓ ⚓ ⚓ ⚓ ⚓ ⚓ ⚓
''')
    n = 0
    turn = 0
    while not (n >= 5 and n <= 10):
        try:
            n = int(input('\nPlease choose table size (5 - 10): '))
        except ValueError:
            print('\nPlease enter only numbers!')
    while not (turn >= 5 and turn <= 50):
        try:
            turn = int(input('\nPlease choose number of turns (5 - 50): '))
        except ValueError:
            print('\nPlease choose number between 5 and 50!')
    game_options = {}
    game_options["size"] = n
    game_options["turn"] = turn

    large_ships = 0
    while not (large_ships >= 1 and large_ships <= n ** 2 // 12):
        try:
            large_ships = int(input(f'\nHow many large (duble unit) ships do you want (1 - {n ** 2 // 12})? '))
        except ValueError:
            print('\nPlease, only enter numbers')
    game_options["large_ships"] = large_ships

    small_ships = 0
    while not (small_ships >= 1 and small_ships <= n ** 2 // 12):
        try:
            small_ships = int(input(f'\nHow many small (single unit) ships do you want (1 - {(n ** 2 - large_ships * 6) // 6})! '))
        except ValueError:
            print('\nPlease, only enter numbers')
    game_options["large_ships"] = large_ships
    game_options["small_ships"] = small_ships
    return game_options


def main():
    clear_screen()
    new_game = True
    while new_game:
        game_options = menu()
        game_logic(game_options)
        answer = ''
        while answer != 'Y' and answer != 'N':
            answer = input('\nDo you want to play again? Enter Y or N! ').upper()
        if answer == 'N':
            print('\nGood bye!')
            new_game = False


if __name__ == "__main__":
    main()