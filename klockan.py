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
    running = True
    size = (400, 400)
    floating_minutes = False
    floating_hours = True
    with_seconds = True

    def __init__(self):
        pygame.Surface.__init__(self, self.size)
        print("Klocka init")
        self.hand_color = (255, 200, 0)
        self.dots_color = GREEN
        self.background_color = GRAY
        self.background_image = None #pygame.image.load("back.png").convert()
        self.pos = (0, 0)
        self.hand_length = 160

    def blit_on(self, surface):
        self.fill(self.background_color)
        if not self.background_image == None: self.blit(self.background_image, (0,0))
        self.blit_dots()
        self.blit_hands()
        surface.blit(self, self.pos)

    def blit_dots(self):
        # standard coords of 12:00:00
        x = 0
        y = self.hand_length * 0.9
        for i in range(1, 61):
            angle = i * 6
            point = self.screen_point(self.rotated((x,y), angle))
            spoint = self.screen_point(self.rotated((x,y * 0.9), angle))
            pygame.draw.line(self, BLACK, spoint, point, 4)
        for i in range(1, 13):
            angle = i * 30
            point = self.screen_point(self.rotated((x,y), angle))
            spoint = self.screen_point(self.rotated((x,y * 1.1), angle))
            pygame.draw.line(self, BLUE, spoint, point, 4)

    def blit_hands(self):
        # standard coords of 12:00:00
        x = 0
        y = self.hand_length

        second = self.now.tm_sec
        minute = self.now.tm_min
        if self.floating_minutes:
            minute += second / 60.
        hour = self.now.tm_hour
        if self.floating_hours:
            hour += minute / 60.
        day = hour / 24.

        if hour > 12: hour = hour - 12
        hour_angle = hour * 30
        minute_angle = minute * 6
        second_angle = second * 6

        self.blit_hand(21, y * 0.6, BLUE, hour_angle)
        self.blit_hand(13, y * 0.8, PINK, minute_angle)
        if self.with_seconds: self.blit_hand(5, y * 1.0, YELLOW, second_angle)

        DAWN = 30
        DAWN_END = 40
        DUSK = 90
        DUSK_END = 100
        def fade(step, number_of_steps, base_color, next_color):
            return [x + (((y-x)/number_of_steps)*step) for x, y in zip(pygame.color.Color(base_color), pygame.color.Color(next_color))]

        for i in range(0, int(120 * day)+1):
            angle_start = i * 6
            angle_end = (i+1) * 6
            point = self.screen_point(self.rotated((x,y*(1.05+0.15*i/120.)), angle_start))
            spoint = self.screen_point(self.rotated((x,y*(1.05+0.15*i/120.)), angle_end))
            daycol = BLACK
            if i > DAWN and i <= DAWN_END:
                daycol = fade(i-DAWN, DAWN_END-DAWN, BLACK, YELLOW)
            if i > DAWN_END:
                daycol = YELLOW
            if i > DUSK and i <= DUSK_END:
                daycol = fade(i-DUSK, DUSK_END-DUSK, YELLOW, BLACK)
            if i > DUSK_END:
                daycol = BLACK
            pygame.draw.line(self, daycol, spoint, point, 9)

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
display_delta = 0

pygame.init()
pygame.font.init()
pygame.key.set_repeat(500, 50)
# available = pygame.font.get_fonts()
# print(available)
font = pygame.font.SysFont("menlottc", 36)
font2 = pygame.font.SysFont("menlottc", 24)
game_display = pygame.display.set_mode((display_width, display_height), 0, 32)
game_display.fill(GRAY)
pygame.display.set_caption('Klockan')
pygame.display.update()
klockan = Klocka()
digital = font.render("00:00", True, GREEN)

def event_handler(klocka):
    global display_delta, display_offset, display_time
    mul = 1
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            quit()
        if event.type == KEYDOWN and event.key == K_UP:
            display_delta += 1
        if event.type == KEYDOWN and event.key == K_DOWN:
            display_delta -= 1
        if event.type == pygame.KEYDOWN:
            if event.key == K_d or event.key == K_e:
                mul = 1
            if event.key == K_s or event.key == K_w:
                if klocka.with_seconds:
                    mul = 73
                else:
                    mul = 60
            if event.key == K_a or event.key == K_q:
                if klocka.with_seconds:
                    mul = 73 * 12
                else:
                    mul = 60 * 12
            if event.mod & pygame.KMOD_SHIFT:
                mul *= 3
            if event.mod & pygame.KMOD_CTRL:
                mul *= 5
        if event.type == KEYDOWN and event.key == K_m:
            klocka.floating_minutes = not klocka.floating_minutes
        if event.type == KEYDOWN and event.key == K_h:
            klocka.floating_hours = not klocka.floating_hours
        if event.type == KEYDOWN and event.key == K_i:
            klocka.with_seconds = not klocka.with_seconds
        if event.type == KEYDOWN and event.key == K_n:
            display_offset = 0
            display_time = time.time()
        if event.type == KEYDOWN and event.key == K_r:
            if not klocka.running:
                display_offset = display_time - time.time()
            else:
                display_offset = 0
            klocka.running = not klocka.running
        if event.type == KEYDOWN and (event.key == K_LEFT or event.key == K_d or event.key == K_s or event.key == K_a):
            display_delta = 0
            display_offset -= mul
        if event.type == KEYDOWN and (event.key == K_RIGHT or event.key == K_e or event.key == K_w or event.key == K_q):
            display_delta = 0
            display_offset += mul

def draw_text():
    pygame.draw.rect(game_display, GRAY, (0, 550, display_width, 200))
    timme = klockan.now.tm_hour
    minut = klockan.now.tm_min
    if timme > 12: timme -= 12
    namn = ["tolv", "ett", "två", "tre", "fyra", "fem", "sex", "sju", "åtta", "nio", "tio", "elva", "tolv", "ett"]
    period = ["natten", "tidiga morgonen", "morgonen", "förmiddagen", "dagen", "eftermiddagen", "kvällen", "sena kvällen", "natten"]
    minuter = ["", "fem över ", "tio över ", "kvart över ", "tjugo över ", "fem i halv ", "halv ", "fem över halv ", "tjugo i ", "kvart i ", "tio i ", "fem i ", ""]
    precision = ["     ", "ung. ", "ung. ", "ung. ", "ung. "]
    text1 = [
        font2.render(precision[minut % 5], True, PINK),
        font2.render(minuter[(minut+2)//5], True, PINK),
        font2.render(namn[timme + (minut+35+2)//60], True, BLUE)
    ]
    text2 = [
        font2.render("     på ", True, BLACK),
        font2.render(period[klockan.now.tm_hour // 3], True, BLACK)
    ]
    t1w = 0
    for dig in text1:
        t1w += dig.get_width()

    offs = 50
    for dig in text1:
        game_display.blit(dig, (offs, 550 - dig.get_height() // 2))
        offs += dig.get_width()

    t2w = 0
    for dig in text2:
        t2w += dig.get_width()

    offs = 50
    for dig in text2:
        game_display.blit(dig, (offs, 580 - dig.get_height() // 2))
        offs += dig.get_width()

def draw_digital():
    pygame.draw.rect(game_display, GRAY, (0, 400, display_width, 200))
    digital = [
        font.render("%02d" % klockan.now.tm_hour, True, BLUE),
        font.render(":", True, BLACK),
        font.render("%02d" % klockan.now.tm_min, True, PINK)]

    if klockan.with_seconds:
        digital += [
            font.render(":", True, BLACK),
            font.render("%02d" % klockan.now.tm_sec, True, YELLOW)]

    tw = 0
    for dig in digital:
        tw += dig.get_width()

    offs = 400 // 2 - tw // 2
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
    event_handler(klockan)
    klockan.now = time.localtime(display_time)
    display_offset += display_delta
    if klockan.running:
        display_time = time.time() + display_offset
    else:
        display_time += display_offset
        display_offset = 0
    if newSecond():
        draw_clock()
        draw_digital()
        draw_text()
    # game_display.fill((100,0,0))
    #pygame.draw.rect(game_display, (100,0,100), Rect(10, 10, 20, 20))
    #pygame.draw.polygon(game_display, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))
    # draw the window onto the screen
    pygame.display.update()
