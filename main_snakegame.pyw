import pygame
import random

SNAKE_SIZE = 12
WIDTH, HEIGHT = SNAKE_SIZE * 40, 420
GAME_POS_X, GAME_POS_Y = SNAKE_SIZE, 50
GAME_WIDTH, GAME_HEIGHT = WIDTH - 2 * GAME_POS_X, SNAKE_SIZE * 25
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

class Snake():
    def __init__(self, size, color):
        self.size = size
        self.color = color
        self.snake = []
        self.start_snake()
        self.food = Food(size, RED)
        

    def start_snake(self):
        for i in range(5):
            self.snake.append(Snake_Square(self.size, self.color, GAME_POS_X + self.size * 10 - i * self.size, GAME_POS_Y))
        self.head = self.snake[0]

    def draw_snake(self):
        for square in self.snake:
            square.draw_square()

    def move_snake(self, direction):
        self.x = self.head.x
        self.y = self.head.y

        if direction == "up":
            self.head.y -= self.size
        if direction == "down":
            self.head.y += self.size
        if direction == "left":
            self.head.x -= self.size
        if direction == "right":
            self.head.x += self.size

        for square in self.snake[1:]:
            x2, y2 = square.x, square.y
            square.x, square.y = self.x, self.y
            self.x, self.y = x2, y2 
        
        self.head = self.snake[0]

    def grabbed_food(self):
        if [self.head.x, self.head.y] == [self.food.x, self.food.y]:
            self.food.change_food(self.snake)
            self.grow_snake()
    
    def grow_snake(self):
        for i in range(2): 
            x = (self.snake[len(self.snake) - 2].x - self.snake[len(self.snake) - 1].x) / 12
            y = (self.snake[len(self.snake) - 2].y - self.snake[len(self.snake) - 1].y) / 12
            self.snake.append(Snake_Square(self.size, self.color, self.snake[len(self.snake) - 1].x + self.size * x, self.snake[len(self.snake) - 1].y + self.size * y))

    def collision(self):
        if self.head.x < GAME_POS_X or self.head.x > (GAME_POS_X + GAME_WIDTH - self.size):
            return True
        if self.head.y < GAME_POS_Y or self.head.y > (GAME_POS_Y + GAME_HEIGHT - self.size):
            return True

        for square in self.snake[1:]:
            if [self.head.x, self.head.y] == [square.x, square.y]:
                return True
        return False  


class Snake_Square():
    def __init__(self, size, color, xcoor, ycoor):
        self.size = size
        self.color = color
        self.x = xcoor
        self.y = ycoor
        self.draw_square()

    def draw_square(self):
        pygame.draw.rect(WIN, self.color, (self.x + 1 , self.y + 1, self.size - 2, self.size - 2))

class Food():
    def __init__(self, size, color):
        self.size = size
        self.color = color
        self.change_food()
    
    def change_food(self, snake = []):
        run = True
        while run:
            self.x = random.randint(0, int(GAME_WIDTH / self.size) - 1)
            self.x = self.x * self.size + GAME_POS_X
            self.y = random.randint(0, int(GAME_HEIGHT / self.size) - 1)
            self.y = self.y * self.size + GAME_POS_Y
            run = False

            for square in snake:
                if [self.x, self.y] == [square.x, square.y]:
                    run = True
    
    def draw_food(self):
        pygame.draw.rect(WIN, self.color, (self.x, self.y, self.size, self.size))


def main():
    run = True
    FPS = 15
    snake = Snake(SNAKE_SIZE, GREEN)
    direction = "right"
    clock = pygame.time.Clock()

    def redraw_window():
        WIN.fill(GREEN)
        pygame.draw.rect(WIN, WHITE, (GAME_POS_X, GAME_POS_Y, GAME_WIDTH, GAME_HEIGHT))
        snake.draw_snake()
        snake.food.draw_food()
        
        pygame.display.update()

    while run:
        clock.tick(FPS)
        snake.move_snake(direction)
        if snake.collision():
            run = False
            break

        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "down":
                    direction = "up"
                    break
                if event.key == pygame.K_DOWN and direction != "up":
                    direction = "down"
                    break
                if event.key == pygame.K_LEFT and direction != "right":
                    direction = "left"
                    break
                if event.key == pygame.K_RIGHT and direction != "left":
                    direction = "right"
                    break

        snake.grabbed_food()



main()