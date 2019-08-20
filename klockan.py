import pygame
from pygame.locals import *
import time

from Klocka import Klocka
from färger import GREEN, BLUE, YELLOW, PINK, BLACK, GRAY

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
                    mul = 73 * 5
                else:
                    mul = 60 * 5
            if event.mod & pygame.KMOD_SHIFT:
                mul *= 3
            if event.mod & pygame.KMOD_CTRL:
                mul *= 4
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
    period = ["natten", "tidiga morgonen", "morgonen", "förmiddagen", "dagen", "eftermiddagen", "kvällen",
              "sena kvällen", "natten"]
    minuter = ["", "fem över ", "tio över ", "kvart över ", "tjugo över ", "fem i halv ", "halv ", "fem över halv ",
               "tjugo i ", "kvart i ", "tio i ", "fem i ", ""]
    precision = ["     ", "ung. ", "ung. ", "ung. ", "ung. "]
    text1 = [
        font2.render(precision[minut % 5], True, PINK),
        font2.render(minuter[(minut + 2) // 5], True, PINK),
        font2.render(namn[timme + (minut + 35 + 2) // 60], True, BLUE)
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
    # pygame.draw.rect(game_display, (100,0,100), Rect(10, 10, 20, 20))
    # pygame.draw.polygon(game_display, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))
    # draw the window onto the screen
    pygame.display.update()
