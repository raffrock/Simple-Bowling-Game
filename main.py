import os
from sys import exit
import pygame

# import files
from bowling_ball import Ball
from score_calcuator import Score
from pins import AllPins

import logging
logging.basicConfig(level=logging.DEBUG)

pygame.init()

#   WHAT TO WORK ON NEXT:
    # make resizing better (ball and pins)
    # add more variety to pin knock down patterns
    # figure out how to display instructions_text
    # add ball rolling sound effect
    # redraw background
    # title screen/intro with ability to pick ball color?

clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 800), pygame.RESIZABLE) # has starting size
screen_width, screen_height = screen.get_size()

# background
game_background = screen.copy()
game_background.fill("White")
background_img = pygame.image.load('bowling_game_background.png')

pygame.display.set_caption("Simple Bowling Game")

# create bowling pit class to call update function later
class BowlingPit:
    def __init__(self):
        self.width, self.height = screen_width * .4, screen_height * .2
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = ((screen_width / 2), (screen_height / 2))

    def update_pit(self):
        self.width, self.height = screen_width * .4, screen_height * .2
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = ((screen_width / 2), (screen_height / 2))

# text
score_font = pygame.font.Font(None, 40)
# key instructions
    # P to turn off sound
    # left and right to move ball
    # up to shoot/roll
    # back to reset pins
    # enter to reset game
    # Space to hide instructions
    # delete to close game
instructions_font = pygame.font.Font(None, 40)
instructions_text = instructions_font.render('Left and Right to move ball.\nUp to roll.\nBack to reset pins.\nEnter to reset game.\nSpace to toggle instructions.\nP to turn off sound.', False,"Black")
toggle_instructions = False

# create all elements
pit = BowlingPit()
ball = Ball(screen_width, screen_height, screen_height/2+30, "purple")
ball.set_speed(6,5)
pins = AllPins((screen_width / 2), screen_height / 2 + 20, pit.width)
game = Score()

# allows for delay for pin reset
pin_reset = False
pin_reset_countdown = 10

# plays music, and allows to be turned off
pygame.mixer.music.load('game_music.mp3')
pygame.mixer.music.play(-1)
toggle_sound = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # quit with backspace key
            if event.key == pygame.K_BACKSPACE:
                pygame.quit()
                exit()
            # show/hide instructions
            if event.key == pygame.K_SPACE:
                toggle_instructions = not toggle_instructions
                if toggle_instructions:
                    screen.blit(instructions_text, (0, 0))
            # return screen to default size and update position of everything
            if event.key == pygame.K_ESCAPE:
                screen_width, screen_height = 800, 800
                background_scale = (screen_width, screen_height)
                background_img = pygame.transform.scale(background_img, background_scale)
                ball.update_x_y(screen_width, screen_height)
                pit.update_pit()
                pins.reset_size(screen_width / 2, screen_height / 2 + 20, pit.width)
            # reset game
            if event.key == pygame.K_RETURN:
                game.reset_score()
                pins.reset_all()
            # turn off music and sound effects with p
            if event.key == pygame.K_p:
                toggle_sound = not toggle_sound
                pins.toggle_sound()
                if toggle_sound:
                    pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.stop()
        # if window resized, call all update functions:
        if event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = screen.get_size()
            background_scale = (screen_width, screen_height)
            background_img = pygame.transform.scale(background_img, background_scale)
            ball.update_x_y(screen_width, screen_height)
            pit.update_pit()
            pins.reset_size(screen_width / 2, screen_height / 2 + 20, pit.width)
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # controls pin reset delay
    if pin_reset:
        logging.debug("pin_reset: " + str(pin_reset_countdown))
        if pin_reset_countdown > 0:
            pin_reset_countdown -= 1
        else:
            pin_reset_countdown = 10
            pin_reset = False
            pins.reset_all()


    if ball.restart:
        if game.game_end:
            # reset after end of game (10 frames)
            game.reset_score()
            game.game_end = False
            game.add_to_turn(pins.pins_down)
            if pins.pins_down == 10:
                ball.roll_count = 0
            pin_reset = True
        elif ball.roll_count == 1:
            game.add_to_turn(pins.pins_down)
            # reset after strike
            if pins.pins_down == 10:
                ball.roll_count = 0
                pin_reset = True
        if ball.roll_count == 2:
            game.add_to_turn(pins.pins_down)
            # reset after turn (2 rolls if not strike)
            pin_reset = True

    screen.blit(background_img, (0, 0))
    if toggle_instructions:
        screen.blit(instructions_text, (0, 0))

        # to check if pit is in correct position
    # pygame.draw.rect(screen, "black", bowling_pit.rect)

    score_text = score_font.render(game.return_score_str(), False, 'Black')
    screen.blit(score_text, (10, 20))

    ball.move()

    if ball.get_if_roll():
        ball.roll()

    # display ball
    pins.display(screen, ball.rect.centerx, ball.rect.centery)
    ball.display(screen)

    pygame.display.flip()
    clock.tick(60)  # 60 FPS