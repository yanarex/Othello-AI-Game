import pygame
import sys
import random
import time


# Game setup
BOARD_SIZE = 8                  # The board is 8x8
SQUARE_SIZE = 80                # Each square is 80 by 80 pixels
WINDOW_SIZE = BOARD_SIZE * SQUARE_SIZE  # board dimensions

# Colors
GREEN = (0, 128, 0)             
GRAY = (128, 128, 128)          # Grid lines
WHITE = (255, 255, 255)  
BLACK = (0, 0, 0)

# Board class: Represents the game board and its operations.
class Board:
    def __init__(self):
        # Initialize an empty board, none means its empty
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.initialize_board()

    def initialize_board(self):
        # Sets up the starting four pieces in the center of the board.
        self.board[3][3] = 'B'
        self.board[3][4] = 'W'
        self.board[4][3] = 'W'
        self.board[4][4] = 'B'

    def in_bounds(self, i, j):
        # Check if the (i, j) coordinates are within the bounds of the board
        return 0 <= i < BOARD_SIZE and 0 <= j < BOARD_SIZE

    def get_valid_moves(self, color):
        # Returns a list of valid moves for a given color
        moves = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                # A cell must be empty and the move should flip at least one opponent piece
                if self.board[i][j] is None and self.is_valid_move(i, j, color):
                    moves.append((i, j))
        return moves

    def is_valid_move(self, i, j, color):
        # Check if placing a piece at position (i, j) is legal
        if self.board[i][j] is not None:
            return False  # Cannot move on a non-empty cell
        opponent = 'W' if color == 'B' else 'B'
        # Look in all 8 directions
        for a in [-1, 0, 1]:
            for b in [-1, 0, 1]:
                if a == 0 and b == 0:
                    continue  # Dont check the same cell
                x, y = i + a, j + b
                count = 0
                # Continue in this direction while encountering opponent pieces.
                while self.in_bounds(x, y) and self.board[x][y] == opponent:
                    count += 1
                    x += a
                    y += b
                # If at least one opponent piece is found and we then land on our own piece, the move is valid.
                if count > 0 and self.in_bounds(x, y) and self.board[x][y] == color:
                    return True
        return False

    def apply_move(self, i, j, color):
        # Place a piece at (i, j) and flip all the opponent pieces as per Othello rules
        opponent = 'W' if color == 'B' else 'B'
        self.board[i][j] = color  # Place the piece
        flips = []
        # Check for flips in each of the 8 directions
        for a in [-1, 0, 1]:
            for b in [-1, 0, 1]:
                if a == 0 and b == 0:
                    continue  # Dont check the same cell
                x, y = i + a, j + b
                potential_flips = []
                # Collect all opponent pieces in this direction.
                while self.in_bounds(x, y) and self.board[x][y] == opponent:
                    potential_flips.append((x, y))
                    x += a
                    y += b
                # If a friendly piece terminates the line, perform the flips.
                if potential_flips and self.in_bounds(x, y) and self.board[x][y] == color:
                    flips.extend(potential_flips)
        # Update the board with flipped pieces.
        for (x, y) in flips:
            self.board[x][y] = color
        return flips

    def copy(self):
        # Return a copy of the current board.
        new_board = Board()
        new_board.board = [row[:] for row in self.board]
        return new_board

# Evaluate the board from the perspective of the player.
# Returns the difference in pieces between the player and the opponent.
def evaluate_board(board, color):
    # Count the pieces for the player.
    my_count = sum(row.count(color) for row in board.board)
    # Determine opponent's color.
    opponent = 'W' if color == 'B' else 'B'
    # Count the opponent's pieces.
    opp_count = sum(row.count(opponent) for row in board.board)
    # Return the difference.
    return my_count - opp_count


# Minimax Algorithm with Alpha-Beta Pruning
def minimax(board, depth, alpha, beta, maximizing_player, color):
    valid_moves = board.get_valid_moves(color)
    # Depth limit reached or no valid moves
    if depth == 0 or not valid_moves:
        return evaluate_board(board, color), None

    best_move = None
    if maximizing_player:
        max_eval = -float("inf")
        # For each valid move, simulate the move and call minimax recursively.
        for move in valid_moves:
            new_board = board.copy()
            new_board.apply_move(move[0], move[1], color)
            # Switch color for opponent.
            opponent = 'W' if color == 'B' else 'B'
            eval_score, _ = minimax(new_board, depth - 1, alpha, beta, False, opponent)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
            alpha = max(alpha, eval_score)
            # Cut-off branch if possible.
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float("inf")
        opponent = 'W' if color == 'B' else 'B'
        for move in valid_moves:
            new_board = board.copy()
            new_board.apply_move(move[0], move[1], color)
            eval_score, _ = minimax(new_board, depth - 1, alpha, beta, True, opponent)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_move

# Helper function that uses minimax to decide the best move
def get_best_move(board, depth, color):
    _, move = minimax(board, depth, -float("inf"), float("inf"), True, color)
    return move


# Drawing the Game Board and UI elements
def draw_board(screen, board):
    screen.fill(GREEN)  # Fill the background with green
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            # Calculate the rectangle for each cell
            rect = pygame.Rect(j * SQUARE_SIZE, (BOARD_SIZE - 1 - i) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)  # Draw grid lines
            if board.board[i][j] is not None:
                # Compute the center of the cell
                center = (j * SQUARE_SIZE + SQUARE_SIZE // 2,
                          (BOARD_SIZE - 1 - i) * SQUARE_SIZE + SQUARE_SIZE // 2)
                # Draw the pieces.
                if board.board[i][j] == 'W':
                    pygame.draw.circle(screen, WHITE, center, SQUARE_SIZE // 2 - 5)
                else:
                    pygame.draw.circle(screen, BLACK, center, SQUARE_SIZE // 2 - 5)

    # Draw Back Button in the top-left corner
    back_button_rect = pygame.Rect(10, 10, 80, 40)
    pygame.draw.rect(screen, GRAY, back_button_rect)
    font = pygame.font.SysFont(None, 24)
    text_surface = font.render("Back", True, WHITE)
    text_rect = text_surface.get_rect(center=back_button_rect.center)
    screen.blit(text_surface, text_rect)

    # Update the display.
    pygame.display.flip()
    return back_button_rect


# Start Screen, Coin Flip, and Color Assignment
def start_screen(screen):
    font = pygame.font.SysFont(None, 48)
    clock = pygame.time.Clock()
    waiting = True
    # wait until the player presses SPACE.
    while waiting:
        screen.fill(GREEN)
        instruct_text = font.render("Press SPACE to flip coin", True, WHITE)
        rect = instruct_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
        screen.blit(instruct_text, rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
        clock.tick(15)
    
    # Simulate a coin flip to decide whether player is Black or White
    human_is_black = random.choice([True, False])
    result_text = "You are Black" if human_is_black else "You are White"
    
    screen.fill(GREEN)
    result_render = font.render(result_text, True, WHITE)
    rect = result_render.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
    screen.blit(result_render, rect)
    pygame.display.flip()
    pygame.time.wait(2000)
    
    # In Othello, Black always moves first
    if human_is_black:
        human_color = 'B'
        agent_color = 'W'
    else:
        human_color = 'W'
        agent_color = 'B'
    return human_color, agent_color


# Check if the game is over
# The game ends when the board is full or when neither player can move
def is_game_over(board):
    full = all(cell is not None for row in board.board for cell in row)
    no_moves = (not board.get_valid_moves('B') and not board.get_valid_moves('W'))
    return full or no_moves

# End Screen, display game results, and play stats
def show_end_screen(screen, board, human_color, agent_color, black_count, white_count, human_wins, agent_wins, draws):
    font = pygame.font.SysFont(None, 36)
    # Determine the winner based on piece counts.
    if black_count > white_count:
        winning_color = 'B'
    elif white_count > black_count:
        winning_color = 'W'
    else:
        winning_color = 'Draw'
        
    result_text = "It's a draw!" if winning_color == 'Draw' else ("You win!" if human_color == winning_color else "You lose!")
    message_lines = [
         result_text,
         f"Black: {black_count}  White: {white_count}",
         f"Your wins: {human_wins}   AI wins: {agent_wins}   Draws: {draws}",
         "Press R to restart or Q to quit"
    ]

    screen.fill(GREEN)
    y = WINDOW_SIZE // 2 - 50
    for line in message_lines:
        text_surface = font.render(line, True, WHITE)
        rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, y))
        screen.blit(text_surface, rect)
        y += 40
    pygame.display.flip()

    waiting = True
    # Wait for the player to choose whether to restart or quit
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    return 'restart'
                elif event.key == pygame.K_q:
                    waiting = False
                    return 'quit'


# Main game loop:
# Handles game initialization, event processing, move application, AI turns, and undo operations
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Othello")
    clock = pygame.time.Clock()

    # Tracking wins for the human, AI, and draws.
    human_total_wins = 0
    agent_total_wins = 0
    draws_total = 0

    while True:
        # Display start screen and decide colors via a coin flip
        human_color, agent_color = start_screen(screen)
        # Create a new board for the game
        board = Board()
        depth = 3  # Using a 3-ply search

        # Initialize move history.
        move_history = [(board.copy(), 'init')]

        # Draw the initial board
        back_button_rect = draw_board(screen, board)
        pygame.time.wait(1000)  # Pause briefly before game start

        current_turn = 'B'  # Black always starts
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Handle Mouse Clicks
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    # Check for click on the Back button.
                    if pygame.Rect(10, 10, 80, 40).collidepoint(pos):
                        if len(move_history) > 1:
                            if move_history[-1][1] == 'ai':
                                move_history.pop()  # Undo AI move.
                                if len(move_history) > 1:
                                    move_history.pop()  # Then undo the human move.
                            else:
                                move_history.pop()  # Just remove the human's move.
                            board = move_history[-1][0].copy()
                            current_turn = human_color
                            back_button_rect = draw_board(screen, board)
                        continue

                    # Process the human's move
                    if current_turn == human_color:
                        x, y = pos
                        j = x // SQUARE_SIZE
                        i = BOARD_SIZE - 1 - (y // SQUARE_SIZE)
                        if board.is_valid_move(i, j, human_color):
                            board.apply_move(i, j, human_color)
                            move_history.append((board.copy(), 'human'))
                            back_button_rect = draw_board(screen, board)
                            current_turn = agent_color

            # Skip turns if no valid moves are available.
            if current_turn == human_color and not board.get_valid_moves(human_color):
                current_turn = agent_color
            elif current_turn == agent_color and not board.get_valid_moves(agent_color):
                current_turn = human_color

            # Check if the game has ended.
            if is_game_over(board):
                running = False
                break

            # AI's Turn: Use minimax to decide the move.
            if current_turn == agent_color and board.get_valid_moves(agent_color):
                pygame.time.wait(500)  # simulate “thinking”

                # Measure AI computation time
                start = time.perf_counter()
                best_move = get_best_move(board, depth, agent_color)
                elapsed = time.perf_counter() - start
                print(f"AI move computation time: {elapsed:.4f} seconds")

                if best_move is not None:
                    board.apply_move(best_move[0], best_move[1], agent_color)
                    move_history.append((board.copy(), 'ai'))
                    back_button_rect = draw_board(screen, board)
                    pygame.time.wait(1000)  # let player see it
                    current_turn = human_color

            clock.tick(10)  # Set the game loop speed

        # Count pieces and determine the winner at the end
        black_count = sum(row.count('B') for row in board.board)
        white_count = sum(row.count('W') for row in board.board)
        if black_count > white_count:
            winner = 'B'
        elif white_count > black_count:
            winner = 'W'
        else:
            winner = 'Draw'

        # Update win counts
        if winner == 'Draw':
            draws_total += 1
        elif winner == human_color:
            human_total_wins += 1
        else:
            agent_total_wins += 1

        # Show end screen and ask to restart or quit
        choice = show_end_screen(
            screen, board, human_color, agent_color,
            black_count, white_count,
            human_total_wins, agent_total_wins, draws_total
        )
        if choice == 'quit':
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    main()
