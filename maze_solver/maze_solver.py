from queue import Queue
from typing import Optional

from PIL import Image
from colorama import Fore, Style
from terminarty import Terminal, Waiting

# Text options
WHITESPACE = ' '
WALL = '#'
START = 'O'
FINISH = 'X'
PATH = '@'

# Color options
WHITESPACE_COLOR = (255, 255, 255)
WALL_COLOR = (0, 0, 0)
START_COLOR = (0, 255, 0)
FINISH_COLOR = (255, 0, 0)
PATH_COLOR = (0, 255, 0)

terminal: Terminal = ...


class InvalidMaze(Exception):
    pass


# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def load(filepath: str) -> list[list[str]]:
    """Loads maze from given file path."""
    img = Image.open(filepath)
    img = img.convert('RGB')
    maze = []
    for clr in img.getdata():
        if clr == WHITESPACE_COLOR:
            maze.append(WHITESPACE)
        elif clr == WALL_COLOR:
            maze.append(WALL)
        elif clr == START_COLOR:
            maze.append(START)
        elif clr == FINISH_COLOR:
            maze.append(FINISH)
        else:
            raise InvalidMaze(f'Unknown color: {clr}')
    return list(chunks(maze, img.width))


def find_neigbours(maze: list[list[str]], pos: tuple[int, int]) -> list[tuple[int, int]]:
    """Finds all neigbours of given position."""
    neighbours = []
    if pos[0] > 0 and maze[pos[0] - 1][pos[1]] in (WHITESPACE, FINISH):  # Up
        neighbours.append((pos[0] - 1, pos[1]))
    if pos[0] < len(maze) - 1 and maze[pos[0] + 1][pos[1]] in (WHITESPACE, FINISH):  # Down
        neighbours.append((pos[0] + 1, pos[1]))
    if pos[1] > 0 and maze[pos[0]][pos[1] - 1] in (WHITESPACE, FINISH):  # Left
        neighbours.append((pos[0], pos[1] - 1))
    if pos[1] < len(maze[0]) - 1 and maze[pos[0]][pos[1] + 1] in (WHITESPACE, FINISH):  # Right
        neighbours.append((pos[0], pos[1] + 1))
    return neighbours


def find_path(maze: list[list[str]]) -> Optional[list[tuple[int, int]]]:
    """Finds path in given maze."""
    start_pos = finish_pos = (0, 0)
    visited = set()
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == START:
                start_pos = (r, c)
            elif maze[r][c] == FINISH:
                finish_pos = (r, c)
    queue = Queue()
    queue.put((start_pos, [start_pos]))
    while not queue.empty():
        pos, path = queue.get()
        visited.add(pos)
        if pos == finish_pos:
            return path
        for neighbour in find_neigbours(maze, pos):
            if neighbour in visited:
                continue
            queue.put((neighbour, path + [neighbour]))
    return None


def draw(maze: list[list[str]], path: list[tuple[int, int]], filepath: str) -> None:
    """Creates new image and draws given maze and path on it."""
    img = Image.new('RGB', (len(maze[0]), len(maze)), WHITESPACE_COLOR)
    for r, c in path:
        maze[r][c] = PATH
    for r in range(len(maze)):
        for c in range(len(maze[r])):
            if maze[r][c] == WHITESPACE:
                continue
            elif maze[r][c] == WALL:
                img.putpixel((c, r), WALL_COLOR)
            elif maze[r][c] == START:
                img.putpixel((c, r), START_COLOR)
            elif maze[r][c] == FINISH:
                img.putpixel((c, r), FINISH_COLOR)
            if maze[r][c] == PATH:
                img.putpixel((c, r), PATH_COLOR)
    img.save(f'solved_{filepath}')


def main():
    """Main function."""
    global terminal
    terminal = Terminal()
    filepath = terminal.input('Enter maze path: ')
    with Waiting('Loading maze...'):
        maze = load(filepath)
    with Waiting('Finding path...'):
        path = find_path(maze)
    if path is None:
        print(f'{Fore.RED}No path was found :({Style.RESET_ALL}')
    else:
        print(f'Found path with length of {Fore.LIGHTBLUE_EX}{len(path)}{Style.RESET_ALL}')
    with Waiting('Drawing...'):
        draw(maze, path, filepath)


if __name__ == '__main__':
    main()
