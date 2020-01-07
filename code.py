import pygame


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
                        screen,
                        (255, 255, 0),
                        (
                            self.left + i * self.cell_size + self.cell_size // 2,
                            self.top + j * self.cell_size + self.cell_size // 2
                        ),
                        self.cell_size // 2 - 2
                    )


pygame.init()
SIZE = (500, 500)
screen = pygame.display.set_mode(SIZE)

field = [
    [0, 0, 0, 0, 1],
    [0, 0, 1, 1, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 1, 1],
    [2, 0, 0, 0, 1]
]
board = Snake(5, 5, field)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    board.render()
    pygame.display.flip()

pygame.quit()
