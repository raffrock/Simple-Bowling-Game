# Ball class intended to have functions
# for movement, rolls, and collusion

import pygame

class Ball(pygame.sprite.Sprite):
    # initializes variables for roll speed and move speed

    # if rolling
    if_roll = False

    def __init__(self, floor_x, floor_y, limit_y, color):
        # calls sprite constructor
        pygame.sprite.Sprite.__init__(self)

        # save color for animation
        self.color = color

        if color == "Blue":
            self.icon = pygame.image.load('/Users/rchetata/PycharmProjects/Simple_Bowling_Game/ball_icon_colors/ball_icon_blue.png').convert_alpha()
        elif color == "Red":
            self.icon = pygame.image.load('/Users/rchetata/PycharmProjects/Simple_Bowling_Game/ball_icon_colors/ball_icon_red.png').convert_alpha()
        else: # color is purple
            self.icon = pygame.image.load('/Users/rchetata/PycharmProjects/Simple_Bowling_Game/ball_icon_colors/ball_icon_purple.png').convert_alpha()
        self.icon = pygame.transform.rotozoom(self.icon, 0, .5)

        # img rect for positioning and collusion
        self.rect = self.icon.get_rect()
        self.rect.center = (floor_x / 2 + 50, floor_y - self.icon.get_height() * .2)

        # variables for reset
        self.reset_pos = floor_y - self.icon.get_height()*.2
        self.limit = limit_y

        # speeds
        self.roll_speed = 0
        self.move_speed = 0

        self.turn_counter = 1

        self.roll_count = 0

        self.restart = False
        self.visible = True
        self.visible_countdown = 10

    def purple_animation(self, turn_counter):
        frames_numbers = ["zero", "one","two","three","four","five","six","seven","eigth","nine","ten","eleven","twele","thriteen","fourteen","fifteen"]
        path = "/Users/rchetata/PycharmProjects/Simple_Bowling_Game/purple_ball_animation/ball_icon_purple_"

        if turn_counter == 1:
            path += frames_numbers[1]
        elif turn_counter == 2:
            path += frames_numbers[2]
        elif turn_counter == 3:
            path += frames_numbers[3]
        elif turn_counter == 4:
            path += frames_numbers[4]
        elif turn_counter == 5:
            path += frames_numbers[5]
        elif turn_counter == 6:
            path += frames_numbers[6]
        elif turn_counter == 7:
            path += frames_numbers[7]
        elif turn_counter == 8:
            path += frames_numbers[8]
        elif turn_counter == 9:
            path += frames_numbers[9]
        elif turn_counter == 10:
            path += frames_numbers[10]
        elif turn_counter == 11:
            path += frames_numbers[11]
        elif turn_counter == 12:
            path += frames_numbers[12]
        elif turn_counter == 13:
            path += frames_numbers[13]
        elif turn_counter == 14:
            path += frames_numbers[14]
        elif turn_counter == 15:
            path += frames_numbers[15]
        else:
            path += frames_numbers[1]

        # update icon to be next frame
        path += ".png"
        self.icon = pygame.image.load(path).convert_alpha()
        self.icon = pygame.transform.rotozoom(self.icon, 0, .5)

    def update_x_y(self, x, y):
        # self.rect.x = x / 2
        # self.rect.y = y - self.icon.get_height()*.8
        self.rect.center = (x / 2 + 50, y - self.icon.get_height() * .2)
        self.reset_pos = y - self.icon.get_height() * .2

    # sets roll speed and move speed outside of constructor
    def set_speed(self, r_speed, m_speed):
        self.roll_speed = r_speed
        self.move_speed = m_speed

    def set_limit(self, new_limit):
        self.limit = new_limit

# rolls ball by para roll_speed (usually 10), and animates roll if purple
    def roll(self):
        self.rect.centery -= self.roll_speed

        if self.turn_counter > 15:
            self.turn_counter = 0

        self.turn_counter += 1

        # add animation for purple ball
        if self.color == "purple":
            self.purple_animation(self.turn_counter)

        # reset to shooting position when collusion
        if self.rect.centery < self.limit:
            self.restart = True
            self.if_roll = False
            self.visible = False
            self.rect.centery = self.reset_pos
            if self.color == "purple":
                self.purple_animation(1)

    # move function
    def move(self):
        key = pygame.key.get_pressed()
        self.restart = False
        if True in key:
            self.visible = True
        if not self.if_roll:
            if key[pygame.K_LEFT]:
                self.rect.centerx -= self.move_speed
            if key[pygame.K_RIGHT]:
                self.rect.centerx += self.move_speed
            if key[pygame.K_UP]:
                self.if_roll = True
                self.roll_count += 1
                if self.roll_count > 2:
                    self.roll_count = 1
                # reset
        # self.ball_rect = self.icon.get_rect()
        # self.ball_rect = pygame.Rect(self.x, self.y, 20, 20)

    def get_if_roll(self):
        return self.if_roll

    def display(self, surface):
        # ball_rect = pygame.Rect(0, 0, 40, 20)
        # ball_rect.center = (self.rect.centerx, self.rect.centery)
        # pygame.draw.rect(surface, (0,250,250), self.rect)
        # if self.restart:
            # pygame.time.wait(130)
        if self.visible or self.visible_countdown <= 0:
            self.visible_countdown = 20
            self.visible = True
            surface.blit(self.icon, self.rect)
        if not self.visible:
            self.visible_countdown -= 1
        # pygame.draw.rect(surface, (0, 0, 250), ball_rect)

