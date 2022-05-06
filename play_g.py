import pygame
import os
from minesweeper import Game, Size
import traceback

SCREEN_SIZE = 500
MINE_SIZE = 9
NUM_MINES = 10

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode([SCREEN_SIZE, SCREEN_SIZE])

running = True

DEBUG = False
game = Game(Size(MINE_SIZE, MINE_SIZE), NUM_MINES, False, screen, SCREEN_SIZE)

game.board.display(screen)
pygame.display.flip()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            try:
                pos = pygame.mouse.get_pos()
                move_by_event = {
                        1:'click',
                        3:'flag',
                        }
                move = move_by_event.get(event.button, None)

                mine_pos_x = int(pos[0] * MINE_SIZE / SCREEN_SIZE)
                mine_pos_y = int(pos[1] * MINE_SIZE / SCREEN_SIZE)
                result = game.play_round(mine_pos_x, mine_pos_y, move)
                if result[0] != 'play':
                    running = False

                pygame.display.flip()
            except Exception:
                print(traceback.format_exc())
                running = False

game.board.debug = True
game.board.print()
pygame.display.quit()
pygame.quit()
os._exit(0)
