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
SPEED = 4
SIZE = 500


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

        self.game_over = False
        self.score = 0

        self.direction = STOP
        self.snake_head = self.width // 2, self.height // 2
        self.fruit = randint(0, self.width - 1), randint(0, self.height - 1)
        while self.field[self.fruit[1]][self.fruit[0]] != 0 or self.snake_head == self.fruit:
            self.fruit = randint(0, self.width - 1), randint(0, self.height - 1)
        self.tail = []
        self.tail_length = 2

        self.did_motion = True

    def free_cells_count(self):
        result = self.width * self.height
        for row in self.field:
            result -= row.count(1)
        result -= self.tail_length + 1
        return result

    def catch_key_press(self, key):
        if not self.did_motion:
            return

        if key == pygame.K_a and self.direction != RIGHT:
            self.direction = LEFT
            self.did_motion = False
        elif key == pygame.K_w and self.direction != DOWN:
            self.direction = UP
            self.did_motion = False
        elif key == pygame.K_d and self.direction != LEFT:
            self.direction = RIGHT
            self.did_motion = False
        elif key == pygame.K_s and self.direction != UP:
            self.direction = DOWN
            self.did_motion = False

    def render(self):
        super().render()
        # хвост змейки
        for tail_part in self.tail:
            tail_x, tail_y = tail_part
            rect = pygame.Rect(
                self.left + tail_x * self.cell_size, self.top + tail_y * self.cell_size,
                self.cell_size, self.cell_size
            )
            pygame.draw.rect(screen, (255, 0, 0), rect, self.cell_size // 10)
        # голова змейки
        rect = pygame.Rect(
            self.left + self.snake_head[0] * self.cell_size,
            self.top + self.snake_head[1] * self.cell_size,
            self.cell_size, self.cell_size
        )
        pygame.draw.rect(screen, (255, 204, 0), rect, self.cell_size // 10)
        # фрукт
        pygame.draw.circle(
            screen, (255, 0, 255),
            (self.fruit[0] * self.cell_size + self.left + self.cell_size // 2,
             self.fruit[1] * self.cell_size + self.top + self.cell_size // 2),
            int(self.cell_size * .4)
        )

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

        self.tail.insert(0, (predX, predY))
        if len(self.tail) > self.tail_length:
            self.tail.pop()

        if self.snake_head in self.tail or self.field[self.snake_head[1]][self.snake_head[0]]:
            pygame.mixer_music.load("data/gameover.mp3")
            pygame.mixer_music.play()
            self.game_over = True
            return

        if self.snake_head == self.fruit:
            pygame.mixer_music.load("data/omnom.mp3")
            pygame.mixer_music.play()
            self.score += 10
            self.tail_length += 1
            self.fruit = randint(0, self.width - 1), randint(0, self.height - 1)
            while self.field[self.fruit[1]][self.fruit[0]] != 0 or self.fruit in self.tail\
                    or self.fruit == self.snake_head:
                self.fruit = randint(0, self.width - 1), randint(0, self.height - 1)
        self.did_motion = True


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
    intro_text = ["Змейка", 'Нажмите "Enter",', "чтобы начать"]
    background = pygame.transform.scale(load_image("background.png"), (SIZE, SIZE))
    screen.blit(background, (0, 0))

    font = pygame.font.Font("data/joystix monospace.ttf", 40)
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
    font = pygame.font.Font("data/joystix monospace.ttf", 36)
    string = "Score:" + str(score).rjust(5, "0")
    string_rendered = font.render(string, 1, pygame.Color("white"))
    rect = string_rendered.get_rect()
    rect.top = 430
    rect.left = 100
    screen.blit(string_rendered, rect)


def end_screen(score):
    global best_score

    screen.fill((0, 0, 0))
    font = pygame.font.Font("data/joystix monospace.ttf", 26)
    strings = ["Игра окончена", "Нажмите Enter,", "чтобы играть сначала",
               "Ваш счёт:", str(score).rjust(5, "0") + " очков",
               "Ваш лучший результат:", str(best_score).rjust(5, "0") + " очков"]
    y_coord = 70
    for string in strings:
        string_rendered = font.render(string, 1, pygame.Color("white"))
        rect = string_rendered.get_rect()
        rect.top = y_coord
        y_coord += 20 + rect.h
        rect.left = SIZE // 2 - rect.w // 2
        screen.blit(string_rendered, rect)
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


def load_field_from_file(filename):
    file_path = os.path.join("10x10_fields", filename)
    with open(file_path) as field_file:
        lines = field_file.read().strip().split("\n")
        field_data = [list(map(int, line.split())) for line in lines]
    return field_data


def main():
    global best_score

    field_size = 10
    field = load_field_from_file("cage_field.txt")

    snake = Snake(field_size, field_size, field)
    snake.set_view(50, 10, int((SIZE * .8)) // field_size)

    clock = pygame.time.Clock()

    # Эти две переменные нужны для того, чтобы змейка двигалась, например,
    # два раза за секунду, а не 120
    time_from_prev_motion = 0
    time_needed_to_draw = 1000 // SPEED
    while not snake.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                snake.catch_key_press(event.key)

        time_from_prev_motion += clock.tick()
        screen.fill((0, 0, 0))
        if time_needed_to_draw < time_from_prev_motion:
            time_from_prev_motion -= time_needed_to_draw
            snake.update()
        snake.render()
        draw_score(snake.score)
        pygame.display.flip()

    best_score = max(best_score, snake.score)
    end_screen(snake.score)


best_score = 0
if __name__ == "__main__":
    pygame.display.set_caption("SNAKE GAME")
    pygame.init()
    screen = pygame.display.set_mode((SIZE, SIZE))
    start_screen()
    while True:
        main()
