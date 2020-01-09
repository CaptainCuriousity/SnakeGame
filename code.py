import pygame
import os
import sys


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.top = 10
        self.left = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.top = top
        self.left = left
        self.cell_size = cell_size

    def render(self):
        for i in range(self.width):
            for j in range(self.height):
                rect = pygame.Rect(
                    self.left + i * self.cell_size, self.top + j * self.cell_size,
                    self.cell_size, self.cell_size
                )
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)


class Snake(Board):
    def __init__(self, width, height, field=None):
        super().__init__(width, height)

        # Игровое поле. 0 соответствует пустой клетке, 1 - барьеру, 2 - еде
        # 3 - голове, 4 - части туловища
        # В случае, если уже есть игровое поле и его размеры совпадают с размером доски,
        # То ставится оно, в противном случае генерируется новое
        if field is not None and len(field) == height and len(field[0]) == width:
            self.field = field
        else:
            self.field = [[0] * width for _ in range(height)]

    def render(self):
        for i in range(self.width):
            for j in range(self.height):
                rect = pygame.Rect(
                    self.left + i * self.cell_size, self.top + j * self.cell_size,
                    self.cell_size, self.cell_size
                )
                if self.field[j][i] == 0:
                    pygame.draw.rect(screen, (255, 255, 255), rect, 1)
                elif self.field[j][i] == 1:
                    pygame.draw.rect(screen, (255, 255, 255), rect)
                elif self.field[j][i] == 2:
                    pygame.draw.rect(screen, (255, 255, 255), rect, 1)
                    pygame.draw.circle(
                        screen, (255, 255, 0),
                        (self.left + i * self.cell_size + self.cell_size // 2,
                         self.top + j * self.cell_size + self.cell_size // 2),
                        self.cell_size // 2 - 2
                    )


def load_image(name, color_key=None):
    fullname = os.path.join("data", name)
    image = pygame.image.load(fullname).convert()

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗМЕЙКА", "На торе"]
    background = pygame.transform.scale(load_image('background.png'), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))

    font = pygame.font.Font("joystix monospace.ttf", 70)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 50
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def end_screen():
    pass


def draw_score():
    pass


pygame.init()
WIDTH, HEIGHT = SIZE = (500, 500)
screen = pygame.display.set_mode(SIZE)
start_screen()

board = Snake(10, 10)
board.set_view(50, 50, 40)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    board.render()
    pygame.display.flip()

pygame.quit()
