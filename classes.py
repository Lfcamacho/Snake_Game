import pygame
from settings import *
import random

class Snake():
    def __init__(self, size, color):
        self.size = size
        self.color = color
        self.body = []
        self.start_snake()        

    # creates snake's body when game starts
    def start_snake(self):
        self.body.append(Snake_Square(self.size, self.color, GAME_POS_X, GAME_POS_Y + self.size * (ROWS // 2)))
        self.grow_snake(4)
        self.head = self.body[0]

    # draws each square of snake's body
    def draw_snake(self, WIN):
        for square in self.body:
            square.draw_square(WIN)

    # updates each snake's body square x and y position
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

    # checks if snake have grabbed the food
    def grabbed_food(self, food):
        if [self.head.x, self.head.y] == [food.x, food.y]:
            return True
        return False

    # adds a given number of squares to the end of snake on a given direction
    def grow_snake(self, squares, direction = None):
        for i in range(squares): 
            if direction:
                x = -1
                y = 0
            else:
                x = (self.body[len(self.body) - 2].x - self.body[len(self.body) - 1].x) / 12
                y = (self.body[len(self.body) - 2].y - self.body[len(self.body) - 1].y) / 12
            self.body.append(Snake_Square(self.size, self.color, int(self.body[len(self.body) - 1].x + self.size * x), int(self.body[len(self.body) - 1].y + self.size * y)))

    # checks if snake have made a collision with himself or the borders
    def collision(self):
        if self.head.x < GAME_POS_X or self.head.x > (GAME_POS_X + GAME_WIDTH - self.size):
            return True
        if self.head.y < GAME_POS_Y or self.head.y > (GAME_POS_Y + GAME_HEIGHT - self.size):
            return True

        for square in self.body[1:]:
            if [self.head.x, self.head.y] == [square.x, square.y]:
                return True
        return False  

    # changes color of the snake
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

    def draw_square(self, WIN):
        pygame.draw.rect(WIN, self.color, (self.x + 1 , self.y + 1, self.size - 2, self.size - 2))

class Food():
    def __init__(self, size, color):
        self.size = size
        self.color = color
        self.change_food()
    
    # changes food position
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
    
    def draw_food(self, WIN):
        radius = self.size // 2
        pygame.draw.circle(WIN, self.color, (self.x + radius, self.y + radius), radius)