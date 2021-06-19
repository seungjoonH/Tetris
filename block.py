import numpy as np
import random as r

BLACK    = (  0,   0,   0)
WHITE    = (255, 255, 255)
L_RED    = (255, 140, 140)
L_ORANGE = (255, 200, 140)
L_YELLOW = (255, 255, 140)
L_GREEN  = (140, 255, 140)
L_SBLUE  = (140, 255, 255)
L_BLUE   = (140, 140, 255)
L_PURPLE = (200, 140, 255)

class Block:
    def __init__(self, num):
        self.data = np.zeros((4, 4), dtype = int)
        self.num = num
        rn = r.randrange(7)
        if rn > 6: rn = 5
        self.next = rn
        self.color = WHITE
        self.get_block(num)
        self.warning = False

    @staticmethod
    def index_to_color(num):
        color_list = [L_RED, L_ORANGE, L_YELLOW, L_GREEN, L_SBLUE, L_BLUE, L_PURPLE]
        return color_list[num]

    @staticmethod
    def convert_quaternary(num):
        notation = '0123456789ABCDEF'
        q, r = divmod(num, 4)
        n = notation[r]
        return Block.convert_quaternary(q) + n if q else n

    @staticmethod
    def sample_block_data(num):
        data = np.zeros((4, 4), dtype = int)
        entire_data = [[1, 2, 5, 9], [1, 2, 6, 10], [1, 5, 6, 10], [2, 5, 6, 9], [5, 6, 9, 10], [1, 5, 9, 13], [1, 5, 6, 9]]

        cur_data = entire_data[num]

        for i in cur_data:
            r = int(Block.convert_quaternary(i)) // 10
            c = int(Block.convert_quaternary(i)) % 10
            data[r][c] = 1
        
        return data

    def get_block(self, num):
        self.data = Block.sample_block_data(num)
        self.color = Block.index_to_color(num)

    def rotate_block(self):
        data = np.zeros((4, 4), dtype = int)

        for i in range(4):
            for j in range(4):
                if self.data[i][j] == 1:
                    data[j][3 - i] = 1
        
        self.data = data

    def color_block(self, color):
        self.color = color