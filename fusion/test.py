# a pygame system that creates a 10x10 grid of squares that can be clicked on
# and change color when clicked on

import pygame
import sys
import random

# initialize pygame
pygame.init()

# set up display

ROWS, COLS = 7, 16
AROWS, ACOLS = 1, 2
aposr, aposc = 10,3
WIDTH, HEIGHT = (COLS*50), (ROWS*50)

SQUARE_SIZE = WIDTH // COLS
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid")

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLORS = [RED, GREEN, BLUE]

# grid
grid = [[random.choice(COLORS) for _ in range(COLS)] for _ in range(ROWS)]

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(WIN, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),10)
    pygame.draw.rect(WIN, RED, (aposc * SQUARE_SIZE, aposr * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),10)
            
def get_square(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def change_color(row, col):
    # grid[row][col] = random.choice(COLORS)
    grid[row][col] = RED
    
def main():
    run = True
    global aposr, aposc
    while run:
        WIN.fill(WHITE)
        draw_grid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_square(pos)
                change_color(row, col)
                aposr, aposc = row, col
        pygame.display.update()
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()
    
    
