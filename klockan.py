import pygame
from pygame.locals import *
import time
from math import sin, cos, radians

GREEN = (0, 180, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

class Klocka(pygame.Surface):
    now = time.localtime()
    size = (400, 400)

    def __init__(self):
        pygame.Surface.__init__(self, self.size)
        print("Klocka init")
        self.hand_color = (255, 200, 0)
        self.dots_color = (255, 100, 0)
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
        hour_point = self.screen_point(self.rotated((x, y * 0.6), hour_angle))
        pygame.draw.line(self, BLUE, self.screen_point((0, 0)), hour_point, 15)
            
        minute_angle = minute * 6
        minute_point = self.screen_point(self.rotated((x, y * 0.8), minute_angle))
        pygame.draw.line(self, GREEN, self.screen_point((0, 0)), minute_point, 7)
        
        second_angle = second * 6
        second_point = self.screen_point(self.rotated((x, y), second_angle))
        pygame.draw.line(self, YELLOW, self.screen_point((0, 0)), second_point, 3)
        
        pygame.draw.circle(self, BLACK, self.screen_point((0, 0)), 20)
        
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
display_width = 800
display_height = 600

pygame.init()
pygame.font.init()
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
    for event in pygame.event.get():
        if event.type == QUIT or (
             event.type == KEYDOWN and (
              event.key == K_ESCAPE or
              event.key == K_q
             )):
            pygame.quit()
            quit()

def draw_digital():
    pygame.draw.rect(game_display, GRAY, (0, 400, display_width, 200))
    digital = [
        font.render("%02d" % klockan.now.tm_hour, True, BLUE),
        font.render(":", True, BLACK),
        font.render("%02d" % klockan.now.tm_min, True, GREEN),
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
    result = klockan.now.tm_sec != last_sec
    last_sec = klockan.now.tm_sec
    return result

while True:
    event_handler()
    klockan.now = time.localtime()
    if newSecond():
        draw_clock()
        draw_digital()
    # game_display.fill((100,0,0))
    #pygame.draw.rect(game_display, (100,0,100), Rect(10, 10, 20, 20))
    #pygame.draw.polygon(game_display, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))
    # draw the window onto the screen
    pygame.display.update()
