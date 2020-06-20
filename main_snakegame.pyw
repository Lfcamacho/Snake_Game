import pygame
import random, os


SNAKE_SIZE = 12
ROWS, COLUMNS = 25, 40
WIDTH, HEIGHT = SNAKE_SIZE * COLUMNS, 440
GAME_POS_X, GAME_POS_Y = SNAKE_SIZE, 80
GAME_WIDTH, GAME_HEIGHT = WIDTH - 2 * GAME_POS_X, SNAKE_SIZE * ROWS
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
SNAKE_ICON = pygame.image.load(os.path.join("img", "snake.png"))
pygame.display.set_icon(SNAKE_ICON)

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (230,230,230)
GREEN = (79,205,177)
RED = (255,0,0)
PURPLE = (128,0,128)

# Fonts
pygame.font.init()
TITLE_FONT = pygame.font.Font("fonts/ka1.ttf", 40)
SCORE_FONT = pygame.font.Font("fonts/FakeHope.ttf", 35)
GAME_FONT = pygame.font.Font("fonts/game_over.ttf", 80)
GAME_FONT_2 = pygame.font.Font("fonts/game_over.ttf", 30)
GAME_FONT_3 = pygame.font.Font("fonts/game_over.ttf", 50)


class Snake():
    def __init__(self, size, color):
        self.size = size
        self.color = color
        self.body = []
        self.start_snake()        

    def start_snake(self):
        self.body.append(Snake_Square(self.size, self.color, GAME_POS_X, GAME_POS_Y + self.size * (ROWS // 2)))
        self.grow_snake(4)
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

    def grow_snake(self, squares, direction = None):
        for i in range(squares): 
            if direction:
                x = -1
                y = 0
            else:
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

    def change_color(self):
        color1 = random.randint(100,255)
        color2 = random.randint(100,255)
        color3 = random.randint(100,255)
        for square in self.body:
            square.color = (color1,color2,color3) 



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
        radius = self.size // 2
        pygame.draw.circle(WIN, self.color, (self.x + radius, self.y + radius), radius)

def pressed_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                return True

def game_over():
    white = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
    white.set_alpha(180)
    WIN.blit(white, (GAME_POS_X,GAME_POS_Y))

    text = GAME_FONT.render("GAME OVER", 1, WHITE)
    y = ((GAME_HEIGHT - text.get_height()) // 2) + GAME_POS_Y - 20
    WIN.blit(text, (((WIDTH - text.get_width()) // 2), y))
    text2 = GAME_FONT_2.render("PRESS ANY KEY TO PLAY AGAIN", 1, WHITE)
    WIN.blit(text2, (((WIDTH - text2.get_width()) // 2), y + text.get_height()))

    pygame.display.update()


def pause():
    white = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
    white.set_alpha(180)
    WIN.blit(white, (GAME_POS_X,GAME_POS_Y))

    text = GAME_FONT.render("PAUSED GAME", 1, WHITE)
    y = ((GAME_HEIGHT - text.get_height()) // 2) + GAME_POS_Y - 20
    WIN.blit(text, (((WIDTH - text.get_width()) // 2), y))
    text2 = GAME_FONT_2.render("PRESS ANY KEY TO CONTINUE", 1, WHITE)
    WIN.blit(text2, (((WIDTH - text2.get_width()) // 2), y + text.get_height()))

    pygame.display.update()
    pressed_key()

def main(start = False, top_score = 0):
    run = True
    FPS = 15
    snake = Snake(SNAKE_SIZE, GREEN)
    food = Food(SNAKE_SIZE, RED)
    direction = "right"
    score = 0
    clock = pygame.time.Clock()

    def redraw_window():

        WIN.fill(GRAY)
        title = TITLE_FONT.render("SNAKE GAME", 1, PURPLE)
        WIN.blit(title, (((WIDTH - title.get_width()) // 2), (GAME_POS_Y - title.get_height()) // 2))
        pygame.draw.rect(WIN, BLACK, (GAME_POS_X, GAME_POS_Y, GAME_WIDTH, GAME_HEIGHT))
        score_label = SCORE_FONT.render(f"SCORE: {score}", 1, BLACK)
        WIN.blit(score_label, (GAME_POS_X, (HEIGHT - score_label.get_height() - 10)))
        topscore_label = SCORE_FONT.render(f"TOP SCORE: {top_score}", 1, BLACK)
        WIN.blit(topscore_label, ((GAME_POS_X + GAME_WIDTH - topscore_label.get_width()), (HEIGHT - topscore_label.get_height() - 10)))

        if not start:
            white = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
            white.set_alpha(180)
            WIN.blit(white, (GAME_POS_X,GAME_POS_Y))
            text = GAME_FONT_3.render("PRESS ANY KEY TO START", 1, WHITE)
            y = ((GAME_HEIGHT - text.get_height()) // 2) + GAME_POS_Y - 10
            WIN.blit(text, (((WIDTH - text.get_width()) // 2), y))
        else:
            snake.draw_snake()
            food.draw_food()

        pygame.display.update()

    while run:

        clock.tick(FPS)
        snake.move_snake(direction)

        if snake.collision():
            game_over()
            pressed_key()
            main(True, top_score)


        if snake.grabbed_food(food):
            score +=10
            food.change_food(snake.body)
            snake.grow_snake(2)
            snake.change_color()
        
        if score > top_score:
            top_score = score

        redraw_window()

        while not start:
            if pressed_key():
                start = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause()
                    redraw_window()
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
                
while True:
    main()
