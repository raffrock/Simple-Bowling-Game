# from importlib.metadata import files
from sys import exit
import pygame
import numpy as np
from pygame import RESIZABLE, VIDEORESIZE

# import files
import bowling_ball
# import pins
from score_calcuator import Score
from pins_easy_pick import AllPins

import logging
logging.basicConfig(level=logging.DEBUG)

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


# new collusion method
    # save angle of fall, for animation and collusion with other pins
    # if pin is in front, it can test for collusion with ball
    # if 1,2,3 are down 5,8,9 can check for ball collusion, otherwise not

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
score_font = pygame.font.Font(None, 50)

background_img = pygame.image.load('bowling_game_background.png')
# background_scene = pygame.display.set_mode((800,800), RESIZABLE)

welcome_text_surface = intro_font.render("Welcome to my Simple Bowling Game!", False, 'Black')
strike_text_surface = intro_font.render("All Pins Down!", False, 'Black')
top_text_x = 30

clock = pygame.time.Clock()

# def __init__(self, floor_x, floor_y, limit_y, color):
ball = bowling_ball.Ball(400, 600, 305, "purple")
ball.set_speed(5,5)

new_all_pins = AllPins()
new_game = Score()

while True:
    # event loop to check for player input
    for event in pygame.event.get():
        # ball move moment with keyboard input
        if event.type == pygame.KEYDOWN:
            # can close with esc key
            # if event.key == pygame.KEYUP:
                # roll_count += 1
                # logging.debug("roll_count: " + str(roll_count))
            if event.key == pygame.K_RETURN:
                if ball.roll_count == 1:
                    new_game.add_to_turn(new_all_pins.pins_down)
                if ball.roll_count == 2:
                    new_game.add_to_turn(new_all_pins.pins_down)
                    new_all_pins.reset_all()
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # if event.type == VIDEORESIZE:
            # background_scene = pygame.display.set_mode(
                # event.dict['size'], RESIZABLE)
            # background_scene.blit(pygame.transform.scale(background_img, event.dict['size']), (0, 0))

    screen.blit(background_img, (0, 0))
    # pygame.display.set_mode()
    # screen.fill((250, 250, 250))

    # if not pins.check_for_strike():
    #     screen.blit(welcome_text_surface, (top_text_x, 20))
    # else:
    #     screen.blit(strike_text_surface, (top_text_x, 20))

    score_text = intro_font.render(new_game.return_score_str(), False, 'Black')
    screen.blit(score_text, (0, 20))

    # moves the text
    # top_text_x -= 2
    # if top_text_x < -700:
    #     top_text_x = 800

    ball.move()

    if ball.get_if_roll():
        ball.roll()

    # pins.display_pins(screen, ball.ball_rect)
    new_all_pins.display(screen, ball.x, ball.y)

    # display ball
    ball.display(screen)

    pygame.display.flip()

    clock.tick(100)  # 60 FPS
