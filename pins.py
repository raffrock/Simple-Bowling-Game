# class for pins intended to create pin objects
# display several pin objects
# detention collusion and disappear
# collect information for score reporting ex. areAllPinsDown() -> bool

import pygame
import numpy as np

# tips
    # can use scale_by() to scale rectangles

# use percentages to calculate size and spacing
# 800

class Pin(pygame.sprite.Sprite):
    # list the colors for the four different rows

    def __init__(self, x, y, row, box_w, box_h): # takes in height and width of box that contains pins
        # calls sprite constructor
        pygame.sprite.Sprite.__init__(self)

        # decide width and height based on size of bowling pit
        # 7 pins visible, then add spacing (6 spaces between + 7 pins)
        self.width = box_w / 7  #- (box_w * 17)
        # self.height = box_h * .9
        self.height = 20
        # self.pin_size = (self.width, self.height)

        self.image = pygame.image.load('Simple-Bowling-Game/pin_icon copy.png')
        self.image = pygame.transform.rotozoom(self.image, 0, .6)
        # self.image = pygame.transform.scale(self.image, self.pin_size)

        self.x = x
        self.y = y

        self.fall_x = x
        self.fall_y = y

        # holds rect and positions pin based on inputs
        self.pin_rect = pygame.Rect(self.x + (self.width // 2), self.y, self.width, self.height)

        # save row
        self.row = row

        self.down = False  # bool is pin is down or now
        self.falling = 3 # countdown of fall
        self.fall_direction = -1  # holds fall direction

    def display(self, surface, ball_rect):
        if self.test_for_collusion(ball_rect):
            self.knock_down(ball_rect)

        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN]:
            self.reset()
            self.falling = 3 # reset count, use for animation later

        if not self.down:
            surface.blit(self.image, (self.x, self.y))
        elif self.down and self.falling >= 0:
            self.falling -= 1
            if self.fall_direction > 0:
                self.fall_x -= 1
                surface.blit(self.image, (self.fall_x, self.fall_y))
            if self.fall_direction < 0:
                self.fall_x += 1
                surface.blit(self.image, (self.fall_x, self.fall_y))

        self.pin_rect = pygame.Rect(self.x + (self.width // 2), self.y, self.width, self.height)

    # def fall_down(self):
    #     # code for falling down animation
    #     # decides left or right?
    #
    #     down = True
    #
    def reset(self):
        self.down = False
        self.fall_x = self.x
        self.fall_y = self.y
        self.fall_direction = 0

    def test_for_collusion(self, collusion_rect):
        return pygame.Rect.colliderect(self.pin_rect, collusion_rect)

    def knock_down(self, collusion_object):
        self.down = True
        self.fall_direction = self.pin_rect.centerx - collusion_object.centerx
        # prompts fall_down animation

"""
  7   8   9  10
    4   5   6
      2   3
        1
"""
# create all pins
pin1 = Pin(175, 300, 1, 500, 300)
pin2 = Pin(133, 300, 2, 500, 300)
pin3 = Pin(217, 300, 2, 500, 300)
pin4 = Pin(91, 300, 3, 500, 300)
pin5 = Pin(175, 300, 3, 500, 300)
pin6 = Pin(250, 300, 3, 500, 300)
pin7 = Pin(50, 300, 4, 500, 300)
pin8 = Pin(133, 300, 4, 500, 300)
pin9 = Pin(217, 300, 4, 500, 300)
pin10 = Pin(300, 300, 4, 500, 300)

all_pins = [pin1,pin2,pin3,pin4,pin5,pin6,pin7,pin8,pin9,pin10]

"""
  7   8   9  10
    4   5   6
      2   3
        1
"""
def fall_impact(pin):
    probability_of_hit = np.random.randint(1,100) # need 100 to hit

    potential_knock_downs = { # left, right
        1 : [2,3],
        2 : [4,5],
        3 : [5,6],
        4 : [7,8],
        5 : [8,9],
        6 : [9,10]
    }
    # if probability_of_hit > 90 and all_pins_up() == True and (all_pins.index(pin) == 1 or all_pins.index(pin) == 2): # hit 2 and 3 pin, possible strike
    # currently, strike is not possible
    if all_pins_up() == True and (all_pins.index(pin) == 1 or all_pins.index(pin) == 2): # hit 2 and 3 pin, possible strike
        strike()
    elif probability_of_hit < 20:
        if pin.fall_direction != 0: # pin has fallen and recently
            if 0 < all_pins.index(pin) < 7: # only row 1 and 2 can knock down others
                if pin.fall_direction > 0:
                    # fall left
                    pin_hit = potential_knock_downs[all_pins.index(pin)][0]-1 # get number of pin hit
                    if not all_pins[pin_hit].down: # if pin hasn't already been hit
                        all_pins[pin_hit].knock_down(pin.pin_rect)
                elif pin.fall_direction < 0:
                    # fall right
                    pin_hit = potential_knock_downs[all_pins.index(pin)][1]-1 # get number of pin hit
                    if not all_pins[pin_hit].down: # if pin hasn't already been hit
                        all_pins[pin_hit].knock_down(pin.pin_rect)
                # else:
                    # fall straight
                    # not including right now, will need to add center values to potential_knock_downs

            pin.fall_direction = 0 # pin is not falling, so not direction

def display_pins(surface, ball_rect):
    for display_pin in all_pins:
        display_pin.display(surface, ball_rect)
        if display_pin.down:
            fall_impact(display_pin)

def check_for_strike():
    for pin in all_pins:
        if not pin.down:
            return False
    return True

def all_pins_up():
    for pin in all_pins:
        if pin.down:
            return False
    return True

def strike():
    for pin in all_pins:
        pin.down = True

# allPins.add()

# if turns into sprite, can use multiple rectangles and better detect collusion
# class Pin:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.rect = pygame.Rect(x, y, 20, 30)
#         self.visible = True
#
#     def isVisible(self):
#         return self.visible
#
#     def isKnockedDown(self, ball_x, ball_y):
#         if pin.y >= ball_y and abs(pin.x - ball_x) <= 30:
#             self.visible = False
#
#     def makeVisible(self):
#         self.visible = True

# holds list of all pins: ctor, getter of list, resets pin visibility
# class AllPins:
#     def __init__(self):
#         self.pin_list = []
    #     self.pin_list.append(Pin(310, 410))
    #     self.pin_list.append(Pin(450, 410))
    #     self.pin_list.append(Pin(345, 420))
    #     self.pin_list.append(Pin(415, 420))
    #     self.pin_list.append(Pin(380, 430))
    #
    # def getPins(self):
    #     return self.pin_list
    #
    # def reset(self):
    #     for pin in self.pin_list:
    #         pin.makeVisible()
    #
    # #  detect strike
    # def strike(self):
    #     for pin in self.pin_list:
    #         if pin.visible:
    #             return False
    #     return True

    # if all_pins.strike():
    #     screen.blit(strike_text_surface, (top_text_x, 20))
    #     # moves the text
    #     top_text_x -= 10
    #     if top_text_x < -500:
    #         top_text_x = 800
    # else:
    #     screen.blit(welcome_text_surface, (top_text_x, 20))
    #     # moves the text
    #     top_text_x -= 2
    #     if top_text_x < -700:
    #         top_text_x = 800