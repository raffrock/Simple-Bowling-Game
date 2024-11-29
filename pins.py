# class for pins intended to create pin objects
# display several pin objects
# detention collusion and disappear
# collect information for score reporting ex. areAllPinsDown() -> bool

import pygame

# tips
    # can use scale_by() to scale rectangles

# use percentages to calculate size and spacing
# 800

class Pin(pygame.sprite.Sprite):
    # list the colors for the four different rows
    down = False  # bool is pin is down or now

    def __init__(self, x, y, row, box_w, box_h): # takes in height and width of box that contains pins
        # calls sprite constructor
        pygame.sprite.Sprite.__init__(self)

        # decide width and height based on size of bowling pit
        # 7 pins visible, then add spacing (6 spaces between + 7 pins)
        self.width = (box_w // 7) - (box_w * 17)
        self.height = box_h * .9
        # self.pin_size = (self.width, self.height)

        self.image = pygame.image.load('Simple-Bowling-Game/pin_icon copy.png')
        # self.image = pygame.transform.scale(self.image, self.pin_size)

        # holds rect and positions pin based on inputs
        self.pin_rect = self.image.get_rect()
        self.pin_rect.x = x
        self.pin_rect.y = y

        self.x = x
        self.y = y

        # save row
        self.row = row

    def display(self, surface):
        surface.blit(self.image, (self.x, self.y))

    # def fall_down(self):
    #     # code for falling down animation
    #     # decides left or right?
    #
    #     down = True
    #
    # def put_back_up(self):
    #     # does as it says, it's for the reset
    #     down = False
    #
    # def knock_down(self):
    #     down = True
    #     # collusion test
    #     # prompts fall_down animation

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