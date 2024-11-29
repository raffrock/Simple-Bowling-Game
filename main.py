# from importlib.metadata import files
from sys import exit
import pygame

# import files
import bowling_ball
import pins

#  NEXT:
#     calculate score and display (think Bowling Game Kata)
#     turn pins and ball into spite classes
#     create background in python so it can be resize?
#     create floor for ball to "roll over off" and pins to stand on?
#     create new background
#     split classes into separate files
#     create falling animation with wait time before pin disappears, delay shooting as well
#     calculate position (and size?) based on screen size, then allow screen size to vary
#     use bowling physic to affect how the pins fall
#         use all 10 pins and find probability of what pins fall based on pin hit
#         store options as dict then randomize pick
#         or if there are patterns, use a function calcuate which pins should fall
#     press H to toggle keyboard inputs
#     press S for settings
#         include music?
#     press T for tips or another key or likelihood of strike?

# starts pygame
pygame.init()

    # allow for full size
# get screen size
# infoObject = pygame.display.Info()
# screen_width = infoObject.current_w
# screen_height = infoObject.current_h
# screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Simple Bowling Game")
    # will implement later
# pygame.display.set_icon()

intro_font = pygame.font.Font(None, 50)

background_surface = pygame.image.load('bowling_game_background.png')

welcome_text_surface = intro_font.render("Welcome to my Simple Bowling Game!", False, 'Black')
strike_text_surface = intro_font.render("All Pins Down!", False, 'Black')
top_text_x = 30

clock = pygame.time.Clock()

# def __init__(self, floor_x, floor_y, limit_y, color):
ball = bowling_ball.Ball(400, 500, 200, "purple")
ball.set_speed(5,5)

# def __init__(self, x, y, row, box_w, box_h)
pin = pins.Pin(50, 200, 1, 100, 200)

while True:
    # event loop to check for player input
    for event in pygame.event.get():
        # ball move moment with keyboard input
        if event.type == pygame.KEYDOWN:
            # can close with esc key
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            # else:
            #     key_down = event.key
        # # if key released, ball stops moving
        # if event.type == pygame.KEYDOWN:
        #     key_down = None
        # if player quits, quit pygame
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # displays background and moving welcome text
    screen.blit(background_surface, (0, 0))

    ball.move()

    if ball.get_if_roll():
        ball.roll()

    pin.display(screen)
    ball.display(screen)

    pygame.display.flip()

    clock.tick(60)  # 60 FPS
