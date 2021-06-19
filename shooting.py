import pygame as pg
import sys

pg.init()

size = [300, 600]
screen = pg.display.set_mode(size)

title = 'My Game'
pg.display.set_caption(title)

clock = pg.time.Clock()
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

ss_x = round(size[0] / 2)
ss_y = round(size[1] * 0.9)
ss_w = round(size[0] * 0.1)
ss_h = round(size[1] * 0.05)

k = 0
while True:
    clock.tick(60)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
    
    key_event = pg.key.get_pressed()
    if key_event[pg.K_LEFT]:
        ss_x -= 1

    if key_event[pg.K_RIGHT]:
        ss_x += 1

    if key_event[pg.K_UP]:
        ss_y -= 1

    if key_event[pg.K_DOWN]:
        ss_y += 1

    screen.fill(BLACK)
    pg.draw.polygon(screen, BLUE, [[round(ss_x - ss_w / 2), ss_y], [round(ss_x + ss_w / 2), ss_y], [ss_x, ss_y - ss_h]])

    pg.display.flip()

    k += 1
pg.quit()

