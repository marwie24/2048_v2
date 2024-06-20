import pygame
import random

pygame.init()

# ekran, wyświetlacz, okno gry
GRID_SIZE = 4
CELL_SIZE = 100
MARGIN = 10
WIDTH = HEIGHT = GRID_SIZE * (CELL_SIZE + MARGIN) + MARGIN

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048 Game')

# kolory
BACKGROUND_COLOR = (187, 173, 160)
CELL_COLORS = {
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

#czcionka
FONT = pygame.font.SysFont('arial', 40)

# tablica wypełniona zerami
grid = [[0] * GRID_SIZE for i in range(GRID_SIZE)]

# dodawanie kafelka 2 lub 4 na początku tury bądź do zainicjalizowania gry
# sprawdza które pola w tablicy są puste, następnie jeżeli jest taka możliwość wybiera z nich losowo jedno pole
# i z prawdopodobieństwem 0.9 dla 2, 0.1 dla 4 losuje wartość dla tego kafelka
def add_new_tile():
    empty_cells = []
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == 0:
                empty_cells.append((r, c))
    if empty_cells:
        r, c = random.choice(empty_cells)
        if random.random() < 0.9:
            grid[r][c] = 2
        else:
            grid[r][c] = 4
    else:
        return True

# funkcja do "odświeżania" tablicy
def draw_grid():
    # zapełnia całość kolore, usuwa co było wcześniej
    screen.fill(BACKGROUND_COLOR)
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            value = grid[r][c]
            color = CELL_COLORS[value]
            # tworzy obiekt prostokąt w pygame, rect = pygame.Rect(left, top, width, height)
            # left - x współrzędna, top - y współrzędna (lewego górnego roku), width - szerokość, height - wysokość prostokąta
            rect = pygame.Rect(c * (CELL_SIZE + MARGIN) + MARGIN, r * (CELL_SIZE + MARGIN) + MARGIN, CELL_SIZE,
                               CELL_SIZE)
            # pygame.draw.rect(destination_surface, color, rect, width=0) width tutaj jako obramowanie, domyślnie brak
            pygame.draw.rect(screen, color, rect)
            # wypisywanie liczb na nie zerowych polach
            # screen.blit(source_surface, target_rect)
            if value != 0:
                if value < 8:
                    text_color = (119, 110, 101)
                else:
                    text_color = (249, 246, 242)
                # FONT.render(text, antialias, color), antialias wygładza krzywe
                text_surface = FONT.render(str(value), True, text_color)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)
    # uwidocznia wszytskie zmiany
    pygame.display.flip()

def move_left_merge():
    global grid
    new_grid = [[0] * GRID_SIZE for i in range(GRID_SIZE)]

    for r in range(GRID_SIZE):
        # wszytskie nie zerowe pola na lewo
        current_position = 0
        for c in range(GRID_SIZE):
            if grid[r][c] != 0:
                new_grid[r][current_position] = grid[r][c]
                current_position += 1
    # merge
    for r in range(GRID_SIZE):
        # -1 bo później c+1
        for c in range(GRID_SIZE - 1):
            # merguje takie same obok siebie w lewo
            if new_grid[r][c] == new_grid[r][c + 1] and new_grid[r][c] != 0:
                new_grid[r][c] = new_grid[r][c]*2
                new_grid[r][c + 1] = 0
    grid = new_grid
def move_right_merge():
    global grid
    new_grid = [[0] * GRID_SIZE for i in range(GRID_SIZE)]

    for r in range(GRID_SIZE):
        # wszytskie nie zerowe pola na prawo
        current_position = 3
        for c in [3,2,1,0]:
            if grid[r][c] != 0:
                new_grid[r][current_position] = grid[r][c]
                current_position -= 1
    # merge
    for r in range(GRID_SIZE):
        for c in [3,2,1]:
            # merguje takie same obok siebie w prawo
            if new_grid[r][c] == new_grid[r][c - 1] and new_grid[r][c] != 0:
                new_grid[r][c] = new_grid[r][c]*2
                new_grid[r][c - 1] = 0
    grid = new_grid

def move_up_merge():
    global grid
    new_grid = [[0] * GRID_SIZE for i in range(GRID_SIZE)]

    for c in range(GRID_SIZE):
        # wszytskie nie zerowe pola w górę
        current_position = 0
        for r in range(GRID_SIZE):
            if grid[r][c] != 0:
                new_grid[current_position][c] = grid[r][c]
                current_position += 1
    #merge
    for c in range(GRID_SIZE):
        for r in range(GRID_SIZE-1):
            # merguje takie same obok siebie w górę
            if new_grid[r][c] == new_grid[r+1][c] and new_grid[r][c] != 0:
                new_grid[r][c] = new_grid[r][c]*2
                new_grid[r+1][c] = 0
    grid = new_grid

def move_down_merge():
    global grid
    new_grid = [[0] * GRID_SIZE for i in range(GRID_SIZE)]

    for c in range(GRID_SIZE):
        # wszytskie nie zerowe pola w górę
        current_position = 3
        for r in [3, 2, 1, 0]:
            if grid[r][c] != 0:
                new_grid[current_position][c] = grid[r][c]
                current_position -= 1
    # merge
    for c in range(GRID_SIZE):
        for r in [3, 2, 1]:
         # merguje takie same obok siebie w dół
            if new_grid[r][c] == new_grid[r - 1][c] and new_grid[r][c] != 0:
                new_grid[r][c] = new_grid[r][c] * 2
                new_grid[r-1][c] = 0

    grid = new_grid

#sprawdzanei czy wygrana
def check_win():
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if grid[r][c] == 2048:
                print("You won!")
                pygame.quit()

# zaczynamy gre!
add_new_tile()
add_new_tile()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                move_left_merge()
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                move_right_merge()
            elif event.key in (pygame.K_UP, pygame.K_w):
                move_up_merge()
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                move_down_merge()
            if add_new_tile():
                print("Game Over")
                running = False
            check_win()

    draw_grid()



pygame.quit()
