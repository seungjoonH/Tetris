import pygame as pg
import sys
import tetris
import autoplayer

from pygame.constants import KEYDOWN

pg.init()

size = [350, 700]
screen = pg.display.set_mode(size)
t_surface = screen.convert_alpha()
over_surface = screen.convert_alpha()

title = 'Tetris'
pg.display.set_caption(title)

clock = pg.time.Clock()
BLACK = (  0,   0,   0)
GREY  = (110, 110, 110)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

board_x = round(size[0] * 0.1)
board_y = round(size[1] * 0.3)
board_w = round(size[0] * 0.8)
board_h = round(size[1] * 0.7)

cell_w = round(board_w / 10)
cell_h = round(board_h / 20)

p = autoplayer.Autoplayer()
t = p.t

s = cur_s = 0
srt = False
ending = False
end = False
my_font = pg.font.SysFont("arial", 30, True, False)
score_text = my_font.render("0", True, WHITE)

while True:
    clock.tick(60)

    # cur_block_pos = t.block_pos[:]
    
    screen.fill(BLACK)
    t_surface.fill(BLACK + (0,))
    over_surface.fill(BLACK + (0,))

    # pg.draw.rect(screen, WHITE, [board_x, board_y, board_w, board_h], 1)
    for i in range(10):
        for j in range(20):
            pg.draw.rect(screen, WHITE, [round(board_x + i * cell_w), round(board_y + j * cell_h), cell_w, cell_h], 1)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                sys.exit()

            elif not srt and not ending:
                t.start()
                srt = True
                s = 0

            if event.key == pg.K_r:
                t.start()
                t.initialize_score()
                srt = True

            # elif event.key == pg.K_SPACE and srt:
            #     t.vertical_fall()

            # elif event.key == pg.K_a and srt:
            #     t.rotate_block()
        else:
            break

    for i in range(10):
        for j in range(20):
            if t.board_color[j + 1][i + 1] > 0:
                pg.draw.rect(screen, t.block.index_to_color(t.board_color[j + 1][i + 1] - 1), [round(board_x + i * cell_w), \
                round(board_y + j * cell_h), cell_w, cell_h], 0)
    
    if srt:
        # key_event = pg.key.get_pressed()

        # if key_event[pg.K_LEFT] and s % 6 == 0:
        #     t.move_block(-1, 0)
        
        # if key_event[pg.K_RIGHT] and s % 6 == 0:
        #     t.move_block(1, 0)

        # if key_event[pg.K_DOWN] and s % 6 == 0:
        #     t.move_block(0, 1)

        if s % 5 == 0:
            p.auto_rotatemove()

        if s % 10 == 0:
            p.auto_place()
        #p.auto_place(s % 10, False)
        
        # if s % 50 == 0:
        #     t.move_block(0, 1)
        #     if cur_block_pos == t.block_pos[:]:
        #         t.next_block()
        #         t.erase_line()

        score_text = my_font.render(str(t.score), True, WHITE)

        for i in range(4):
            for j in range(4):
                if t.block.data[j][i] == 1:
                    pg.draw.rect(t_surface, t.block.color + (150,), [round(board_x + (i + t.block_pos[1] - 1) * cell_w), \
                        round(board_y + (j + t.block_pos[0] + t.preview_vertical_fall() - 1) * cell_h), cell_w, cell_h], \
                        1 - t.block.data[j][i])
                    pg.draw.rect(t_surface, t.block.color, [round(board_x + (i + t.block_pos[1] - 1) * cell_w), \
                        round(board_y + (j + t.block_pos[0] - 1) * cell_h), cell_w, cell_h], \
                        1 - t.block.data[j][i])

        for i in range(4):
            for j in range(4):
                if t.block.sample_block_data(t.block.next)[j][i] == 1:
                    pg.draw.rect(screen, t.block.index_to_color(t.block.next), \
                    [board_x + i * cell_w, round(board_y - cell_h * 5) + j * cell_h, \
                    cell_w, cell_h], 0)

        if t.is_gameover():
            ending = True
            srt = False

    elif ending:
        for i in range(10):
            for j in range((s - cur_s) // 10):
                if t.board_dyna[j + 1][i + 1] > 0:
                    pg.draw.rect(t_surface, BLACK + (100,), [board_x + i * cell_w, board_y + j * cell_h, cell_w, cell_h], 0)
                if (s - cur_s) // 10 == 21:
                    ending = False
                    end = True
                    break
    
    # gameover
    elif end:
        for i in range(10):
            for j in range(20):
                if t.board_dyna[j + 1][i + 1] > 0:
                    pg.draw.rect(t_surface, BLACK + (100,), [board_x + i * cell_w, board_y + j * cell_h, cell_w, cell_h], 0)
        
        over_size = round(size[0] * size[1] / 10000)
        over_font = pg.font.SysFont("arial", over_size, True, False)
        over_text = over_font.render("GAME OVER", True, WHITE)
        over_text.set_alpha(round((30 - abs(30 - s % 60)) * 255 / 30))
        over_rect = over_text.get_rect()
        over_rect.center = round(size[0] / 2), round(size[1] / 2)
        over_surface.blit(over_text, over_rect)


    # press random key to START
    else:
        msg_size = round(size[0] * size[1] / 12000)
        msg_font = pg.font.SysFont("arial", msg_size, True, False)
        msg_text = msg_font.render("press random key to START", True, WHITE)
        msg_text.set_alpha(round((30 - abs(30 - s % 60)) * 255 / 30))
        msg_rect = msg_text.get_rect()
        msg_rect.center = round(size[0] / 2), round(size[1] / 2)
        screen.blit(msg_text, msg_rect)

    # pg.draw.rect(screen, WHITE, [board_x, round(board_y - cell_h * 6), cell_w * 4, cell_h * 4], 1)

    score_rect = score_text.get_rect()
    score_rect.bottomright = board_x + board_w, round(board_y - size[1] * 0.1)
    score_rect.size = round(size[0] * 0.2), round(board_w * 0.1)
    screen.blit(score_text, score_rect)
    screen.blit(t_surface, (0, 0))
    screen.blit(over_surface, (0, 0))

    s += 1

    pg.display.flip()

pg.quit()

