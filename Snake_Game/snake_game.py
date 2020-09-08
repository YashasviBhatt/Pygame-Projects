# Snake Game using Pygame

# importing the libraries
import pygame as pg
from random import randint
import os

# initializing the modules of pygame
pg.init()

# colors
# ceating a tuple mentioning the values of r, g, b
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

# setting up the screen
screen_width = 1000
screen_height = 600
gameWindow = pg.display.set_mode((screen_width, screen_height))             # creating a screen with width and height
pg.display.set_caption('Snake Game by Yashasvi Bhatt')                      # giving the title to game window

fps = 60                                                                    # setting up frames per second

font = pg.font.SysFont(None, 55)                                            # taking system font
# function to display text on screen
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)                            # render() is used to draw text on screen
    gameWindow.blit(screen_text, [x, y])                                    # blit to update the screen with new drawings

# function to increase snake length
def plot_snake(color, snake_list, size):
    for x, y in snake_list:
        pg.draw.rect(gameWindow, color, [x, y, size, size])

clock = pg.time.Clock()                                                     # creating a clock variable to update screen time to time

# creating a function for game
def gameloop():
    # creating game specific variables
    exit_game = False                                                       # creating exit flag
    game_over = False                                                       # creating game over flag
    pause = False                                                           # creating pause flag

    snake_x = randint(100, 500)                                             # starting point of snake head in x direction
    snake_y = randint(100, 500)                                             # starting point of snake head in y direction

    velocity_x = 3                                                          # initial velocity of snake with which snake be moving at x direction
    velocity_y = 0                                                          # initial velocity of snake with which snake be moving at y direction
    speed = velocity_x                                                      # setting the speed

    size = 10                                                           # size of snake head

    food_x = randint(size, screen_width - size)                         # x coordinate of food
    food_y = randint(50 + size, screen_height - (50 + size))            # y coordinate of food

    score = 0                                                           # to add score functionality
    dir = 'r'                                                           # creating a direction flag, indicating direction of snake movement
    value = 10
    food_counter = 0

    snake_list = list()
    snake_length = 1

    if not os.path.exists('hs'):
        with open('hs', 'w') as f:
            f.write('0')
    with open('hs', 'r') as f:
        hiscore = f.read()

    # game loop
    while not exit_game:
        if pause:
            text_screen('Game Paused', green, screen_width // 2 - 125, screen_height // 2 - 30)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    gameWindow.fill(white)
                    text_screen('Exiting Game', blue, screen_width // 2 - 120, screen_height // 2 - 30)
                    exit_game = True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        pause = False
        if game_over:
            with open('hs', 'w') as f:
                f.write(hiscore)
            text_screen(f'Game Over! Press E to continue', red, screen_width // 4 - 35, screen_height // 2 - 30)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    gameWindow.fill(white)
                    text_screen('Exiting Game', blue, screen_width // 2 - 120, screen_height // 2 - 30)
                    exit_game = True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_e:
                        gameloop()
        else:
            for event in pg.event.get():                                            # fetching event from event queue
                if event.type == pg.QUIT:                                           # if quit event is fetched
                    gameWindow.fill(white)
                    text_screen('Exiting Game', blue, screen_width // 2 - 120, screen_height // 2 - 30)
                    exit_game = True
                elif event.type == pg.KEYDOWN:                                      # if key event is fetched
                    if event.key == pg.K_RIGHT or event.key == pg.K_d:
                        if dir == 'l':
                            pass
                        else:
                            velocity_x = speed                                      # incrementing the velocity of snake to move towards x dir
                            velocity_y = 0                                          # setting the velocity in other direction to 0
                            dir = 'r'
                    elif event.key == pg.K_LEFT or event.key == pg.K_a:
                        if dir == 'r':
                            pass
                        else:
                            velocity_x = -speed                                     # decrementing the velocity of snake to move against x dir
                            velocity_y = 0                                          # setting the velocity in other direction to 0
                            dir = 'l'
                    elif event.key == pg.K_UP or event.key == pg.K_w:
                        if dir == 'd':
                            pass
                        else:
                            velocity_y = -speed                                     # incrementing the velocity of snake to move against y dir
                            velocity_x = 0                                          # setting the velocity in other direction to 0
                            dir = 'u'
                    elif event.key == pg.K_DOWN or event.key == pg.K_s:
                        if dir == 'u':
                            pass
                        else:
                            velocity_y = speed                                      # incrementing the velocity of snake to move towards y dir
                            velocity_x = 0                                          # setting the velocity in other direction to 0
                            dir = 'd'
                    elif event.key == pg.K_p:
                        pause = True

            snake_x += velocity_x
            snake_y += velocity_y

            rect_center = size // 2

            # increasing score
            if abs((snake_x + rect_center) - food_x) < 10 and abs((snake_y + rect_center) - food_y) < 10:
                snake_length += 5
                score += 1
                food_counter += 1
                if food_counter > 5:
                    value += 1                                                      # increasing score increase factor
                    speed += 0.4                                                    # speeding up the gameplay
                    food_counter = 0                                                # resetting food counter
                    pg.display.update()
                food_x = randint(size, screen_width - size)                         # new x coordinate of food
                food_y = randint(50 + size, screen_height - (50 + size))            # new y coordinate of food

            gameWindow.fill(white)                                                  # filling the game window with white color

            #text_screen('FPS : '+str(fps), blue, 845, 5)                            # display the fps
            pg.draw.rect(gameWindow, green, (0, 0, screen_width, 45))
            text_screen('Score : ' + str(score * value) + '   Highscore : ' + hiscore, blue, 5, 5) # calling text_screen function to display score on screen
            final_score = score * value
            if final_score > int(hiscore):
                hiscore = str(final_score)

            head = list()
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                game_over = True

            if snake_x > (screen_width - 10) or snake_x < 0 or snake_y > (screen_height - 10) or snake_y < 47:
                game_over = True

            pg.draw.circle(gameWindow, red, (food_x, food_y), size - 5)             # creating food
            plot_snake(black, snake_list, size)                                     # calling function to generate snake

        # drawing border
        pg.draw.rect(gameWindow, green, [0, 0, 0, screen_height])
        pg.draw.rect(gameWindow, green, [screen_width - 1, 0, screen_width - 1, screen_height])
        pg.draw.rect(gameWindow, green, [0, screen_height - 1, screen_width, screen_height - 1])
        pg.display.update()                                                     # updating the screen with all the new changes
        clock.tick(fps)                                                         # updates the number of frame after every 1 second

gameloop()

pg.quit()
quit()