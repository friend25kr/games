import pygame
import random
import sys

# --- Constants ---
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 480  # Score display area included
GRID_ROWS = 8
GRID_COLS = 8
CELL_SIZE = SCREEN_WIDTH // GRID_COLS # Each cell will be square
NUM_CANDY_TYPES = 5  # Number of different candy colors/types
EMPTY_CELL = -1      # Represents an empty cell on the board

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BACKGROUND_COLOR = (30, 30, 30)
CANDY_COLORS = [
    (255, 100, 100),  # Light Red
    (100, 255, 100),  # Light Green
    (100, 100, 255),  # Light Blue
    (255, 255, 100),  # Light Yellow
    (255, 100, 255),  # Light Magenta
    # (100, 255, 255),  # Light Cyan - Add more if NUM_CANDY_TYPES is increased
]
SELECTED_BORDER_COLOR = (255, 255, 255)
GRID_LINE_COLOR = (50, 50, 50)
SCORE_COLOR = (200, 200, 200)

FPS = 30 # Frames per second

# --- Helper Functions ---

def generate_candy_for_cell(r, c, board, num_types):
    """
    Generates a candy for cell (r,c) that doesn't create an initial match of 3.
    This is used during initial board creation.
    """
    possible_types = list(range(num_types))
    random.shuffle(possible_types)

    for candy_type in possible_types:
        # Check horizontal: board[r][c-1] and board[r][c-2]
        if c >= 2 and board[r][c-1] == candy_type and board[r][c-2] == candy_type:
            continue
        # Check vertical: board[r-1][c] and board[r-2][c]
        if r >= 2 and board[r-1][c] == candy_type and board[r-2][c] == candy_type:
            continue
        return candy_type
    
    # Fallback if all types create a match (should be rare) or for first few cells.
    return random.randint(0, num_types - 1)


def init_board(rows, cols, num_types):
    """Initializes the game board with no pre-existing matches."""
    board = [[EMPTY_CELL for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            board[r][c] = generate_candy_for_cell(r, c, board, num_types)
    return board


def draw_board(screen, board, cell_size, selected_pos=None):
    """Draws the game board and candies."""
    rows = len(board)
    cols = len(board[0])
    for r in range(rows):
        for c in range(cols):
            candy_type = board[r][c]
            # Define the rectangle for the current cell
            rect = pygame.Rect(c * cell_size, r * cell_size, cell_size, cell_size)

            if candy_type != EMPTY_CELL:
                # Ensure candy_type is a valid index for CANDY_COLORS
                color_index = candy_type % len(CANDY_COLORS) 
                pygame.draw.rect(screen, CANDY_COLORS[color_index], rect)
            
            # Draw a border for each cell
            pygame.draw.rect(screen, GRID_LINE_COLOR, rect, 1) 

            # Highlight the selected candy
            if selected_pos and selected_pos == (r, c):
                pygame.draw.rect(screen, SELECTED_BORDER_COLOR, rect, 3)


def get_clicked_cell(mouse_pos, cell_size, grid_rows, grid_cols):
    """Converts mouse click coordinates to board cell (row, col)."""
    mx, my = mouse_pos
    r = my // cell_size
    c = mx // cell_size
    
    # Check if the click is within the grid boundaries
    if 0 <= r < grid_rows and 0 <= c < grid_cols:
        return r, c
    return -1, -1 # Clicked outside the board grid


def find_all_matches(board):
    """Finds all horizontal and vertical matches of 3 or more candies."""
    rows = len(board)
    cols = len(board[0])
    matches = set() # Use a set to store unique coordinates of matched candies

    # Horizontal matches
    for r in range(rows):
        for c in range(cols - 2): # Need at least 3 cells to check
            if board[r][c] != EMPTY_CELL and \
               board[r][c] == board[r][c+1] and \
               board[r][c] == board[r][c+2]:
                
                # Add the initial 3 matched candies
                matches.add((r, c))
                matches.add((r, c+1))
                matches.add((r, c+2))
                # Check for longer matches (4 or more in a row)
                for k in range(c + 3, cols):
                    if board[r][k] == board[r][c]:
                        matches.add((r, k))
                    else:
                        break # End of the current match
    
    # Vertical matches
    for c in range(cols):
        for r in range(rows - 2): # Need at least 3 cells to check
            if board[r][c] != EMPTY_CELL and \
               board[r][c] == board[r+1][c] and \
               board[r][c] == board[r+2][c]:

                # Add the initial 3 matched candies
                matches.add((r, c))
                matches.add((r+1, c))
                matches.add((r+2, c))
                # Check for longer matches (4 or more in a column)
                for k in range(r + 3, rows):
                    if board[k][c] == board[r][c]:
                        matches.add((k, c))
                    else:
                        break # End of the current match
    return list(matches) # Return as a list of (row, col) tuples


def remove_candies(board, matched_coords):
    """Sets matched candies to EMPTY_CELL."""
    for r, c in matched_coords:
        board[r][c] = EMPTY_CELL


def apply_gravity(board):
    """Makes candies fall down to fill empty spaces."""
    rows = len(board)
    cols = len(board[0])
    for c in range(cols):
        # Create a temporary new column with empty cells at the top
        new_col = [EMPTY_CELL] * rows
        current_idx_new_col = rows - 1 # Start filling from the bottom of new_col
        
        # Iterate existing column from bottom up
        for r in range(rows - 1, -1, -1): 
            if board[r][c] != EMPTY_CELL:
                new_col[current_idx_new_col] = board[r][c]
                current_idx_new_col -= 1
        
        # Copy the new column back to the board
        for r in range(rows):
            board[r][c] = new_col[r]


def refill_board(board, num_types):
    """Fills empty cells at the top with new random candies."""
    rows = len(board)
    cols = len(board[0])
    for c in range(cols):
        for r in range(rows): # Iterate from top down
            if board[r][c] == EMPTY_CELL:
                # New candies "fall" from above
                board[r][c] = random.randint(0, num_types - 1)


def draw_score(screen, score, font, position):
    """Draws the current score on the screen."""
    score_text = font.render(f"Score: {score}", True, SCORE_COLOR)
    screen.blit(score_text, position)

# --- Main Game Function ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Candy Crush Basic - Gemini Code Assist")
    clock = pygame.time.Clock()
    score_font = pygame.font.Font(None, 36) # Default font, size 36

    board = init_board(GRID_ROWS, GRID_COLS, NUM_CANDY_TYPES)
    selected_candy_pos = None
    score = 0
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    clicked_r, clicked_c = get_clicked_cell(mouse_pos, CELL_SIZE, GRID_ROWS, GRID_COLS)

                    if clicked_r != -1: # Click was on the board grid
                        if selected_candy_pos is None:
                            # First click: select a candy
                            if board[clicked_r][clicked_c] != EMPTY_CELL:
                                selected_candy_pos = (clicked_r, clicked_c)
                        else:
                            # Second click: try to swap with the first selected candy
                            r1, c1 = selected_candy_pos
                            r2, c2 = clicked_r, clicked_c

                            # Check for adjacency (Manhattan distance == 1)
                            if abs(r1 - r2) + abs(c1 - c2) == 1:
                                # Perform swap
                                board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]
                                
                                # Check if this swap creates any match
                                matches_after_swap = find_all_matches(board)
                                
                                if matches_after_swap:
                                    # Valid swap, start cascading resolution
                                    while True: # Loop for cascading matches
                                        current_matches = find_all_matches(board)
                                        if not current_matches:
                                            break # No more matches, cascade finished

                                        score += len(current_matches) * 10 # Add to score
                                        remove_candies(board, current_matches)
                                        
                                        # To visualize steps (optional, makes game slower):
                                        # draw_board(screen, board, CELL_SIZE, None)
                                        # draw_score(screen, score, score_font, (10, GRID_ROWS * CELL_SIZE + 20))
                                        # pygame.display.flip()
                                        # pygame.time.wait(200) # ms delay

                                        apply_gravity(board)
                                        # draw_board(screen, board, CELL_SIZE, None)
                                        # draw_score(screen, score, score_font, (10, GRID_ROWS * CELL_SIZE + 20))
                                        # pygame.display.flip()
                                        # pygame.time.wait(200)

                                        refill_board(board, NUM_CANDY_TYPES)
                                        # draw_board(screen, board, CELL_SIZE, None)
                                        # draw_score(screen, score, score_font, (10, GRID_ROWS * CELL_SIZE + 20))
                                        # pygame.display.flip()
                                        # pygame.time.wait(200)
                                        
                                        # After refill, new matches might have formed, so loop again
                                else:
                                    # Invalid swap (no match formed), swap back to original positions
                                    board[r1][c1], board[r2][c2] = board[r2][c2], board[r1][c1]
                                
                                selected_candy_pos = None # Deselect after attempt
                            else:
                                # Not adjacent, or clicked same candy again.
                                if (r1,c1) == (r2,c2): # Clicked the same candy
                                    selected_candy_pos = None # Deselect
                                elif board[clicked_r][clicked_c] != EMPTY_CELL: # Clicked a different, non-adjacent candy
                                     selected_candy_pos = (clicked_r, clicked_c) # Select the new one
                                else: # Clicked an empty cell or non-adjacent non-candy
                                    selected_candy_pos = None
                    else: # Clicked outside board grid (e.g., score area)
                        selected_candy_pos = None


        # --- Drawing ---
        screen.fill(BACKGROUND_COLOR) # Clear screen
        draw_board(screen, board, CELL_SIZE, selected_candy_pos)
        # Position score display below the grid
        draw_score(screen, score, score_font, (10, GRID_ROWS * CELL_SIZE + 20)) 
        
        pygame.display.flip() # Update the full display
        clock.tick(FPS)       # Control game speed

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
