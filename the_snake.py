from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Ввводим размер квадратика:
CELL_SIZE = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Общий класс для яблока и змейки"""

    def __init__(self, body_color=None):
        # Общие координаты
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        # Сохраняем результат
        self.position = (center_x, center_y)
        # Общий цвет
        self.body_color = body_color
        # Активен ли объект
        self.is_active = True

    def draw(self):
        """Пустой метод для последующего объявления в дочерних классах"""


# Класс яблока:
class Apple(GameObject):
    """Класс яблока"""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)

    def randomize_position(self, occupied_cells):
        """Генерация случайной позиции."""
        while True:
            # Генерируем случайную клетку (потом переведем в пиксели)
            x_cell = randint(0, GRID_WIDTH - 1)
            y_cell = randint(0, GRID_HEIGHT - 1)

            new_pos = (x_cell * CELL_SIZE, y_cell * CELL_SIZE)

            # ПРОВЕРКА: Если змейки нет или позиция свободна
            if occupied_cells is None or new_pos not in occupied_cells:
                self.position = new_pos
                return

    def draw(self):
        """Отрисовка яблока"""
        rect = pg.Rect(self.position, (CELL_SIZE, CELL_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змеи"""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Определяем позицию головы змеи"""
        if not self.positions:
            return None
        return self.positions[0]

    def move(self):
        """Логика движения змейки"""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head_x = head_x + dx * CELL_SIZE
        new_head_y = head_y + dy * CELL_SIZE

        final_x = (new_head_x // CELL_SIZE) % GRID_WIDTH * CELL_SIZE
        final_y = (new_head_y // CELL_SIZE) % GRID_HEIGHT * CELL_SIZE
        final_head = (final_x, final_y)

        self.positions.insert(0, final_head)

        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """Метод для возвращения змейки в изначальное состояние"""
        # Я прочел коментарий,это не метод проверки, а возрат змейки в центр
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2
        start_pos = (center_x, center_y)

        self.length = 1
        self.positions = [start_pos]

        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змеи, если игрок нажал клавишу"""
        if self.next_direction is not None:

            is_reverse = (
                self.next_direction[0] == -self.direction[0]
                and self.next_direction[1] == -self.direction[1]
            )

            if not is_reverse:
                self.direction = self.next_direction

            self.next_direction = None

    def draw(self):
        """Метод для отрисовки змейки"""
        for position in self.positions:
            rect = pg.Rect(position, (CELL_SIZE, CELL_SIZE))

            pg.draw.rect(screen, self.body_color, rect)

            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Логика управления игроком"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Игровой процесс"""
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()
    occupied_cells = set(snake.positions)
    apple.randomize_position(occupied_cells)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        # Двигаем змею
        snake.move()
        # Проверяем, не врезалась ли змея в себя
        head = snake.get_head_position()
        if head in snake.positions[1:]:
            snake.reset()
            continue
        # Рост змейки на деление, если съела яблоко
        elif head == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pg.display.flip()


if __name__ == '__main__':
    main()
