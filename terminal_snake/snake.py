import threading
from itertools import pairwise
from random import randint
from time import sleep

from colorama import Fore
from terminarty import Box, Terminal, Cursor
from terminarty.BoxStyles import Thick

WIDTH = 20
HEIGHT = 8
APPLE = '●'
SNAKE = '█'
SNAKISH = [
    SNAKE,
    Thick.HORIZONTAL_LINE,
    Thick.VERTICAL_LINE,
    'x'
]

grid = [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]
terminal = Terminal()
snake_direction = (1, 0)
snake = []
score = 0


def spawn_apple():
    """Spawns an apple on a random position on the grid."""
    while True:
        x, y = randint(0, WIDTH - 1), randint(0, HEIGHT - 1)
        if grid[y][x] == ' ':
            grid[y][x] = APPLE
            return


def spawn_snake():
    """Spawns snake on the center of the grid."""
    grid[HEIGHT // 2][WIDTH // 2] = SNAKE
    grid[HEIGHT // 2][WIDTH // 2 - 1] = SNAKE
    snake.append((WIDTH // 2, HEIGHT // 2))
    snake.append((WIDTH // 2 - 1, HEIGHT // 2))


def game_over():
    """Shows game over screen and exits the game."""
    terminal.clear()
    print(f'{Fore.LIGHTRED_EX}Game Over!')
    print(f'{Fore.RESET}Score{Fore.LIGHTBLACK_EX}:{Fore.LIGHTGREEN_EX} {score}')
    exit(0)


def move_snake():
    """Moves the snake in the direction it is facing."""
    global snake, snake_direction, score
    head = snake[0]
    x, y = head
    x += snake_direction[0]
    y += snake_direction[1]
    if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
        game_over()
    if grid[y][x] == APPLE:
        score += 1
        spawn_apple()
        snake.insert(0, (x, y))
    elif grid[y][x] in SNAKISH:
        game_over()
    else:
        snake.insert(0, (x, y))
        old_x, old_y = snake.pop()
        grid[old_y][old_x] = ' '
    for x, y in snake:
        grid[y][x] = SNAKE


def enhance_snake():
    """Makes snake look better."""
    global grid
    for a, b in pairwise(snake):
        x1, y1 = a
        x2, y2 = b
        if x1 == x2 and y1 != y2:
            grid[y2][x2] = Thick.VERTICAL_LINE
        if x1 != x2 and y1 == y2:
            grid[y2][x2] = Thick.HORIZONTAL_LINE
        if (grid[y1][x1] == Thick.HORIZONTAL_LINE and grid[y2][x2] == Thick.VERTICAL_LINE) or \
                (grid[y1][x1] == Thick.VERTICAL_LINE and grid[y2][x2] == Thick.HORIZONTAL_LINE):
            if (x1, y1) != snake[0]:
                grid[y1][x1] = 'x'
    x, y = snake[0]
    if snake_direction == (1, 0) or snake_direction == (-1, 0):
        grid[y][x] = Thick.HORIZONTAL_LINE
    elif snake_direction == (0, 1) or snake_direction == (0, -1):
        grid[y][x] = Thick.VERTICAL_LINE


def draw():
    """Draws the grid to the terminal."""
    enhance_snake()
    s = ''
    for row in grid:
        for char in row:
            s += char
        s += '\n'
    box = Box(s, color=Fore.LIGHTBLACK_EX)
    print(box, end='', flush=True)
    Cursor.setpos(1, 1)


def input_loop():
    """Handles user input."""
    global snake_direction
    while True:
        key = terminal.getchar()
        if key == b'w' and snake_direction != (0, 1):
            snake_direction = (0, -1)
        elif key == b'a' and snake_direction != (1, 0):
            snake_direction = (-1, 0)
        elif key == b's' and snake_direction != (0, -1):
            snake_direction = (0, 1)
        elif key == b'd' and snake_direction != (-1, 0):
            snake_direction = (1, 0)
        elif key == b'q':
            game_over()


def game_loop():
    """Main game loop."""
    while True:
        move_snake()
        draw()
        sleep(0.2)


def show_interface():
    """Shows the main menu interface."""
    terminal.clear()
    choise = terminal.select(f'{Fore.LIGHTGREEN_EX}Snake\n{Fore.RESET}', ['Start', 'Info', 'Exit'])
    if choise == 'Start':
        return
    elif choise == 'Info':
        print(f'Eat {Fore.LIGHTRED_EX}apples{Fore.RESET} to get {Fore.LIGHTGREEN_EX}points{Fore.LIGHTBLACK_EX}.\n'
              f'{Fore.LIGHTRED_EX}Game Over{Fore.RESET} when you touch yourself or the walls{Fore.LIGHTBLACK_EX}.\n'
              f'{Fore.RESET}Use {Fore.YELLOW}WASD {Fore.RESET}to move the snake{Fore.LIGHTBLACK_EX}.\n')
        print(f'{Fore.LIGHTBLACK_EX}Press any key to continue...')
        terminal.getchar()
        return show_interface()
    elif choise == 'Exit':
        terminal.clear()
        exit(0)


def main():
    """Main function."""
    input_thread = threading.Thread(target=input_loop, daemon=True)
    show_interface()
    spawn_snake()
    spawn_apple()
    terminal.clear()
    input_thread.start()
    game_loop()


if __name__ == '__main__':
    main()
