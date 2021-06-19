import numpy as np
from block import *
import random as r
import copy
import math

class Tetris:
    def __init__(self):
        self.block = np.zeros((4, 4), dtype = int)
        self.block_pos = [1, 4]
        self.board_dyna = np.zeros((22, 12), dtype = int)
        self.board_stat = np.zeros((22, 12), dtype = int)
        self.board_color = np.zeros((22, 12), dtype = int)

        self.score = 0
    
    def initialize_score(self):
        self.score = 0

    def update_score(self, add_score):
        self.score += add_score

    def start(self):
        self.generate_block()
        Tetris.initialize_board(self.board_dyna)
        Tetris.initialize_board(self.board_stat)
        Tetris.initialize_board(self.board_color)
        self.locate_block()

    @staticmethod
    def initialize_board(b):
        for i in range(22):
            b[i] = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        b[0] = [1] * 12
        b[21] = [1] * 12

    def fence_board(self, b):
        for i in b:
            i[0] = 1
            i[11] = 1
        b[0] = [1] * 12
        b[21] = [1] * 12

    def generate_block(self):
        try:
            self.block = Block(self.block.next)
        except:
            self.block = Block(r.randrange(7))
        self.block_pos = [1, 4]
        
    def next_block(self):
        self.board_color += copy.deepcopy((self.board_dyna - self.board_stat) * (self.block.num + 1))
        self.board_stat = copy.deepcopy(self.board_dyna)
        self.generate_block()
        self.update_score(10)
        
    def locate_block(self):
        self.board_dyna = copy.deepcopy(self.board_stat)
        for i in range(4):
            for j in range(4):
                try:
                    self.board_dyna[self.block_pos[0] + i][self.block_pos[1] + j] += self.block.data[i][j]
                except:
                    continue

    def block_offset(self, hori, vert, rot):
        temp_board = copy.deepcopy(self.board_stat)
        block_rot = np.zeros((4, 4), dtype = int)
        self.fence_board(temp_board)

        for i in range(4):
            for j in range(4):
                if rot == 0: 
                    block_rot[i][j] = self.block.data[i][j]
                elif rot == 1:
                    block_rot[j][3 - i] = self.block.data[i][j]
               
        for i in range(4):
            for j in range(4):
                try:
                    temp_board[self.block_pos[0] + vert + i][self.block_pos[1] + hori + j] += block_rot[i][j]
                        
                except:
                    continue
                
        return temp_board

    def move_block(self, hori, vert):
        if not 2 in self.block_offset(hori, vert, 0) and not self.block.warning:
            self.block_pos[0] += vert
            self.block_pos[1] += hori
            self.locate_block()

    def rotate_block(self):
        self.block.warning = False
        possible = False

        if 2 in self.block_offset(0, 0, 1):
            for i in range(1, 9):
                hori = math.ceil(i / 4) * (math.ceil(i / 2) % 2) * (-1) ** i
                vert = math.ceil(i / 4) * (math.ceil(i / 2 - 1) % 2) * (-1) ** i
                if vert < 0: continue

                if not 2 in self.block_offset(hori, vert, 1) and not 2 in self.block_offset(hori, vert + 1, 1):
                    self.move_block(hori, vert)
                    self.block.waring = True
                    possible = True
                    break
        
        if not 2 in self.block_offset(0, 0, 1) or possible:
            self.block.rotate_block()
            self.locate_block()
        
    def fix_board(self):
        self.board_stat = self.board_dyna

    def erase_line(self):
        chain = 0
        for n in range(22):
            for i in range(20, 0, -1):
                if sum(self.board_stat[i]) == 12:
                    for j in range(i - 1, 0, -1):
                        self.board_stat[j + 1] = self.board_stat[j]
                        self.board_color[j + 1] = self.board_color[j]
                    chain += 1

        if chain > 0:
            self.update_score(round(100 * 2 ** (chain - 1)))

    def vertical_fall(self):
        while not 2 in self.block_offset(0, 1, 0):
            self.move_block(0, 1)
        self.next_block()
        self.erase_line()

    def visualize_block(self, num):
        self.block.get_block(num)
        print(self.block.data)
        print()

    def preview_vertical_fall(self):
        i = 0
        while not 2 in self.block_offset(0, i, 0):
            i += 1
        return i - 1

    def visualize_board(self):
        print(self.board_dyna)

    def is_gameover(self):
        temp_board = np.zeros((22, 12), dtype = int)
        temp_board += self.board_stat

        for i in range(4):
            for j in range(4):
                try:
                    temp_board[self.block_pos[0] + i][self.block_pos[1] + j] += self.block.data[i][j]
                except:
                    continue
        
        return 2 in temp_board
