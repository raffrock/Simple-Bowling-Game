# setting up basic pygame loop
from importlib.metadata import files
from sys import exit, displayhook
import pygame

#  NEXT:
#     turn pins and ball into spite classes
#     calculate score and display
#     split classes into separate files
#     calculate position (and size?) based on screen size, then allow screen size to vary
#     use bowling physic to affect how the pins fall

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

ball_rect_x = 300
ball_rect_y = 750
roll = False
ball_circle = pygame.draw.circle(screen, (35, 36, 36), (ball_rect_x, ball_rect_y), 7)

# if turns into sprite, can use multiple rectangles and better detect collusion
class Pin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 20, 30)
        self.visible = True

    def isVisible(self):
        return self.visible

    def isKnockedDown(self, ball_x, ball_y):
        if pin.y >= ball_y and abs(pin.x - ball_x) <= 30:
            self.visible = False

    def make_visible(self):
        self.visible = True

# holds list of all pins: ctor, getter of list, resets pin visibility
class AllPins:
    def __init__(self):
        self.pin_list = []
        self.pin_list.append(Pin(310, 410))
        self.pin_list.append(Pin(450, 410))
        self.pin_list.append(Pin(345, 420))
        self.pin_list.append(Pin(415, 420))
        self.pin_list.append(Pin(380, 430))

    def getPins(self):
        return self.pin_list

    def reset(self):
        for pin in self.pin_list:
            pin.make_visible()

    #  detect strike
    def strike(self):
        for pin in self.pin_list:
            if pin.visible:
                return False
        return True


welcome_text_surface = intro_font.render("Welcome to my Simple Bowling Game!", False, 'Black')
strike_text_surface = intro_font.render("All Pins Down!", False, 'Black')
top_text_x = 30

clock = pygame.time.Clock()

key_down = None
allPin = AllPins()

while True:
    # event loop to check for player input
    for event in pygame.event.get():
        # ball move moment with keyboard input
        if event.type == pygame.KEYDOWN:
            # can close with esc key
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            key_down = event.key
        # if key released, ball stops moving
        if event.type == pygame.KEYUP:
            key_down = None
        # if player quits, quit pygame
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    if not roll: # can only move when not rolling
        if key_down == pygame.K_RIGHT:
            ball_rect_x += 5
        if key_down == pygame.K_LEFT:
            ball_rect_x -= 5
        if key_down == pygame.K_UP:
            roll = True
    if key_down == pygame.K_DOWN:
        allPin.reset()

    if roll and ball_rect_y > 400:
        ball_rect_y -= 10
    elif ball_rect_y >= 400:
        ball_rect_y = 750
        roll = False

    # displays background and moving welcome text
    screen.blit(background_surface, (0, 0))
    if allPin.strike():
        screen.blit(strike_text_surface, (top_text_x, 20))
        # moves the text
        top_text_x -= 10
        if top_text_x < -500:
            top_text_x = 800
    else:
        screen.blit(welcome_text_surface, (top_text_x, 20))
        # moves the text
        top_text_x -= 2
        if top_text_x < -700:
            top_text_x = 800

    # draws bowling ball
    pygame.draw.circle(screen, (35, 36, 36), (ball_rect_x, ball_rect_y), 30)

    for pin in allPin.getPins():
        pin.isKnockedDown(ball_rect_x,ball_rect_y)
        if pin.isVisible():
            pygame.draw.rect(screen, "White", pin)

    pygame.display.flip()

    clock.tick(60)  # 60 FPS
