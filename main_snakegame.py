import pygame
import os
from settings import *
from classes import *
from os import path

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
SNAKE_ICON = pygame.image.load(os.path.join("img", "snake.png"))
pygame.display.set_icon(SNAKE_ICON)

# wait till user presses a key to continue
def pressed_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                return True

def screen_message(main_text, secondary_text):
    white = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
    white.set_alpha(180)
    WIN.blit(white, (GAME_POS_X,GAME_POS_Y))

    text = GAME_FONT.render(main_text, 1, WHITE)
    y = ((GAME_HEIGHT - text.get_height()) // 2) + GAME_POS_Y - 20
    WIN.blit(text, (((WIDTH - text.get_width()) // 2), y))
    text2 = GAME_FONT_2.render(secondary_text, 1, WHITE)
    WIN.blit(text2, (((WIDTH - text2.get_width()) // 2), y + text.get_height()))

    pygame.display.update()

# screen display when snake makes a collision (lost)
def game_over():
    screen_message("GAME OVER", "PRESS ANY KEY TO PLAY AGAIN")
    pressed_key()

# screen display when game is paused
def pause():
    screen_message("PAUSED GAME", "PRESS ANY KEY TO CONTINUE")
    pressed_key()

# screen display when just opened the game
def start_screen():
    white = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
    white.set_alpha(180)
    WIN.blit(white, (GAME_POS_X,GAME_POS_Y))
    
    text = GAME_FONT_3.render("PRESS ANY KEY TO START", 1, WHITE)
    y = ((GAME_HEIGHT - text.get_height()) // 2) + GAME_POS_Y - 10
    WIN.blit(text, (((WIDTH - text.get_width()) // 2), y))
    pygame.display.update()
    pressed_key()
    return True

# redraws titles, scores and game area
def redraw_window(score, top_score):

    WIN.fill(GRAY)
    title = TITLE_FONT.render("SNAKE GAME", 1, PURPLE)
    WIN.blit(title, (((WIDTH - title.get_width()) // 2), (GAME_POS_Y - title.get_height()) // 2))
    pygame.draw.rect(WIN, BLACK, (GAME_POS_X, GAME_POS_Y, GAME_WIDTH, GAME_HEIGHT))
    score_label = SCORE_FONT.render(f"SCORE: {score}", 1, BLACK)
    WIN.blit(score_label, (GAME_POS_X, (HEIGHT - score_label.get_height() - 10)))
    topscore_label = SCORE_FONT.render(f"HIGHSCORE: {top_score}", 1, BLACK)
    WIN.blit(topscore_label, ((GAME_POS_X + GAME_WIDTH - topscore_label.get_width()), (HEIGHT - topscore_label.get_height() - 10)))


def main(start = False):

    # load highscore file and read value
    try:
        f = open(HS_FILE,"r")
        highscore = int(f.read())
        f.close()
    except:        
        highscore = 0  

    run = True
    FPS = 14
    # create snake object and food object
    snake = Snake(SNAKE_SIZE, GREEN)
    food = Food(SNAKE_SIZE, RED)
    direction = "right"
    score = 0
    clock = pygame.time.Clock()

    while run:

        clock.tick(FPS)
        snake.move_snake(direction)

        if snake.collision():
            game_over()
            main(True)  # restart game by calling main()

        if snake.grabbed_food(food):
            score +=10
            food.change_food(snake.body)
            snake.grow_snake(2)
            snake.change_color()
        
        if score > highscore:
            highscore = score
            # save new highscore in text file
            f = open(HS_FILE,"w")
            f.write(str(score))
            f.close()

        redraw_window(score, highscore)        
        snake.draw_snake(WIN)
        food.draw_food(WIN)

        if not start:
            start = start_screen()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause()
                    redraw_window(score, highscore)
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
