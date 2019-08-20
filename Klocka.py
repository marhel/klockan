import time
from math import radians, cos, sin

import pygame
from pygame.locals import *

from färger import GREEN, BLUE, YELLOW, PINK, PINK_T, BLACK, GRAY, TRANSPARENT


class Klocka(pygame.Surface):
    now = time.localtime()
    running = False
    size = (500, 500)
    floating_minutes = False
    floating_hours = True
    with_seconds = False
    pygame.font.init()
    font = pygame.font.SysFont("menlottc", 36)
    font2 = pygame.font.SysFont("menlottc", 18)

    def __init__(self):
        pygame.Surface.__init__(self, self.size)
        print("Klocka init")
        self.hand_color = (255, 200, 0)
        self.background_color = GRAY
        self.pos = (0, 0)
        self.hand_length = 160

    def blit_on(self, surface):
        self.fill(self.background_color)

        second = self.now.tm_sec
        minute = self.now.tm_min
        if self.floating_minutes:
            minute += second / 60.
        hour = self.now.tm_hour
        if self.floating_hours:
            hour += minute / 60.
        day = hour / 24.

        self.blit_hands(hour, minute)
        self.blit_dots()
        self.blit_second_hand(second)
        self.blit_day(day)

        pygame.draw.circle(self, BLACK, self.screen_point((0, 0)), 20)

        surface.blit(self, self.pos)

    def blit_dots(self):
        # standard coords of 12:00:00
        x = 0
        y = self.hand_length * 0.9
        for i in range(1, 13):
            angle = i * 30
            point = self.screen_point(self.rotated((x, y), angle))
            spoint = self.screen_point(self.rotated((x, y * 1.1), angle))
            pygame.draw.line(self, BLUE, spoint, point, 4)
        for i in range(1, 61):
            angle = i * 6
            point = self.screen_point(self.rotated((x, y), angle))
            spoint = self.screen_point(self.rotated((x, y * 0.9), angle))
            pygame.draw.line(self, PINK, spoint, point, 4)
        for i in range(1, 13):
            angle = i * 30
            point = self.screen_point(self.rotated((x, y * 1.3), angle))
            num = self.font.render(str(i), True, BLUE)
            num_rect = num.get_rect()
            num_rect.center = point
            self.blit(num, num_rect)
        for i in range(5, 61, 5):
            angle = i * 6
            point = self.screen_point(self.rotated((x, y / 1.3), angle))
            num = self.font2.render(str(i), True, PINK_T)
            num_rect = num.get_rect()
            num_rect.center = point
            self.blit(num, num_rect, special_flags=BLEND_ADD)

    def blit_hands(self, hour, minute):
        # standard coords of 12:00:00
        x = 0
        y = self.hand_length

        if hour > 12: hour = hour - 12
        hour_angle = hour * 30
        minute_angle = minute * 6

        self.blit_hand(21, y * 0.6, BLUE, hour_angle)
        self.blit_hand(13, y * 0.8, PINK, minute_angle)

    def blit_second_hand(self, second):
        # standard coords of 12:00:00
        x = 0
        y = self.hand_length

        second_angle = second * 6

        if self.with_seconds: self.blit_hand(5, y * 1.0, YELLOW, second_angle)

    def blit_hand(self, w, l, col, rot):
        hand_img = pygame.Surface((w, 2 * l))
        hand_img.set_colorkey(TRANSPARENT)
        pygame.draw.rect(hand_img, col, (0, 0, w, l))
        rot_hour = pygame.transform.rotate(hand_img, - rot)
        hand_rect = rot_hour.get_rect()
        hand_rect.center = self.screen_point((0, 0))
        self.blit(rot_hour, hand_rect)

    def blit_day(self, day):
        x = 0
        y = self.hand_length
        dawn = 30
        dawn_end = 40
        dusk = 90
        dusk_end = 100

        def fade(step, number_of_steps, base_color, next_color):
            return [x + (((y - x) / number_of_steps) * step) for x, y in
                    zip(pygame.color.Color(base_color), pygame.color.Color(next_color))]

        for i in range(0, int(120 * day) + 1):
            angle_start = i * 6
            angle_end = (i + 1) * 6
            point = self.screen_point(self.rotated((x, y * (1.4 + 0.15 * i / 120.)), angle_start))
            spoint = self.screen_point(self.rotated((x, y * (1.4 + 0.15 * i / 120.)), angle_end))
            daycol = BLACK
            if dawn < i <= dawn_end:
                daycol = fade(i - dawn, dawn_end - dawn, BLACK, YELLOW)
            if i > dawn_end:
                daycol = YELLOW
            if dusk < i <= dusk_end:
                daycol = fade(i - dusk, dusk_end - dusk, YELLOW, BLACK)
            if i > dusk_end:
                daycol = BLACK
            pygame.draw.line(self, daycol, spoint, point, 9)

    def rotated(self, point, angle):
        x, y = point
        angle = radians(-angle)
        rotated_x = int(x * cos(angle) - y * sin(angle))
        rotated_y = int(x * sin(angle) + y * cos(angle))
        return (rotated_x, rotated_y)

    def screen_point(self, point):
        x, y = point
        x_p = x + self.size[0] / 2
        y_p = -y + self.size[1] / 2
        return (int(x_p), int(y_p))
