import os
from sys import exit
import pygame

# import files
import bowling_ball
# import pins
from score_calcuator import Score
from pins_easy_pick import AllPins

import logging
logging.basicConfig(level=logging.DEBUG)

pygame.init()

# get screen size
# os.environ["SDL_VIDEO_CENTERS"] = '1'
# info = pygame.display.Info()
# window_width, window_height = info.current_w, info.current_h

clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 800), pygame.RESIZABLE) # has starting size
screen_width, screen_height = screen.get_size()

# background
game_background = screen.copy()
game_background.fill("White")
background_img = pygame.image.load('bowling_game_background.png')

pygame.display.set_caption("Simple Bowling Game")

class BowlingPit:
    def __init__(self):
        self.pit_width, self.pit_height = 0,0
        self.rect = pygame.Rect(0, 0, 0, 0)

    def update_pit(self):
        self.pit_width, self.pit_height = screen_width * .4, screen_height * .2
        self.rect = pygame.Rect(0, 0, self.pit_width, self.pit_height)
        self.rect.center = ((screen_width / 2), (screen_height / 2))

# text
score_font = pygame.font.Font(None, 40)
# put key instructions
instructions_font = pygame.font.Font(None, 10)

# music & sounds
# ball_crash_sound = pygame.mixer.Sound("ball_pin_collusion.m4a")
# background_music = pygame.mixer.Sound("crash.wav")

# create all elements
bowling_pit = BowlingPit()
bowling_pit.update_pit()
ball = bowling_ball.Ball(screen_width, screen_height, screen_height/2+30, "purple")
ball.set_speed(6,5)
new_all_pins = AllPins((screen_width / 2),screen_height/2+20, bowling_pit.pit_width)
new_game = Score()

screen.fill((250, 250, 250))

finish_roll = False
pin_reset = False

pygame.mixer.music.load('game-176807.mp3')
pygame.mixer.music.play(-1)

while True:
    # pygame.mixer.music.load('game-176807.mp3')
    # pygame.mixer.music.play()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                screen_width, screen_height = 800, 800
                background_scale = (screen_width, screen_height)
                background_img = pygame.transform.scale(background_img, background_scale)
                ball.update_x_y(screen_width, screen_height)
                bowling_pit.update_pit()
                new_all_pins.reset_size(screen_width/2, screen_height/2+20, bowling_pit.pit_width)
                # new_all_pins.set_y_value(screen_height/2)
            # reset game
            if event.key == pygame.K_RETURN:
                new_game.reset_score()
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # if resize, call all update functions:
        if event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = screen.get_size()
            background_scale = (screen_width, screen_height)
            background_img = pygame.transform.scale(background_img, background_scale)
            ball.update_x_y(screen_width, screen_height)
            bowling_pit.update_pit()
            new_all_pins.reset_size(screen_width/2, screen_height/2+20, bowling_pit.pit_width)
            # new_all_pins.set_y_value(screen_height/2)


    if ball.restart:
        # pygame.mixer.music.play()
        if new_game.game_end:
            # pygame.time.delay(50)
            new_game.reset_score()
            new_game.game_end = False
            new_all_pins.reset_all()
            # if new_all_pins.pins_down >= 1:
            #     done_falling = True
            #     for pin in new_all_pins.all_pins:
            #         if pin.falling_countdown > -2:
            #             done_falling = False
            #     if done_falling:
            #         new_all_pins.reset_all()
            pin_reset = True
            new_game.add_to_turn(new_all_pins.pins_down)
        if ball.roll_count == 1:
            new_game.add_to_turn(new_all_pins.pins_down)
        if ball.roll_count == 2:
            new_game.add_to_turn(new_all_pins.pins_down)
            new_all_pins.reset_all()
            # if new_all_pins.pins_down >= 1:
            #     done_falling = True
            #     for pin in new_all_pins.all_pins:
            #         if pin.falling_countdown > -2:
            #             done_falling = False
            #     if done_falling:
            #         new_all_pins.reset_all()
            pin_reset = True

        # if pin_reset and new_all_pins.pins_down >= 1:
        #     done_falling = True
        #     for pin in new_all_pins.all_pins:
        #         if pin.falling_countdown > 0:
        #             done_falling = False
        #     if done_falling:
        #         pin_reset = False
        #         new_all_pins.reset_all()


    screen.blit(background_img, (0, 0))
    # pygame.draw.rect(screen, "black", bowling_pit.rect)

    score_text = score_font.render(new_game.return_score_str(), False, 'Black')
    screen.blit(score_text, (10, 20))

    ball.move()

    if ball.get_if_roll():
        ball.roll()

    # display ball
    bowling_pit.update_pit()
    new_all_pins.display(screen, ball.rect.centerx, ball.rect.centery)
    ball.display(screen)

    pygame.display.flip()
    clock.tick(60)  # 60 FPS