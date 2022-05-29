from colorama import Fore, Back, Style
from terminarty import Terminal, Cursor

FIELD = """
 {} │ {} │ {}
───┼───┼───
 {} │ {} │ {}
───┼───┼───
 {} │ {} │ {}
"""

terminal = Terminal()
field = [' ', ' ', ' ',
         ' ', ' ', ' ',
         ' ', ' ', ' ']
cursor_pos = 0
turn = 'X'


def draw(winners: tuple[int, int, int] = None) -> None:
    """Draws field to the terminal.."""
    Cursor.setpos(1, 1)
    edited_field = field[:]
    for i, l in enumerate(field):
        if field[i] == ' ':
            continue
        elif field[i] == 'X':
            if winners is not None and i in winners:
                edited_field[i] = Back.LIGHTRED_EX + 'X' + Style.RESET_ALL
            else:
                edited_field[i] = Fore.LIGHTRED_EX + 'X' + Style.RESET_ALL
        elif field[i] == 'O':
            if winners is not None and i in winners:
                edited_field[i] = Back.LIGHTBLUE_EX + 'O' + Style.RESET_ALL
            else:
                edited_field[i] = Fore.LIGHTBLUE_EX + 'O' + Style.RESET_ALL
    if winners is None:
        if turn == 'X':
            edited_field[cursor_pos] = Fore.LIGHTRED_EX + '█' + Style.RESET_ALL
        elif turn == 'O':
            edited_field[cursor_pos] = Fore.LIGHTBLUE_EX + '█' + Style.RESET_ALL
    print(FIELD.format(*edited_field))


def next_turn() -> None:
    """Changes turn to the other player."""
    global turn
    turn = 'O' if turn == 'X' else 'X'
    move_cursor()


def get_input() -> None:
    """Gets input from the user."""
    global field
    char = terminal.getchar()
    if char == b'\x03':
        Cursor.show()
        raise KeyboardInterrupt
    elif char == b' ':
        move_cursor()
    elif char == b'\r':
        field[cursor_pos] = turn
        next_turn()


def move_cursor() -> None:
    """Moves cursor to the next field."""
    global cursor_pos
    slice = field[cursor_pos + 1:]
    if not slice or not slice.count(' '):
        cursor_pos = 0
        if field[cursor_pos] == ' ':
            return
        else:
            slice = field[cursor_pos + 1:]
    for l in slice:
        if l == ' ':
            cursor_pos += 1
            break
        else:
            cursor_pos += 1


def win_check() -> tuple[int, int, int] or int:
    """Checks if there is a winner. Returns tuple with winning coords or -1 if draw."""
    if field[0] == field[1] == field[2] != ' ':
        return 0, 1, 2
    elif field[3] == field[4] == field[5] != ' ':
        return 3, 4, 5
    elif field[6] == field[7] == field[8] != ' ':
        return 6, 7, 8
    elif field[0] == field[3] == field[6] != ' ':
        return 0, 3, 6
    elif field[1] == field[4] == field[7] != ' ':
        return 1, 4, 7
    elif field[2] == field[5] == field[8] != ' ':
        return 2, 5, 8
    elif field[0] == field[4] == field[8] != ' ':
        return 0, 4, 8
    elif field[2] == field[4] == field[6] != ' ':
        return 2, 4, 6
    elif not field.count(' '):
        return -1


def reset_game() -> None:
    """Resets game to the initial state."""
    global field
    global cursor_pos
    global turn
    field = [' ', ' ', ' ',
             ' ', ' ', ' ',
             ' ', ' ', ' ']
    cursor_pos = 0
    turn = 'X'
    terminal.clear()
    Cursor.hide()
    draw()


def game_loop() -> None:
    """Main game loop."""
    while True:
        get_input()
        draw()
        winners = win_check()
        if winners:
            if winners == -1:
                draw((-1, -1, -1))
                print(f'{Fore.LIGHTYELLOW_EX}Draw!{Style.RESET_ALL}')
                break
            elif field[winners[0]] == 'X':
                draw(winners)
                print(f'{Fore.LIGHTRED_EX}X wins!{Style.RESET_ALL}')
                break
            elif field[winners[0]] == 'O':
                draw(winners)
                print(f'{Fore.LIGHTBLUE_EX}O wins!{Style.RESET_ALL}')
                break


def show_interface() -> None:
    """Shows the main menu interface."""
    terminal.clear()
    choise = terminal.select(f'{Fore.LIGHTGREEN_EX}Tic Tac Toe\n{Fore.RESET}', ['Start', 'Info', 'Exit'])
    if choise == 'Start':
        return
    elif choise == 'Info':
        print(f'{Fore.LIGHTGREEN_EX}Tic Tac Toe{Style.RESET_ALL} is a game for '
              f'{Fore.LIGHTRED_EX}2 players{Style.RESET_ALL}.'
              f' Each player takes a turn and marks a field on the board.\n'
              f'The first player to get {Fore.LIGHTGREEN_EX}3{Style.RESET_ALL} in a row wins.\n'
              f'Press {Fore.LIGHTBLACK_EX}SPACE{Style.RESET_ALL} to change the cursor position'
              f' and {Fore.LIGHTBLACK_EX}ENTER{Fore.RESET} to mark the field.\n')
        print(f'{Fore.LIGHTBLACK_EX}Press any key to continue...')
        terminal.getchar()
        return show_interface()
    elif choise == 'Exit':
        terminal.clear()
        exit(0)


def main() -> None:
    """Main function."""
    show_interface()
    terminal.clear()
    Cursor.hide()
    draw()
    while True:
        game_loop()
        print(f'\n{Fore.LIGHTBLACK_EX}'
              f'Press '
              f'{Style.RESET_ALL}ENTER{Fore.LIGHTBLACK_EX}'
              f' to play again or any other key to exit.{Style.RESET_ALL}')
        char = terminal.getchar()
        if char == b'\x03':
            Cursor.show()
            raise KeyboardInterrupt
        elif char == b'\r':
            reset_game()
        else:
            break
    terminal.clear()
    Cursor.show()


if __name__ == '__main__':
    main()
