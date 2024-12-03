# creates pin can randomize their fall direction
# rather than being informed by collusion object's position

import pygame
import numpy as np
import math
    # for conlog statements
import logging
logging.basicConfig(level=logging.DEBUG)

class Pin:

    # pin input information: position, number
    # hidden information: active, down, fall direction

    potential_knock_downs = { # left, right
        1 : [2,3],
        2 : [4,5],
        3 : [5,6],
        4 : [7,8],
        5 : [8,9],
        6 : [9,10],
    }

    def __init__(self, number, x, y):
        self.image = pygame.image.load('Simple-Bowling-Game/pin_icon copy.png')
        self.image = pygame.transform.rotozoom(self.image, 0, .6)
        self.image_rotate = self.image.copy()

        self.x = x
        self.y = y
        self.number = number

        # assume pin is 30 pixels wid
        self.pin_range_low = x - 20
        self.pin_range_high = x + 30

        self.down = False
        self.fall_direction = "none"
        if number in [5,6,7]:
            self.active = False
        else:
            self.active = True

        self.left = False
        self.right = False
        self.falling_countdown = 0

    def knock_down(self):
        self.active = False
        self.down = True
        self.falling_countdown = 5

        # decide left, right, or straight
        left_or_right = np.random.randint(1, 4) # range: [0,4)
        if left_or_right == 1:
            self.left = True
        elif left_or_right == 2:
            self.right = True

    def reset(self):
        if self.number in [5,6,7]:
            self.active = False
        else:
            self.active = True
        self.down = False
        self.image_rotate = self.image.copy()
        self.left = False
        self.right = False


    def display(self, surface):
        # key = pygame.key.get_pressed()
        # if key[pygame.K_DOWN]:
        #     self.reset()
        # if self.active:
        #     self.test_if_ball_collusion(ball_x)
        # display pin up or falling

        if not self.down:
            surface.blit(self.image, (self.x, self.y))
        elif self.down and self.falling_countdown > 0:
            if self.left:
                self.image_rotate = pygame.transform.rotate(self.image_rotate,5)
                surface.blit(self.image_rotate, (self.x, self.y))
            elif self.right:
                self.image_rotate = pygame.transform.rotate(self.image_rotate, -5)
                surface.blit(self.image_rotate, (self.x, self.y))
            self.falling_countdown -= 1

    def test_if_ball_collusion(self, ball_x, ball_y):
        if self.pin_range_low <= ball_x <= self.pin_range_high and abs(self.y-ball_y) <= 10: # margin of error
            # probability_of_hit = np.random.randint(1, 100)  # need over 60 to hit
            # if probability_of_hit > 60:
            #     self.knock_down()
            self.knock_down()
            return True
            # self.test_for_collateral()
        return False
    
    def test_for_collateral(self):
        probability_of_hit = np.random.randint(1, 100)  # need 80 to hit
        logging.debug("probability of collateral: " + str(probability_of_hit))
        if self.number in self.potential_knock_downs.keys() and probability_of_hit > 20:
            # return number of pin to be knocked down
            if self.left:
                logging.debug("collateral pin: " + str(self.number) + "->" + str(self.potential_knock_downs[self.number][0]))
                return self.potential_knock_downs[self.number][0]
            elif self.right:
                logging.debug("collateral pin: " + str(self.number) + "->" + str(self.potential_knock_downs[self.number][1]))
                return self.potential_knock_downs[self.number][1]
        return 0

class AllPins:
    all_pins = []
    x_values = [0, 170, 130, 210, 90, 170, 250, 50, 130, 210, 290]

    cover_mapping = {
        1 : 5,
        2 : 8,
        3 : 9
    }

    def __init__(self):
        for i in range(1,11):
            curr_x_val = self.x_values[i]
            self.all_pins.append( Pin(i, curr_x_val, 300) )

        self.pins_down = 0

    def set_x_values(self, new_x_values):
        for i in range(0,len(new_x_values)):
            self.all_pins[i].x = new_x_values[i]

    def set_y_values(self, new_y_values):
        for i in range(0,len(new_y_values)):
            self.all_pins[i].y = new_y_values[i]

    def display(self, surface, ball_x, ball_y):
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN]:
            self.reset_all()
        else:
            for pin in self.all_pins:
                # check if ball hit pin
                if not pin.down and pin.test_if_ball_collusion(ball_x, ball_y):
                    self.pins_down += 1

                    # strike possibility
                    if self.pins_down == 1 and (pin.number == 2 or pin.number == 3):
                        probability_of_strike = np.random.randint(1, 100)
                        if probability_of_strike > 90:
                            self.strike()

                    logging.debug("pin hit: " + str(pin.number))
                    logging.debug("pins down: " + str(self.pins_down))

                    # change hidden pins to active if needed
                    if pin.number in [1,2,3]: # pins that cover others
                        now_active = 0
                        if pin.number == 1:
                            now_active = 5
                        elif pin.number == 2:
                            now_active = 8
                        elif pin.number == 3:
                            now_active = 9
                        # now_active = self.cover_mapping[pin.number]
                        if not self.all_pins[now_active-1].down:
                            self.all_pins[now_active-1].active = True

                    # save number that will be hit
                    collateral_num = pin.test_for_collateral()
                    # while there is a collateral pin
                    while collateral_num != 0 and not self.all_pins[collateral_num-1].down:
                        self.pins_down += 1
                        logging.debug("pins down: " + str(self.pins_down))
                        # logging.debug("Pit Collateral: " + str(collateral_num))
                        self.all_pins[collateral_num-1].knock_down()
                        collateral_num = pin.test_for_collateral()
                pin.display(surface)
                # pin_rect = pin.image_rotate.get_rect()
                # Rect(left, top, width, height)
                if pin.active:
                    pin_rect = pygame.Rect(pin.x, pin.y, (pin.pin_range_high-pin.pin_range_low), 10)
                    # pin_rect = pin.image.get_rect()
                    pygame.draw.rect(surface, (250,250,250), pin_rect)

    def reset_all(self):
        self.pins_down = 0
        for pin in self.all_pins:
            pin.reset()

    def strike(self):
        for pin in self.all_pins:
            pin.down = True
            pin.left = True
        self.pins_down = 10

    def get_hit_coor_x(self):
        x_vals = []
        for pin in self.all_pins:
            if pin.active:
                x_vals.append([pin.pin_range_low, pin.pin_range_high])
            else:
                x_vals.append([0,0])
        return x_vals

    def get_hit_coor_y(self):
        y_vals = []
        for pin in self.all_pins:
            if pin.active:
                y_vals.append(pin.y)
            else:
                y_vals.append(0)
        return y_vals
