import pygame
import random
import sys

WIDTH, HEIGHT = 480, 600
GRID_SIZE = 100
SPACING = 10
BOARD_SIZE = 4
BACKGROUND_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}
TEXT_COLOR = (119, 110, 101)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048')
clock = pygame.time.Clock()

class Game2048:
    def __init__(self):
        self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def transpose(self):
        return [[self.board[j][i] for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]

    def reverse(self):
        return [row[::-1] for row in self.board]

    def merge_row(self, row):
        merged = []
        prev = None
        for num in row:
            if num != 0:
                if prev is None:
                    prev = num
                elif prev == num:
                    merged.append(prev * 2)
                    self.score += prev * 2
                    prev = None
                else:
                    merged.append(prev)
                    prev = num
        if prev is not None:
            merged.append(prev)
        merged += [0] * (BOARD_SIZE - len(merged))
        return merged

    def move_left(self):
        new_board = []
        changed = False
        for row in self.board:
            merged = self.merge_row(row)
            new_board.append(merged)
            if merged != row:
                changed = True
        if changed:
            self.board = new_board
            self.add_new_tile()
        return changed

    def move_right(self):
        self.board = self.reverse()
        changed = self.move_left()
        self.board = self.reverse()
        return changed

    def move_up(self):
        self.board = self.transpose()
        changed = self.move_left()
        self.board = self.transpose()
        return changed

    def move_down(self):
        self.board = self.transpose()
        changed = self.move_right()
        self.board = self.transpose()
        return changed

    def is_game_over(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == 0:
                    return False
                if i < BOARD_SIZE - 1 and self.board[i][j] == self.board[i+1][j]:
                    return False
                if j < BOARD_SIZE - 1 and self.board[i][j] == self.board[i][j+1]:
                    return False
        return True

def draw_board(game):
    screen.fill(BACKGROUND_COLOR)
    
    font = pygame.font.Font(None, 60)
    text = font.render(f'Score: {game.score}', True, TEXT_COLOR)
    screen.blit(text, (20, 20))
    
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            x = j * (GRID_SIZE + SPACING) + SPACING
            y = i * (GRID_SIZE + SPACING) + SPACING + 80
            tile_value = game.board[i][j]
            tile_color = TILE_COLORS.get(tile_value, (0, 0, 0))
            pygame.draw.rect(screen, tile_color, (x, y, GRID_SIZE, GRID_SIZE))
            if tile_value != 0:
                font = pygame.font.Font(None, 40 if tile_value < 100 else 30 if tile_value < 1000 else 24)
                text = font.render(str(tile_value), True, TEXT_COLOR)
                text_rect = text.get_rect(center=(x + GRID_SIZE//2, y + GRID_SIZE//2))
                screen.blit(text, text_rect)
   
    if game.is_game_over():
        font = pygame.font.Font(None, 80)
        text = font.render('Game Over!', True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, text_rect)

def main():
    game = Game2048()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not game.is_game_over():
                if event.key == pygame.K_LEFT:
                    game.move_left()
                elif event.key == pygame.K_RIGHT:
                    game.move_right()
                elif event.key == pygame.K_UP:
                    game.move_up()
                elif event.key == pygame.K_DOWN:
                    game.move_down()
        draw_board(game)
        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main()
