# Pin creates pins that test for ball collusion and whose fall direction is decided by collusion object's position
# AllPins to stores and control all pins, including reset and collateral falls

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
        self.image = pygame.image.load('pin_icon_positions/pin_icon_0.png')
        self.image = pygame.transform.rotozoom(self.image, 0, .65)
        self.image_rotate = self.image.copy()
        self.pin_height = self.image.get_height()
        self.pin_width = self.image.get_width()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y+self.pin_height//2)
        self.reset_rect = self.rect
        self.reset_rect.center = self.rect.center

        self.number = number

        self.pin_range_low = self.rect.centerx - self.pin_width/7
        self.pin_range_high = self.rect.centerx + self.pin_width/7 + 20 # to off-set ball being off center

        self.down = False
        self.fall_direction = "none"
        if number in [5,8,9]:
            self.active = False
        else:
            self.active = True

        self.left = False
        self.right = False
        self.falling_countdown = 0

    def knock_down(self, object_x):
        self.active = False
        self.down = True
        self.falling_countdown = 10

        # decide left or right based on position of collusion object
        if self.rect.centerx > object_x: # to left of pin
            self.left = True
        elif self.rect.centerx < object_x:
            self.right = True
        # else straight -> falls straight back

    def reset(self):
        if self.number in [5,8,9]:
            self.active = False
        else:
            self.active = True
        self.down = False
        self.image_rotate = self.image.copy()
        self.left = False
        self.right = False
        self.falling_countdown = 0

        self.rect.center = self.reset_rect.center

    def pin_animation(self):
        path = "pin_icon_positions/pin_icon_"
        if self.falling_countdown == 5:
            path += "1.png"
        elif self.falling_countdown == 4:
            path += "2.png"
        elif self.falling_countdown == 3:
            path += "3.png"
        elif self.falling_countdown == 2:
            path += "4.png"
        else:
            path += "5.png"
        self.image_rotate = pygame.image.load(path)
        self.image_rotate = pygame.transform.rotozoom(self.image_rotate, 0, .6)

    def display(self, surface):
        if not self.down:
            self.reset_rect.center = self.rect.center
            surface.blit(self.image, self.rect)
        elif self.down and self.falling_countdown != 0:
            if self.left:
                self.pin_animation()
                self.image_rotate = pygame.transform.flip(self.image_rotate, True, False)
                surface.blit(self.image_rotate, (self.rect.centerx, self.rect.centery-self.falling_countdown))
            elif self.right:
                self.pin_animation()
                surface.blit(self.image_rotate, (self.rect.centerx, self.rect.centery-self.falling_countdown))
            self.falling_countdown -= 1

    def test_if_ball_collusion(self, ball_x, ball_y):
        if self.pin_range_low <= ball_x <= self.pin_range_high and abs(self.rect.y-ball_y) <= self.pin_height: # margin of error
            self.knock_down(ball_x)
            return True
        return False
    
    def test_for_collateral(self):
        probability_of_hit = np.random.randint(1, 100)  # need 80 to hit
        logging.debug("probability of collateral: " + str(probability_of_hit))
        if self.number in self.potential_knock_downs.keys() and probability_of_hit > 50:
            # return number of pin to be knocked down
            if self.left:
                logging.debug("collateral pin: " + str(self.number) + "->" + str(self.potential_knock_downs[self.number][0]))
                return self.potential_knock_downs[self.number][0]
            elif self.right:
                logging.debug("collateral pin: " + str(self.number) + "->" + str(self.potential_knock_downs[self.number][1]))
                return self.potential_knock_downs[self.number][1]
        return 0

class AllPins:
    cover_mapping = {
        1: 5,
        2: 8,
        3: 9
    }

    def __init__(self, center_x, floor_y, pit_width):
        # list to hold pins
        self.all_pins = []

                # 1->9
                # 2->8 3->9
                # 4 (5) 6
                # 7 (8) (9) 10
        self.image = pygame.image.load('pin_icon_positions/pin_icon_0.png')
        self.image = pygame.transform.rotozoom(self.image, 0, .6)
        pin_space = pit_width // 10 #- pin_width
        x_values = [center_x,
                    center_x-pin_space,
                    center_x+pin_space,
                    center_x - pin_space*2,
                    center_x,
                    center_x + pin_space * 2,
                    center_x - pin_space * 3,
                    center_x - pin_space,
                    center_x + pin_space,
                    center_x + pin_space * 3]

        # for i in range(9, -1, -1):
        for i in range(0, 10):
            curr_x_val = x_values[i]
            self.all_pins.append(Pin(i+1, curr_x_val + 1, floor_y))

            self.pins_down = 0

        # control sound effect for pins crashing
        self.sound_effect = True

    def reset_size(self, center_x, center_y, pit_width):
        pin_space = pit_width // 10  # - pin_width
        new_x_values = [center_x,
                    center_x - pin_space,
                    center_x + pin_space,
                    center_x - pin_space * 2,
                    center_x,
                    center_x + pin_space * 2,
                    center_x - pin_space * 3,
                    center_x - pin_space,
                    center_x + pin_space,
                    center_x + pin_space * 3]

        for i in range(9, -1, -1):
            self.all_pins[i].rect.center = (new_x_values[i], center_y)
            self.all_pins[i].reset_rect.center = self.all_pins[i].rect.center
            self.all_pins[i].pin_range_low = self.all_pins[i].rect.centerx - self.all_pins[i].pin_width / 7
            self.all_pins[i].pin_range_high = self.all_pins[i].rect.centerx + self.all_pins[i].pin_width / 7 + 20

    def set_x_values(self, new_x_values):
        for i in range(9, -1, -1):
            self.all_pins[i].rect.x = new_x_values[i]
            self.all_pins[i].reset_rect.center = self.all_pins[i].rect.center

    def set_y_value(self, new_y_value):
        for pin in self.all_pins:
            pin.rect.y = new_y_value
            pin.reset_rect.center = pin.rect.center

    def display(self, surface, ball_x, ball_y):
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN]:
            self.reset_all()
        else:
            for pin in self.all_pins:
                # check if ball hit pin
                if not pin.down and pin.test_if_ball_collusion(ball_x, ball_y):
                    ball_crash_sound = pygame.mixer.Sound("ball_pin_collusion.mp3")
                    if self.sound_effect:
                        pygame.mixer.Sound.play(ball_crash_sound)
                    self.pins_down += 1

                    # strike possibility
                    if self.pins_down == 1 and (pin.number == 2 or pin.number == 3):
                        probability_of_strike = np.random.randint(1, 100)
                        # probability_of_strike = 100 # to check if strike is working properly
                        if probability_of_strike > 85 and pin.number == 2:
                            self.strike(True, False)
                        elif probability_of_strike > 90 and pin.number == 3:
                            self.strike(True, False)

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

                        # make active if not down, to avoid double count
                        if not self.all_pins[now_active-1].down:
                            self.all_pins[now_active-1].active = True

                    # save number that will be hit
                    collateral_num = pin.test_for_collateral()
                    # while there is a collateral pin
                    while collateral_num != 0 and not self.all_pins[collateral_num-1].down:
                        self.pins_down += 1
                        logging.debug("pins down: " + str(self.pins_down))
                        self.all_pins[collateral_num-1].knock_down(pin.rect.centerx)
                        collateral_num = pin.test_for_collateral()
                pin.display(surface)
                    # to check collusion
                # if pin.active:
                    # pin_rect = pin.image.get_rect()
                    # pin_rect = pygame.Rect(pin.rect.centerx,pin.rect.centery,(pin.pin_range_high-pin.pin_range_low), pin.pin_height/2)
                    # pin_rect.center = (pin.rect.centerx,pin.rect.centery)
                    # pygame.draw.rect(surface, (250,250,0), pin_rect)

    def reset_all(self):
        self.pins_down = 0
        for pin in self.all_pins:
            # pygame.time.wait(20)
            pin.reset()

    def strike(self, left, right):
        for pin in self.all_pins:
            pin.down = True
            pin.left = left
            pin.right = right
        self.pins_down = 10

    def toggle_sound(self):
        self.sound_effect = not self.sound_effect

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
