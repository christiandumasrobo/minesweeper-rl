import random
import pygame
# Cartesian plane

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Box:
    def __init__(self):
        self.mine = False
        self.flag = False
        self.visible = False
        self.mines_near = 0

class Board:
    def __init__(self, size, num_mines, debug, screen, screen_size):
        self.width = size.width
        self.height = size.height
        self.boxes = []
        self.debug = debug
        self.screen_size = screen_size
        self.screen = screen

        for x in range(self.width):
            self.boxes.append([])
            for y in range(self.height):
                self.boxes[-1].append(Box())

        mines = 0
        while mines < num_mines:
            mine_x = random.randint(0, self.width - 1)
            mine_y = random.randint(0, self.height - 1)
            if self.boxes[mine_x][mine_y].mine:
                continue
            self.boxes[mine_x][mine_y].mine = True
            mines += 1

    def print(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.boxes[x][y].flag:
                    print('F', end='')
                elif self.boxes[x][y].mine and self.debug:
                    print('M', end='')
                elif not self.boxes[x][y].visible:
                    print('O', end='')
                elif self.boxes[x][y].visible and self.boxes[x][y].mines_near:
                    print(self.boxes[x][y].mines_near, end='')
                elif self.boxes[x][y].visible:
                    print('C', end='')
                else:
                    print(' ', end='')
            print()

    def display(self, screen):
        box_width = int(self.screen_size / self.width)
        screen.fill(WHITE)

        for x in range(0, self.screen_size, box_width):
            pygame.draw.line(screen, BLACK, (x, 0), (x, self.screen_size))

        for y in range(0, self.screen_size, box_width):
            pygame.draw.line(screen, BLACK, (0, y), (self.screen_size, y))

        font = pygame.font.SysFont('Comic Sans MS', int(box_width))
        flag_pts = ((0, 0), (0, box_width), (box_width, box_width / 2))
        square_pts = ((0, 0), (0, box_width), (box_width, box_width), (box_width, 0))
        for y in range(self.height):
            for x in range(self.width):
                if self.boxes[x][y].flag:
                    pts = [(flag_pt[0] + x * box_width, flag_pt[1] + y * box_width) for flag_pt in flag_pts]
                    pygame.draw.polygon(screen, RED, pts)
                elif self.boxes[x][y].mine and self.debug:
                    pygame.draw.circle(screen, BLACK, (x*box_width + box_width / 2, y*box_width + box_width / 2), box_width / 2)
                elif self.boxes[x][y].visible and self.boxes[x][y].mines_near:
                    text_surface = font.render(str(self.boxes[x][y].mines_near), False, BLACK)
                    screen.blit(text_surface, (x * box_width, y * box_width))
                elif self.boxes[x][y].visible:
                    pts = [(square_pt[0] + x * box_width, square_pt[1] + y * box_width) for square_pt in square_pts]
                    pygame.draw.polygon(screen, BLACK, pts)

    # An action
    def flag(self, x, y):
        if self.boxes[x][y].visible:
            return ('play', 0)
        self.boxes[x][y].flag = not self.boxes[x][y].flag
        return ('play', 0)

    def adjacent_indices(self, x, y):
        x_left = (max(x - 1, 0), y)
        x_right = (min(x + 1, self.width - 1), y)
        y_up = (x, max(y - 1, 0))
        y_down = (x, min(y + 1, self.height - 1))
        return [x_left, x_right, y_up, y_down]

    def cardinal_indices(self, x, y):
        x_left = x - 1
        x_right = x + 1
        y_up = y - 1
        y_down = y + 1
        directions = []
        for x_it in range(x_left, x_right + 1):
            for y_it in range(y_up, y_down + 1):
                if x_it < 0 or x_it >= self.width or y_it < 0 or y_it >= self.height:
                    continue
                if not (x == x_it and y == y_it):
                    directions.append((x_it, y_it))
        return directions

    def clear_check(self, x, y):
        if self.boxes[x][y].mine:
            return

        if self.boxes[x][y].visible:
            return
        
        self.boxes[x][y].visible = True
        # Limit to only uncover squares not adjacent to mines
        for direction in self.adjacent_indices(x, y):
            if self.boxes[direction[0]][direction[1]].mine:
                return

        for direction in self.adjacent_indices(x, y):
            self.clear_check(*direction)

    def add_nums(self):
        for x in range(self.width):
            for y in range(self.height):
                num_mines = 0
                for direction in self.cardinal_indices(x, y):
                    if self.boxes[direction[0]][direction[1]].mine:
                        num_mines += 1
                self.boxes[x][y].mines_near = num_mines

    # An action
    def click(self, x, y):
        if self.boxes[x][y].visible:
            return ('play', 0)

        # Lose condition
        if self.boxes[x][y].mine:
            return ('lose', -100)

        self.clear_check(x, y)
        self.add_nums()
        self.boxes[x][y].visible = True
        if self.win():
            return ('win', 100)

        # Continue playing

        return ('play', 2)

    def win(self):
        win_condition = True
        for x in range(self.width):
            for y in range(self.height):
                if not self.boxes[x][y].visible and not self.boxes[x][y].mine:
                    win_condition = False
        return win_condition


class Game:
    def __init__(self, size, num_mines, debug=False, screen=None, screen_size=None):
        self.size = size
        self.board = Board(size, num_mines, debug, screen, screen_size)
        self.total_score = 0

    def play_round(self, x, y, move=''):
        result = ('play', 0)
        if move == 'flag':
            result = self.board.flag(x, y)
        elif move == 'quit' or move == 'exit':
            result = (lose, -100)
        else:
            result = self.board.click(x, y)

        if not self.board.screen:
            self.board.print()
        else:
            self.board.display(self.board.screen)

        return result

