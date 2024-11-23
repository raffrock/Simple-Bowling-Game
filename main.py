# setting up basic pygame loop
from sys import exit
import pygame

# starts pygame
pygame.init()

    # will implement later
# get screen size
# infoObject = pygame.display.Info()
# screen_width = infoObject.current_w
# screen_height = infoObject.current_h
# screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Simple Bowling Game")
    # will implement later
# pygame.display.set_icon()

intro_font = pygame.font.Font(None,50)

    # change size later, and allow to be run on other computers
background_surface = pygame.image.load('/Users/rchetata/PycharmProjects/PythonProject/bowling_game_background.png')
# bowling_pin_icon = pygame.image.load('/Users/rchetata/PycharmProjects/PythonProject/bowling_pin_icon.png').convert_alpha()
# ball_icon = pygame.image.load('/Users/rchetata/PycharmProjects/PythonProject/tiny_ball_icon.png').convert()
# ball_rect = ball_circle.get_rect(center = (ball_rect_x,ball_rect_y))

ball_rect_x = 300
ball_rect_y = 750
roll = False
# ball_circle = pygame.draw.circle(screen, (0,0,0), (ball_rect_x, ball_rect_y), 7)

welcome_text_surface = intro_font.render("Welcome to my Simple Bowling Game!", False, 'Black')
welcome_text_x = 30

clock = pygame.time.Clock()

key_down = None
while True:
    # event loop to check for player input
    for event in pygame.event.get():
        # ball move moment with keyboard input
            # K_RIGHT and K_LEFT
        if event.type == pygame.KEYDOWN:
            key_down = event.key
        if event.type == pygame.KEYUP:
            if event.key is not pygame.K_UP:
                key_down = None
        # if player quits, quit pygame
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # controls to move ball
    if key_down == pygame.K_RIGHT:
        ball_rect_x += 5
    if key_down == pygame.K_LEFT:
        ball_rect_x -= 5
    if key_down == pygame.K_UP:
        roll = True
    # if key_down == pygame.K_DOWN:
    #     ball_rect_y = 750 # ball resets position
    #     roll = False

    if roll and ball_rect_y > 400:
        ball_rect_y -= 10
    elif ball_rect_y >= 400:
        ball_rect_y = 750
        roll = False

    # if not roll:
    #     ball_rect_y = 750

    screen.blit(background_surface,(0,0))
    screen.blit(welcome_text_surface,(welcome_text_x,20))
    # moves the text
    welcome_text_x -= 2
    if welcome_text_x < -700:
        welcome_text_x = 800

    # screen.blit(ball_circle, (ball_rect_x,ball_rect_y))
    pygame.draw.circle(screen, (35,36,36), (ball_rect_x, ball_rect_y), 30)

    pygame.display.flip()
    # pygame.display.update()
    clock.tick(60)  # limits FPS to 60
