import pygame
import random
import math

pygame.init()

FPS = 60

WIDTH, HEIGHT = 800, 800
ROWS = 4
COL = 4

RECT_HEIGHT = HEIGHT // ROWS # Height of each rectangle
RECT_WIDTH = WIDTH // COL # Width of each rectangle

OUTLINE_COLOR = (187, 173, 160) # Color of the outline of the rectangles
OUTLINE_THICKNESS = 10  # Thickness of the outline of the rectangles
BACKGROUND_COLOR = (205, 192, 180) # Background color of the window
FONT_COLOR = (119, 110, 101)

FONT = pygame.font.SysFont('comicsans', 60, bold=True)  # Font of the numbers
MOVE_VEL = 20   # Velocity of the movement of the numbers

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))   # Window object
pygame.display.set_caption('2048')  # Title of the window

class Tile:
    COLORS = [
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]

    def __init__(self, value, row, col):    
        self.value = value  # Value of the tile
        self.row = row  # Row of the tile
        self.col = col  # Column of the tile
        self.x = col * RECT_WIDTH   # X position of the tile
        self.y = row * RECT_HEIGHT  # Y position of the tile
        

    def get_color(self):    # Get the color of the tile based on the value
        color_index = int(math.log2(self.value)) - 1    # Calculate the index of the color based on the value
        return self.COLORS[color_index]   # Return the color based on the index
    
    def draw(self, window): # Draw the tile
        color = self.get_color() # Get the color of the tile
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))  # Draw the tile

        text = FONT.render(str(self.value), 1, FONT_COLOR) # Render the text of the value
        window.blit(text, (self.x + RECT_WIDTH // 2 - text.get_width() // 2, self.y + RECT_HEIGHT // 2 - text.get_height() // 2)) # Draw the text

    def set_pos(self, ceil= False): # Set the position of the tile
        if ceil:   # If ceil is True, round up the position
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH) 
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)
        

    def move(self,delta): # Move the tile
        self.x += delta[0] # Move the tile in the x direction
        self.y += delta[1] # Move the tile in the y direction

def draw_grid(window): # Draw the grid of the window
    for row in range(1, ROWS): # Loop through the rows
        y = row * RECT_HEIGHT   # Calculate the y position of the horizontal lines
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)  # Draw the horizontal lines

    for col in range(1, COL): # Loop through the columns
        x = col * RECT_WIDTH    # Calculate the x position of the vertical lines
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS) # Draw the vertical lines

    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS) # Draw the outline of the window

def draw(window, tiles): # Draw the window
    window.fill(BACKGROUND_COLOR) # Fill the window with the background color

    for tile in tiles.values(): # Loop through the tiles
        tile.draw(window)

    draw_grid(window) # Draw the grid
    pygame.display.update() # Update the window

def get_random_pos(tiles): # Get a random position for the tile
    row = None
    col = None
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COL)

        if f"{row}{col}" not in tiles:
            break
    
    return row, col

def move_tiles(window, tiles, clock, direction): # Move the tiles
    updated = True
    blocks = set()

    if direction == 'left': # If the direction is left
        sort_func = lambda x: x.col # Sort the tiles based on the column
        reverse = False # Reverse the sorting
        delta = (-MOVE_VEL, 0) # Set the delta of the movement
        boundary_check = lambda tile: tile.col == 0 # Check if the tile is at the boundary
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}") # Get the next tile
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL # Check if the tiles can merge
        move_check = lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL # Check if the tiles can move
        ceil = True

    elif direction == 'right':
        sort_func = lambda x: x.col
        reverse = True
        delta = (MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == COL - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
        move_check = lambda tile, next_tile: tile.x < next_tile.x - RECT_WIDTH - MOVE_VEL
        ceil = False

    elif direction == 'up':
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -MOVE_VEL)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
        move_check = lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL
        ceil = True
        
    elif direction == 'down':
        sort_func = lambda x: x.row
        reverse = True
        delta = (0, MOVE_VEL)
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
        move_check = lambda tile, next_tile: tile.y < next_tile.y - RECT_HEIGHT - MOVE_VEL
        ceil = False
    
    while updated:
        clock.tick(FPS)
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

        for i, tile in enumerate(sorted_tiles): 

            if boundary_check(tile):
                continue

            next_tile = get_next_tile(tile)

            if not next_tile:
                tile.move(delta)
            elif (tile.value == next_tile.value and next_tile not in blocks and next_tile not in blocks):

                if merge_check(tile, next_tile):
                    tile.move(delta)
                    
                else:
                    next_tile.value *= 2
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)

            elif move_check(tile, next_tile):
                tile.move(delta)
            else:
                continue
        
            tile.set_pos(ceil)
            updated = True
        update_tiles(window, tiles, sorted_tiles)
    return end_move(tiles)

def end_move(tiles):
    if len(tiles) == 16:
        return "lost"

    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue"


def update_tiles(window, tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile
    
    draw(window, tiles)

def generate_tiles():
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)

    return tiles

def main(window):               
    clock = pygame.time.Clock() # Clock object to control the FPS
    run = True  # Main loop flag
    
    tiles = generate_tiles() # Create the tiles

    while run:
        clock.tick(FPS) # Control the FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_tiles(window, tiles, clock, 'left')
                elif event.key == pygame.K_RIGHT:
                    move_tiles(window, tiles, clock, 'right')
                elif event.key == pygame.K_UP:
                    move_tiles(window, tiles, clock, 'up')
                elif event.key == pygame.K_DOWN:
                    move_tiles(window, tiles, clock, 'down')

        draw(window, tiles) # Draw the window

    pygame.quit()

if __name__ == '__main__':
    main(WINDOW)