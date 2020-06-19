import pygame
import random, os

SNAKE_SIZE = 12
WIDTH, HEIGHT = SNAKE_SIZE * 40, SNAKE_SIZE * 35
GAME_POS_X, GAME_POS_Y = SNAKE_SIZE, 50
GAME_WIDTH, GAME_HEIGHT = WIDTH - 2 * GAME_POS_X, SNAKE_SIZE * 25
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (150,150,150)
GREEN = (79,205,177)
BLUE = (128, 212, 255)
RED = (255,0,0)

# Fonts
pygame.font.init()
TITLE_FONT = pygame.font.SysFont("comicsans", 50)
MESSAGE_FONT  = pygame.font.SysFont("comicsans", 30)

# Images
SNAKE_IMG = pygame.transform.rotozoom(pygame.image.load(os.path.join("img", "snake.png")), 0, 0.27)
APPLE_IMG = pygame.transform.rotozoom(pygame.image.load(os.path.join("img", "apple.png")), 0, 0.07)


class Snake():
    def __init__(self, size, color):
        self.size = size
        self.color = color
        self.body = []
        self.start_snake()        

    def start_snake(self):
        for i in range(5):
            self.body.append(Snake_Square(self.size, self.color, GAME_POS_X + self.size * (18 - i), 12 * self.size + GAME_POS_Y))
        self.head = self.body[0]

    def draw_snake(self):
        for square in self.body:
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

        for square in self.body[1:]:
            x2, y2 = square.x, square.y
            square.x, square.y = self.x, self.y
            self.x, self.y = x2, y2 
        
        self.head = self.body[0]

    def grabbed_food(self, food):
        if [self.head.x, self.head.y] == [food.x, food.y]:
            return True
        return False

    def grow_snake(self):
        for i in range(2): 
            x = (self.body[len(self.body) - 2].x - self.body[len(self.body) - 1].x) / 12
            y = (self.body[len(self.body) - 2].y - self.body[len(self.body) - 1].y) / 12
            self.body.append(Snake_Square(self.size, self.color, int(self.body[len(self.body) - 1].x + self.size * x), int(self.body[len(self.body) - 1].y + self.size * y)))

    def collision(self):
        if self.head.x < GAME_POS_X or self.head.x > (GAME_POS_X + GAME_WIDTH - self.size):
            return True
        if self.head.y < GAME_POS_Y or self.head.y > (GAME_POS_Y + GAME_HEIGHT - self.size):
            return True

        for square in self.body[1:]:
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
        #pygame.draw.rect(WIN, BLACK, (self.x , self.y, self.size, self.size))
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
        radius = self.size // 2
        pygame.draw.circle(WIN, self.color, (self.x + radius, self.y + radius), radius)


def main():
    run = True
    FPS = 15
    snake = Snake(SNAKE_SIZE, WHITE)
    food = Food(SNAKE_SIZE, RED)
    direction = "right"
    pause = False
    start = False
    clock = pygame.time.Clock()

    def redraw_window():
        WIN.fill(WHITE)
        title = TITLE_FONT.render("SNAKE GAME", 1, BLACK)
        WIN.blit(title, (((WIDTH - title.get_width()) // 2), (GAME_POS_Y - title.get_height()) // 2))
        #WIN.blit(SNAKE_IMG, (GAME_POS_X,0))
        #WIN.blit(APPLE_IMG, (430,10))
        pygame.draw.rect(WIN, BLACK, (GAME_POS_X - 2, GAME_POS_Y - 2, GAME_WIDTH + 4, GAME_HEIGHT + 4))
        pygame.draw.rect(WIN, GREEN, (GAME_POS_X, GAME_POS_Y, GAME_WIDTH, GAME_HEIGHT))

        if not start:
            text = MESSAGE_FONT.render("Press any key to start...", 1, BLACK)
            WIN.blit(text, (((WIDTH - text.get_width()) // 2),300))
        elif pause:
            pass
        else:
            snake.draw_snake()
            food.draw_food()

        pygame.display.update()

    while run:

        clock.tick(FPS)
        
        snake.move_snake(direction)
        if snake.collision():
            run = False
            main()

        if snake.grabbed_food(food):
            food.change_food(snake.body)
            snake.grow_snake()

        redraw_window()

        while not start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    start = True

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

main()