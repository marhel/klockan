import pygame
from pygame.locals import *
import time
from math import sin, cos, radians

GREEN = (0x4C, 0xE0, 0xB3)
BLUE = (0x56, 0xCB, 0xF9)
YELLOW = (0xF4, 0xE7, 0x6E)
PINK = (0xEF, 0x76, 0x7A)
BLACK = (0x29, 0x2C, 0x33)
GRAY = (0x5C, 0x64, 0x73)
TRANSPARENT = (0, 0, 0, 0)

class Klocka(pygame.Surface):
    now = time.localtime()
    size = (400, 400)

    def __init__(self):
        pygame.Surface.__init__(self, self.size)
        print("Klocka init")
        self.hand_color = (255, 200, 0)
        self.dots_color = GREEN
        self.background_color = GRAY
        self.background_image = None #pygame.image.load("back.png").convert()
        self.pos = (0, 0)
        self.hand_length = 180
        
    def blit_on(self, surface):
        self.fill(self.background_color)
        if not self.background_image == None: self.blit(self.background_image, (0,0))
        self.blit_dots()
        self.blit_hands()
        surface.blit(self, self.pos)
    
    def blit_dots(self):
        # standard coords of 12:00:00
        x = 0
        y = self.hand_length - 10
        for i in range(1, 61):
            angle = i * 6
            point = self.screen_point(self.rotated((x,y), angle))
            spoint = self.screen_point(self.rotated((x,y * 0.9), angle))
            pygame.draw.line(self, BLACK, spoint, point, 4)
            self.set_at(point, self.dots_color)
        for i in range(1, 13):
            angle = i * 30
            point = self.screen_point(self.rotated((x,y), angle))
            spoint = self.screen_point(self.rotated((x,y * 1.1), angle))
            pygame.draw.line(self, self.dots_color, spoint, point, 4)
    
    def blit_hands(self):
        # standard coords of 12:00:00
        x = 0
        y = self.hand_length
        
        second = self.now.tm_sec
        minute = self.now.tm_min + second / 60.
        hour = self.now.tm_hour + minute / 60.
        
        if hour > 12: hour = hour - 12
        hour_angle = hour * 30
        minute_angle = minute * 6
        second_angle = second * 6

        self.blit_hand(15, y * 0.6, BLUE, hour_angle)
        self.blit_hand(7, y * 0.8, PINK, minute_angle)
        self.blit_hand(3, y * 1.0, YELLOW, second_angle)

        pygame.draw.circle(self, BLACK, self.screen_point((0, 0)), 20)

    def blit_hand(self, w, l, col, rot):
        hand_img = pygame.Surface((w , 2 * l))
        hand_img.set_colorkey(TRANSPARENT)
        pygame.draw.rect(hand_img, col, (0,0, w, l))
        rot_hour = pygame.transform.rotate(hand_img, - rot)
        hand_rect = rot_hour.get_rect()
        hand_rect.center = self.screen_point((0, 0))
        self.blit(rot_hour, hand_rect)
        
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


last_sec = -1
display_width = 400
display_height = 600
display_time = time.time()
display_offset = 0
display_delta = 1

pygame.init()
pygame.font.init()
pygame.key.set_repeat(500, 50)
# available = pygame.font.get_fonts()
# print(available)
font = pygame.font.SysFont("menlottc", 36)
game_display = pygame.display.set_mode((display_width, display_height), 0, 32)
game_display.fill(GRAY)
pygame.display.set_caption('Klockan')
pygame.display.update()
klockan = Klocka()
digital = font.render("00:00", True, GREEN)

def event_handler():
    global display_delta, display_offset
    mul = 1
    for event in pygame.event.get():
        if event.type == QUIT or (
             event.type == KEYDOWN and (
              event.key == K_ESCAPE or
              event.key == K_q
             )):
            pygame.quit()
            quit()
        if event.type == KEYDOWN and event.key == K_UP:
            display_delta += 1
        if event.type == KEYDOWN and event.key == K_DOWN:
            display_delta -= 1
        if event.type == pygame.KEYDOWN:
            if event.mod == pygame.KMOD_NONE:
                mul = 1
            if event.mod & pygame.KMOD_SHIFT:
                mul *= 60
            if event.mod & pygame.KMOD_CTRL:
                mul *= 60
        if event.type == KEYDOWN and event.key == K_LEFT:
            display_delta = 0
            display_offset -= mul
        if event.type == KEYDOWN and event.key == K_RIGHT:
            display_delta = 0
            display_offset += mul

def draw_digital():
    pygame.draw.rect(game_display, GRAY, (0, 400, display_width, 200))
    digital = [
        font.render("%02d" % klockan.now.tm_hour, True, BLUE),
        font.render(":", True, BLACK),
        font.render("%02d" % klockan.now.tm_min, True, PINK),
        font.render(":", True, BLACK),
        font.render("%02d" % klockan.now.tm_sec, True, YELLOW)]
    offs = 400 // 2 - 176 // 2
    for dig in digital:
        game_display.blit(dig, (offs, 450 - dig.get_height() // 2))
        offs += dig.get_width()

def draw_clock():
    klockan.blit_on(game_display)

def newSecond():
    global last_sec, digital
    result = klockan.now.tm_hour * 60 * 60 + klockan.now.tm_min * 60 + klockan.now.tm_sec != last_sec
    last_sec = klockan.now.tm_hour * 60 * 60 + klockan.now.tm_min * 60 + klockan.now.tm_sec
    return result

while True:
    event_handler()
    klockan.now = time.localtime(display_time)
    display_offset += display_delta
    display_time = time.time() + display_offset
    if newSecond():
        draw_clock()
        draw_digital()
    # game_display.fill((100,0,0))
    #pygame.draw.rect(game_display, (100,0,100), Rect(10, 10, 20, 20))
    #pygame.draw.polygon(game_display, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))
    # draw the window onto the screen
    pygame.display.update()
