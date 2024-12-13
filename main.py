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
MOVE_VEL = 50   # Velocity of the movement of the numbers

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))   # Window object
pygame.display.set_caption('2048')  # Title of the window

# Load sound effects
WIN_SOUND = pygame.mixer.Sound('win.mp3')
LOSE_SOUND = pygame.mixer.Sound('lose.mp3')

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
        (237, 200, 80),
        (237, 197, 63),
        (237, 194, 46),
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

def draw_pause_menu(window):
    window.fill(BACKGROUND_COLOR)
    
    title_font = pygame.font.SysFont('comicsans', 100, bold=True)
    button_font = pygame.font.SysFont('comicsans', 60)
    
    title_text = title_font.render("Paused", 1, FONT_COLOR)
    resume_text = button_font.render("RESUME", 1, FONT_COLOR)
    restart_text = button_font.render("RESTART", 1, FONT_COLOR)
    main_menu_text = button_font.render("MAIN MENU", 1, FONT_COLOR)
            
    title_y = HEIGHT // 4
    button_y = HEIGHT // 2 - 50

    resume_button = pygame.Rect(WIDTH // 2 - 150, button_y, 300, 60)
    restart_button = pygame.Rect(WIDTH // 2 - 150, button_y + 100, 300, 60)
    main_menu_button = pygame.Rect(WIDTH // 2 - 150, button_y + 200, 300, 60)
    
    mouse_pos = pygame.mouse.get_pos()
    
    if resume_button.collidepoint(mouse_pos):
        pygame.draw.rect(window, (150, 150, 150), resume_button)
    else:
        pygame.draw.rect(window, OUTLINE_COLOR, resume_button)
    
    if restart_button.collidepoint(mouse_pos):
        pygame.draw.rect(window, (150, 150, 150), restart_button)
    else:
        pygame.draw.rect(window, OUTLINE_COLOR, restart_button)
    
    if main_menu_button.collidepoint(mouse_pos):
        pygame.draw.rect(window, (150, 150, 150), main_menu_button)
    else:
        pygame.draw.rect(window, OUTLINE_COLOR, main_menu_button)
    
    window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, title_y))
    window.blit(resume_text, (resume_button.x + resume_button.width // 2 - resume_text.get_width() // 2, resume_button.y + resume_button.height // 2 - resume_text.get_height() // 2))
    window.blit(restart_text, (restart_button.x + restart_button.width // 2 - restart_text.get_width() // 2, restart_button.y + restart_button.height // 2 - restart_text.get_height() // 2))
    window.blit(main_menu_text, (main_menu_button.x + main_menu_button.width // 2 - main_menu_text.get_width() // 2, main_menu_button.y + main_menu_button.height // 2 - main_menu_text.get_height() // 2))
    
    pygame.display.update()

def draw_game_over(window, background):
    window.blit(background, (0, 0))  # Use the captured background image
    
    title_font = pygame.font.SysFont('comicsans', 100, bold=True)
    button_font = pygame.font.SysFont('comicsans', 60)
    
    title_text = title_font.render("Game Over", 1, FONT_COLOR)
    title_outline = title_font.render("Game Over", 1, (0, 0, 0))  # Black outline
    restart_text = button_font.render("RESTART", 1, FONT_COLOR)
    main_menu_text = button_font.render("MAIN MENU", 1, FONT_COLOR)

    title_y = HEIGHT // 4
    button_y = HEIGHT // 2 - 50

    restart_button = pygame.Rect(WIDTH // 2 - 150, button_y, 300, 60)
    main_menu_button = pygame.Rect(WIDTH // 2 - 150, button_y + 100, 300, 60)
    
    mouse_pos = pygame.mouse.get_pos()
    
    if restart_button.collidepoint(mouse_pos):
        pygame.draw.rect(window, (150, 150, 150), restart_button)
    else:
        pygame.draw.rect(window, OUTLINE_COLOR, restart_button)
    
    if main_menu_button.collidepoint(mouse_pos):
        pygame.draw.rect(window, (150, 150, 150), main_menu_button)
    else:
        pygame.draw.rect(window, OUTLINE_COLOR, main_menu_button)
    
    # Draw the outline first
    window.blit(title_outline, (WIDTH // 2 - title_outline.get_width() // 2 - 2, title_y - 2))
    window.blit(title_outline, (WIDTH // 2 - title_outline.get_width() // 2 + 2, title_y - 2))
    window.blit(title_outline, (WIDTH // 2 - title_outline.get_width() // 2 - 2, title_y + 2))
    window.blit(title_outline, (WIDTH // 2 - title_outline.get_width() // 2 + 2, title_y + 2))
    
    # Draw the title text
    window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, title_y))
    window.blit(restart_text, (restart_button.x + restart_button.width // 2 - restart_text.get_width() // 2, restart_button.y + restart_button.height // 2 - restart_text.get_height() // 2))
    window.blit(main_menu_text, (main_menu_button.x + main_menu_button.width // 2 - main_menu_text.get_width() // 2, main_menu_button.y + main_menu_button.height // 2 - main_menu_text.get_height() // 2))
    
    pygame.display.update()

def game_over_menu(window, background):
    run = True
    LOSE_SOUND.play()  # Play lose sound
    while run:
        draw_game_over(window, background)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return "quit"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                restart_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 60)
                main_menu_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 60)
                
                if restart_button.collidepoint(mouse_pos):
                    return "restart"
                if main_menu_button.collidepoint(mouse_pos):
                    return "main_menu"

def get_random_pos(tiles): # Get a random position for the tile
    row = None
    col = None
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COL)

        if f"{row}{col}" not in tiles:
            break
    
    return row, col

def merge_check(tile, next_tile, delta):
    if delta[0] != 0:  # Horizontal movement
        return abs(tile.x - next_tile.x) <= MOVE_VEL
    else:  # Vertical movement
        return abs(tile.y - next_tile.y) <= MOVE_VEL

def animate_merge(window, tile, next_tile, delta, clock, tiles):
    merge_delta = (delta[0] * 1.5, delta[1] * 1.5)  # Increase the speed of the merge animation
    while not merge_check(tile, next_tile, merge_delta):
        tile.move(merge_delta)
        tile.set_pos()
        draw(window, tiles)
        clock.tick(FPS)
    draw(window, tiles)  # Ensure final position is drawn

def move_tiles(window, tiles, clock, direction): # Move the tiles
    updated = True
    blocks = set() # Set of the tiles that have been merged
    moved = False

    if direction == 'left': # If the direction is left
        sort_func = lambda x: x.col # Sort the tiles based on the column
        reverse = False # Reverse the sorting
        delta = (-MOVE_VEL, 0) # Set the delta of the movement
        boundary_check = lambda tile: tile.col == 0 # Check if the tile is at the boundary
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}") # Get the next tile
        move_check = lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL # Check if the tiles can move
        ceil = True

    elif direction == 'right':
        sort_func = lambda x: x.col
        reverse = True
        delta = (MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == COL - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        move_check = lambda tile, next_tile: tile.x < next_tile.x - RECT_WIDTH - MOVE_VEL
        ceil = False

    elif direction == 'up':
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -MOVE_VEL)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        move_check = lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL
        ceil = True
        
    elif direction == 'down':
        sort_func = lambda x: x.row
        reverse = True
        delta = (0, MOVE_VEL)
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
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
                moved = True
            elif (tile.value == next_tile.value and tile not in blocks and next_tile not in blocks):

                if merge_check(tile, next_tile, delta):
                    tile.move(delta)
                    moved = True
                else:
                    # Animate the merging move
                    animate_merge(window, tile, next_tile, delta, clock, tiles)
                    next_tile.value *= 2
                    sorted_tiles.pop(i)
                    blocks.add(tile)
                    blocks.add(next_tile)
                    moved = True
                    
            elif move_check(tile, next_tile):
                tile.move(delta)
                moved = True
            else:
                continue
        
            tile.set_pos(ceil)
            updated = True
        update_tiles(window, tiles, sorted_tiles)
    
    if moved:
        return end_move(tiles)
    if len(tiles) == ROWS * COL and not can_move_or_merge(tiles):
        return "lost"
    return "continue"

def can_move_or_merge(tiles):
    for tile in tiles.values():
        # Check if any adjacent tiles can be merged
        for delta in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor_row = tile.row + delta[0]
            neighbor_col = tile.col + delta[1]
            neighbor_key = f"{neighbor_row}{neighbor_col}"
            if neighbor_key in tiles and tiles[neighbor_key].value == tile.value:
                return True
    return False

def end_move(tiles):
    if len(tiles) == ROWS * COL and not can_move_or_merge(tiles):
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

def draw_main_menu(window):
    window.fill(BACKGROUND_COLOR)
    
    title_font = pygame.font.SysFont('comicsans', 100, bold=True)
    button_font = pygame.font.SysFont('comicsans', 60)
    
    title_text = title_font.render("2048", 1, FONT_COLOR)
    play_text = button_font.render("PLAY", 1, FONT_COLOR)
    quit_text = button_font.render("QUIT", 1, FONT_COLOR)

    play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 60)
    quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 60)

    mouse_pos = pygame.mouse.get_pos()

    if play_button.collidepoint(mouse_pos):
        pygame.draw.rect(window, (150, 150, 150), play_button)
    else:
        pygame.draw.rect(window, OUTLINE_COLOR, play_button)
    
    if quit_button.collidepoint(mouse_pos):
        pygame.draw.rect(window, (150, 150, 150), quit_button)
    else:
        pygame.draw.rect(window, OUTLINE_COLOR, quit_button)
    
    window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
    window.blit(play_text, (play_button.x + play_button.width // 2 - play_text.get_width() // 2, play_button.y + play_button.height // 2 - play_text.get_height() // 2))
    window.blit(quit_text, (quit_button.x + quit_button.width // 2 - quit_text.get_width() // 2, quit_button.y + quit_button.height // 2 - quit_text.get_height() // 2))

    pygame.display.update()

def draw_win_screen(window, background):
    window.blit(background, (0, 0))  # Use the captured background image
    
    title_font = pygame.font.SysFont('comicsans', 100, bold=True)
    button_font = pygame.font.SysFont('comicsans', 60)
    
    title_text = title_font.render("YOU WIN!", 1, FONT_COLOR)
    restart_text = button_font.render("RESTART", 1, FONT_COLOR)
    main_menu_text = button_font.render("MAIN MENU", 1, FONT_COLOR)

    title_y = HEIGHT // 4
    button_y = HEIGHT // 2 - 50

    restart_button = pygame.Rect(WIDTH // 2 - 150, button_y, 300, 60)
    main_menu_button = pygame.Rect(WIDTH // 2 - 150, button_y + 100, 300, 60)
    
    mouse_pos = pygame.mouse.get_pos()
    
    if restart_button.collidepoint(mouse_pos):
        pygame.draw.rect(window, (150, 150, 150), restart_button)
    else:
        pygame.draw.rect(window, OUTLINE_COLOR, restart_button)
    
    if main_menu_button.collidepoint(mouse_pos):
        pygame.draw.rect(window, (150, 150, 150), main_menu_button)
    else:
        pygame.draw.rect(window, OUTLINE_COLOR, main_menu_button)
    
    window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, title_y))
    window.blit(restart_text, (restart_button.x + restart_button.width // 2 - restart_text.get_width() // 2, restart_button.y + restart_button.height // 2 - restart_text.get_height() // 2))
    window.blit(main_menu_text, (main_menu_button.x + main_menu_button.width // 2 - main_menu_text.get_width() // 2, main_menu_button.y + main_menu_button.height // 2 - main_menu_text.get_height() // 2))
    
    pygame.display.update()

def win_menu(window, background):
    run = True
    WIN_SOUND.play()  # Play win sound
    while run:
        draw_win_screen(window, background)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return "quit"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                restart_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 60)
                main_menu_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 60)
                
                if restart_button.collidepoint(mouse_pos):
                    return "restart"
                if main_menu_button.collidepoint(mouse_pos):
                    return "main_menu"

def check_win(tiles):
    for tile in tiles.values():
        if tile.value == 2048:
            return True
    return False

def main_menu(window):
    run = True
    while run:
        draw_main_menu(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 60)
                quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 60)
                
                if play_button.collidepoint(mouse_pos):
                    return True  # Start a new game
                if quit_button.collidepoint(mouse_pos):
                    run = False
                    pygame.quit()
                    return False

def pause_menu(window):
    run = True
    while run:
        draw_pause_menu(window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return "quit"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                resume_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 300, 60)
                restart_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 50, 300, 60)
                main_menu_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 150, 300, 60)
                
                if resume_button.collidepoint(mouse_pos):
                    return "resume"
                if restart_button.collidepoint(mouse_pos):
                    return "restart"
                if main_menu_button.collidepoint(mouse_pos):
                    return "main_menu"

def main(window):
    while True:
        if not main_menu(window):
            return
                           
        clock = pygame.time.Clock() # Clock object to control the FPS
        run = True  # Main loop flag
        
        tiles = generate_tiles() # Create the tiles
        result = "continue"  # Initialize result variable

        while run:
            clock.tick(FPS) # Control the FPS

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        result = pause_menu(window)
                        if result == "resume":
                            continue
                        elif result == "restart":
                            tiles = generate_tiles()
                        elif result == "main_menu":
                            if not main_menu(window):
                                return
                            tiles = generate_tiles()
                            
                    elif event.key == pygame.K_r:
                        tiles = generate_tiles()
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        result = move_tiles(window, tiles, clock, 'left')
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        result = move_tiles(window, tiles, clock, 'right')
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        result = move_tiles(window, tiles, clock, 'up')
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        result = move_tiles(window, tiles, clock, 'down')

                if result == "lost":
                    background = window.copy()  # Capture the current screen
                    result = game_over_menu(window, background)
                    if result == "restart":
                        tiles = generate_tiles()
                    elif result == "main_menu":
                        if not main_menu(window):
                            return
                        tiles = generate_tiles()
                
                if check_win(tiles):
                    background = window.copy()  # Capture the current screen
                    result = win_menu(window, background)
                    if result == "restart":
                        tiles = generate_tiles()
                    elif result == "main_menu":
                        if not main_menu(window):
                            return
                        tiles = generate_tiles()

            draw(window, tiles) # Draw the window
 
        pygame.quit()

if __name__ == '__main__':
    main(WINDOW)