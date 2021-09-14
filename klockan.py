import pygame
from pygame.locals import *
import time

from Klocka import Klocka
from färger import GREEN, BLUE, YELLOW, PINK, BLACK, GRAY

last_sec = -1
display_width = 500
display_height = 800
display_time = time.time()
display_offset = 0
display_delta = 0

pygame.init()
pygame.font.init()
pygame.key.set_repeat(500, 50)
# available = pygame.font.get_fonts()
# print(available)
font = pygame.font.SysFont("menlottc", 128)
font2 = pygame.font.SysFont("menlottc", 24)
font3 = pygame.font.SysFont("menlottc", 48)
game_display = pygame.display.set_mode((display_width, display_height), 0, 32)
game_display.fill(GRAY)
pygame.display.set_caption('Klockan')
pygame.display.update()
klockan = Klocka()
digital = []
clock_text = True
clock_digital = True
clock_analog = True
clock_now = True


def event_handler(klocka):
    global display_delta, display_offset, display_time, clock_text, clock_digital, clock_analog, clock_now
    mul = 1
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            quit()
        if event.type == KEYDOWN and event.key == K_UP:
            display_delta += 1
            klocka.running = False
        if event.type == KEYDOWN and event.key == K_DOWN:
            display_delta -= 1
            klocka.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == K_3 or event.key == K_e:
                mul = 1
            if event.key == K_2 or event.key == K_w:
                if klocka.with_seconds:
                    mul = 73
                else:
                    mul = 60
            if event.key == K_1 or event.key == K_q:
                if klocka.with_seconds:
                    mul = 73 * 5
                else:
                    mul = 60 * 5
            if event.mod & pygame.KMOD_SHIFT:
                mul *= 3
            if event.mod & pygame.KMOD_CTRL:
                mul *= 4
        if event.type == KEYDOWN and not event.mod and event.key == K_m:
            klocka.numbered_minutes = not klocka.numbered_minutes
        if event.type == KEYDOWN and not event.mod and event.key == K_h:
            klocka.numbered_hours = not klocka.numbered_hours
        if event.type == KEYDOWN and event.mod & pygame.KMOD_SHIFT and event.key == K_h:
            klocka.tick_hours = not klocka.tick_hours
        if event.type == KEYDOWN and event.mod & pygame.KMOD_CTRL and event.key == K_m:
            klocka.floating_minutes = not klocka.floating_minutes
        if event.type == KEYDOWN and event.mod & pygame.KMOD_SHIFT and event.key == K_m:
            klocka.tick_minutes = not klocka.tick_minutes
        if event.type == KEYDOWN and event.mod & pygame.KMOD_CTRL and event.key == K_h:
            klocka.floating_hours = not klocka.floating_hours
        if event.type == KEYDOWN and event.key == K_s:
            klocka.with_seconds = not klocka.with_seconds
        if event.type == KEYDOWN and event.key == K_t:
            clock_text = not clock_text
        if event.type == KEYDOWN and event.key == K_d:
            clock_digital = not clock_digital
        if event.type == KEYDOWN and event.key == K_a:
            clock_analog = not clock_analog
        if event.type == KEYDOWN and event.key == K_p:
            klocka.pseudo_24h = not klocka.pseudo_24h
        if event.type == KEYDOWN and (event.key == K_n or event.key == K_RETURN):
            display_offset = 0
            display_time = time.time()
        if event.type == KEYDOWN and event.key == K_r:
            display_delta = 0
            if not klocka.running:
                display_offset = display_time - time.time()
            else:
                display_offset = 0
            klocka.running = not klocka.running
        if event.type == KEYDOWN and (event.key == K_LEFT or event.key == K_3 or event.key == K_2 or event.key == K_1):
            display_delta = 0
            display_offset += mul
        if event.type == KEYDOWN and (event.key == K_RIGHT or event.key == K_e or event.key == K_w or event.key == K_q):
            display_delta = 0
            display_offset -= mul


def draw_state():
    top = display_width+150

    state = [[klockan.numbered_minutes, 'm'],
             [klockan.numbered_hours, 'h'],
             [klockan.tick_minutes, 'M'],
             [klockan.tick_hours, 'H'],
             [klockan.floating_minutes, '^M'],
             [klockan.floating_hours, '^H'],
             [klockan.with_seconds, 's'],
             [klockan.pseudo_24h, 'p'],
             [klockan.running, 'r'],
             [clock_now, 'n'],
             [clock_text, 't'],
             [clock_digital, 'd'],
             [clock_analog, 'a']]
    text3 = [font2.render(char, True, YELLOW if toggle else BLACK) for toggle, char in state]

    t3w = 0
    for dig in text3:
        t3w += dig.get_width()

    offs = game_display.get_width() // 2
    start = offs - t3w // 2
    for dig in text3:
        game_display.blit(dig, (offs - t3w // 2, top + 90 - dig.get_height() // 2))
        offs += dig.get_width()
    game_display.blit(font2.render("hastighet: " + (str(display_delta) if display_delta else "verklig" if klockan.running else "stillastående"), True, YELLOW if display_delta else BLUE if klockan.running else BLACK), (start, top + 110 - dig.get_height() // 2))
    game_display.blit(font2.render("1/Q 2/W 3/E + pilarna, med shift/ctrl", True, PINK), (start, top + 130 - dig.get_height() // 2))


def draw_text():
    top = display_width+150
    pygame.draw.rect(game_display, GRAY, (0, top, display_width, 200))
    if not clock_text: return
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
        font3.render(precision[minut % 5], True, PINK),
        font3.render(minuter[(minut + 2) // 5], True, PINK),
        font3.render(namn[timme + (minut + 35 + 2) // 60], True, BLUE)
    ]
    text2 = [
        font3.render("     på ", True, YELLOW),
        font3.render(period[klockan.now.tm_hour // 3], True, YELLOW)
    ]

    offs = 70
    for dig in text1:
        game_display.blit(dig, (offs, top - dig.get_height() // 2))
        offs += dig.get_width()

    offs = 70
    for dig in text2:
        game_display.blit(dig, (offs, top + 30 - dig.get_height() // 2))
        offs += dig.get_width()


def draw_digital():
    top = display_width + 20
    pygame.draw.rect(game_display, GRAY, (0, top, display_width, 200))
    if not clock_digital: return
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

    offs = display_width // 2 - tw // 2
    for dig in digital:
        game_display.blit(dig, (offs, top))
        offs += dig.get_width()


def draw_clock():
    if not clock_analog:
        top = display_width
        pygame.draw.rect(game_display, GRAY, (0, 0, display_width, top))
        return
    klockan.blit_on(game_display)


def is_new_state():
    global last_sec, digital, last_state
    state = [klockan.floating_minutes, klockan.floating_hours, klockan.tick_minutes, klockan.tick_hours, klockan.numbered_minutes, klockan.numbered_hours, klockan.with_seconds, klockan.pseudo_24h, klockan.running, clock_text, clock_digital, clock_analog, clock_now, display_delta]
    sec = klockan.now.tm_hour * 60 * 60 + klockan.now.tm_min * 60 + klockan.now.tm_sec
    result = sec != last_sec or state != last_state
    last_sec = sec
    last_state = state
    return result


while True:
    event_handler(klockan)
    klockan.now = time.localtime(display_time)
    clock_now = display_offset == 0 and klockan.running

    display_offset += display_delta / (60 if klockan.with_seconds else 1)
    if klockan.running:
        display_time = time.time() + display_offset
    else:
        display_time += display_offset
        display_offset = 0
    if is_new_state():
        draw_clock()
        draw_digital()
        draw_text()
        draw_state()
    # game_display.fill((100,0,0))
    # pygame.draw.rect(game_display, (100,0,100), Rect(10, 10, 20, 20))
    # pygame.draw.polygon(game_display, GREEN, ((146, 0), (291, 106), (236, 277), (56, 277), (0, 106)))
    # draw the window onto the screen
    pygame.display.update()
