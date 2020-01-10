import pygame
import os
import sys
from random import randint


STOP = 0
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4
FPS = 60
SPEED = 2


class Board:
    def __init__(self, width, height, field=None):
        self.width = width
        self.height = height

        self.top = 10
        self.left = 10
        self.cell_size = 30

        if field is not None and len(field) == height and len(field[0]) == width:
            self.field = field
        else:
            self.field = [[0] * width for _ in range(height)]

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
                if self.field[j][i] == 0:
                    pygame.draw.rect(screen, (255, 255, 255), rect, 1)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), rect)


class Snake(Board):
    def __init__(self, width, height, field=None):
        super().__init__(width, height, field)

        # Игровое поле. 0 соответствует пустой клетке, 1 - барьеру
        self.score = 0

        self.direction = STOP
        self.snake_head = self.width // 2, self.height // 2
        self.fruit = randint(0, self.width - 1), randint(0, self.height - 1)
        while self.field[self.fruit[0]][self.fruit[1]] != 0:
            self.fruit = randint(0, self.width - 1), randint(0, self.height - 1)
        self.tail = []
        self.tail_length = 3

    def catch_key_press(self, key):
        if key == pygame.K_a and self.direction != RIGHT:
            self.direction = LEFT
        elif key == pygame.K_w and self.direction != DOWN:
            self.direction = UP
        elif key == pygame.K_d and self.direction != LEFT:
            self.direction = RIGHT
        elif key == pygame.K_s and self.direction != UP:
            self.direction = DOWN

    def render(self):
        super().render()
        # голова змейки
        pygame.draw.circle(
            screen, (255, 0, 128),
            (self.snake_head[0] * self.cell_size + self.left + self.cell_size // 2,
             self.snake_head[1] * self.cell_size + self.top + self.cell_size // 2),
            self.cell_size // 2 - 2
        )
        # фрукт
        pygame.draw.circle(
            screen, (0, 255, 0),
            (self.fruit[0] * self.cell_size + self.left + self.cell_size // 2,
             self.fruit[1] * self.cell_size + self.top + self.cell_size // 2),
            self.cell_size // 2 - 2
        )
        # хвост змейки
        for tail_part in self.tail:
            tail_x, tail_y = tail_part
            rect = pygame.Rect(
                self.left + tail_x * self.cell_size, self.top + tail_y * self.cell_size,
                self.cell_size, self.cell_size
            )
            pygame.draw.rect(screen, (255, 0, 0), rect)

    def update(self):
        if self.direction == STOP:
            return

        predX, predY = self.snake_head
        if self.direction == UP:
            self.snake_head = (predX, (predY - 1) % self.height)
        elif self.direction == RIGHT:
            self.snake_head = ((predX + 1) % self.width, predY)
        elif self.direction == DOWN:
            self.snake_head = (predX, (predY + 1) % self.height)
        elif self.direction == LEFT:
            self.snake_head = ((predX - 1) % self.width, predY)

        if self.snake_head in self.tail or self.field[self.snake_head[1]][self.snake_head[0]] == 1:
            print("Loser")

        if self.snake_head == self.fruit:
            self.score += 10
            self.tail_length += 1
            self.fruit = randint(0, self.width - 1), randint(0, self.height - 1)
            while self.field[self.fruit[1]][self.fruit[0]] != 0 or self.fruit in self.tail:
                self.fruit = randint(0, self.width - 1), randint(0, self.height - 1)

        self.tail.insert(0, (predX, predY))
        if len(self.tail) > self.tail_length:
            self.tail.pop()


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
    intro_text = ["Змейка на торе", 'Нажмите "Enter",', "чтобы начать"]
    background = pygame.transform.scale(load_image("background.png"), (WIDTH, HEIGHT))
    screen.blit(background, (0, 0))

    font = pygame.font.Font("joystix monospace.ttf", 40)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color("black"))
        intro_rect = string_rendered.get_rect()
        text_coord += 30
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_ESCAPE:
                    terminate()
        pygame.display.flip()


def draw_score(score):
    font = pygame.font.Font("joystix monospace.ttf", 36)
    string = "Score:" + str(score).rjust(4, "0")
    string_rendered = font.render(string, 1, pygame.Color("white"))
    rect = string_rendered.get_rect()
    rect.top = 430
    rect.left = 100
    screen.blit(string_rendered, rect)


def end_screen():
    pass


pygame.init()
WIDTH, HEIGHT = SIZE = (500, 500)
screen = pygame.display.set_mode(SIZE)
start_screen()

field = [
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

snake = Snake(10, 10, field)
snake.set_view(50, 10, 40)

clock = pygame.time.Clock()

# Эти три переменные нужны для того, чтобы змейка двигалась, например,
# два раза за секунду, а не 120
time_from_start = 0
time_needed_to_draw = 1000 // SPEED
total_motions = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            snake.catch_key_press(event.key)
    time_from_start += clock.tick(FPS)
    print(time_from_start)
    screen.fill((0, 0, 0))
    if total_motions * time_needed_to_draw < time_from_start:
        total_motions += 1
        snake.update()
    snake.render()
    draw_score(snake.score)
    pygame.display.flip()

pygame.quit()
