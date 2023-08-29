import pygame
import time
import numpy as np

# Colours
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (10, 10, 10)
COLOR_ALIVE_NEXT = (255, 255, 255)

# Constants
W = 50 # width of grid including buffer
CELL_SIZE = 10
BORDER = 0
SLEEP_TIME = 0.1

def main():
    pygame.init()
    screen = pygame.display.set_mode((W * CELL_SIZE, W * CELL_SIZE))
    grid = np.zeros(W * W, dtype=np.uint8)
    if BORDER: screen.fill(COLOR_GRID)

    #spawnGlider(grid, 0)

    pygame.display.flip()
    pygame.display.update()

    running = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
            if not running:
                # if left click, make living cells
                if pygame.mouse.get_pressed()[0]:
                    i = get_index_from_mouse_pos(pygame.mouse.get_pos())
                    grid[i] = 1
                # if right click, make dead cells
                elif pygame.mouse.get_pressed(num_buttons=3)[2]:
                    i = get_index_from_mouse_pos(pygame.mouse.get_pos())
                    grid[i] = 0
            
        if running:
            firstGeneration(grid)
            time.sleep(SLEEP_TIME)
        
        draw_cells(screen, grid, CELL_SIZE)
        pygame.display.update()

    
def get_index_from_mouse_pos(pos):
    x = pos[0] // CELL_SIZE
    y = pos[1] // CELL_SIZE
    return y * W + x

def draw_cells(screen, grid, size):
    for x in range(grid.size):
        color = COLOR_ALIVE_NEXT if grid[x] == 1 else COLOR_DIE_NEXT
        col = x % W
        row = x // W

        pygame.draw.rect(screen, color, (col * size, row * size, size - BORDER, size - BORDER))

def num_neighbours(grid, i):
    return grid[i - W - 1]+ grid[i - W] + grid[i - W + 1] + \
            grid[i - 1] + grid[i + 1] + \
            grid[i + W - 1] + grid[i + W] + grid[i + W + 1]

def on_border(i):
    return (i < W) or (i % W == 0) or (i % W == W-1) or (i >= W*W - W)

# determine if given cell with given neighbours survives or dies
# return if this cell's state changed
def cell_changes(grid, i, n):
    if grid[i]:
        if n != 2 and n != 3:
            return 1 # live cell dies
        else:
            return 0 # live cell lives
    else:
        if n == 3:
            return 1 # dead cell lives
        else:
            return 0 # dead cell stays dead

def firstGeneration(grid):
    changes = []

    for x in range(grid.size):
        if on_border(x): continue # don't change border cells
        
        if cell_changes(grid, x, num_neighbours(grid, x)):
            changes.append(x)

    for x in range(len(changes)):
        grid[changes[x]] = not grid[changes[x]]
        

def printGrid(grid):
    output = ""

    for x in range(W):
        for y in range(W):
            output += str(grid[x * W + y]) + " "
        output += "\n"
    
    print(output)
        

##########################
# Lexicon Functions
##########################
def spawnGlider(grid, i):
    i = i + W + 1 # i = 0 positions glider at top left most spot in grid not on border
    grid[i] = grid[W + 1 + i] = grid[W + 2 + i] = grid[2 * W + i] = grid[2 * W + 1 + i] = 1



if __name__ == "__main__":
    main()