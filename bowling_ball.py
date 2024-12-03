# Ball class intended to have functions
# for movement, rolls, and collusion

import pygame

# # controls to move ball
# if key_down == pygame.K_RIGHT:
#     ball_rect_x += 5
# if key_down == pygame.K_LEFT:
#     ball_rect_x -= 5
# if key_down == pygame.K_UP:
#     roll = True
#
# if roll and ball_rect_y > 400:
#     ball_rect_y -= 10
# elif ball_rect_y >= 400:
#     ball_rect_y = 750
#     roll = False
#
# ball_rect_x = 300
# ball_rect_y = 750
# roll = False

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

        # position ball
        # self.rect = self.icon.get_rect()
        # self.rect.x = floor_x / 2
        # self.rect.y = floor_y

        self.x = floor_x / 2
        self.y = floor_y

        # variables for reset
        self.reset_pos = floor_y
        self.limit = limit_y

        # speeds
        self.roll_speed = 0
        self.move_speed = 0

        self.turn_counter = 1

        self.roll_count = 0

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

    # sets roll speed and move speed outside of constructor
    def set_speed(self, r_speed, m_speed):
        self.roll_speed = r_speed
        self.move_speed = m_speed

    def set_limit(self, new_limit):
        self.limit = new_limit

# rolls ball by para roll_speed (usually 10), and animates roll if purple
    def roll(self):
        self.y -= self.roll_speed

        if self.turn_counter > 15:
            self.turn_counter = 0

        self.turn_counter += 1

        # add animation for purple ball
        if self.color == "purple":
            self.purple_animation(self.turn_counter)

        # reset to shooting position when collusion
        if self.y <= self.limit:
            self.if_roll = False
            self.y = self.reset_pos
            if self.color == "purple":
                self.purple_animation(1)

    # move function
    def move(self):
        key = pygame.key.get_pressed()
        if not self.if_roll:
            if key[pygame.K_LEFT]:
                self.x -= self.move_speed
            if key[pygame.K_RIGHT]:
                self.x += self.move_speed
            if key[pygame.K_UP]:
                self.if_roll = True
                self.roll_count += 1
                # reset
                if self.roll_count > 2:
                    self.roll_count = 1
        # self.ball_rect = self.icon.get_rect()
        # self.ball_rect = pygame.Rect(self.x, self.y, 20, 20)

    def get_if_roll(self):
        return self.if_roll

    def display(self, surface):
        surface.blit(self.icon, (self.x, self.y))
        # Rect(left, top, width, height)
        ball_rect = pygame.Rect(self.x, self.y, 10, 10)
        pygame.draw.rect(surface, (250,250,250), ball_rect)

