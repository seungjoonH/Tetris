import tetris
import numpy as np

class Autoplayer:
    def __init__(self):
        self.t = tetris.Tetris()
    
    def find_optimized_position(self):
        temp_board = np.zeros((22, 12), dtype = int)
        tetris.Tetris.initialize_board(temp_board)

        best_score = -10000
        best_pos = 0
        best_rot = 0
        
        for rot in range(4):
            for pos in range(-5, 6):
                try:
                    self.t.block_pos[1] = pos + 4
                    self.t.locate_block()
                    temp_board = self.t.block_offset(0, self.t.preview_vertical_fall(), 0)
                    self.t.block_pos[1] = 4
                    self.t.locate_block()

                    if best_score < self.score_position(temp_board):
                        best_score = self.score_position(temp_board)
                        best_pos = pos
                        best_rot = rot

                except:
                    continue

            self.t.rotate_block()
        
        #sys.exit()
        return best_pos, best_rot

    def score_position(self, board):
        score = 0
        for i in range(1, 21):
            for j in range(1, 11):
                score += abs(board[i][j] - 6)
            score += (i - 10) * sum(board[i])

            if sum(board[i]) == 12:
                score += score + 10000
        
        for i in range(1, 11):
            obturate = 0
            weight = 0

            for j in range(1, 21):
                if board[j][i] == 1:
                    obturate = j
                    weight = 1

                if 0 < obturate < j and board[j][i] == 0:
                    score -= weight * 10
                    weight += 1
                        
        if 2 in board:
            score -= 10000

        if self.t.block.num != 5:
            for i in range(1, 21):
                score -= board[i][10] * 10

        return score

    # def auto_rotatemove(self):
    #     pos, rot = self.find_optimized_position()
    #     for i in range(rot):
    #         self.t.rotate_block()
    #         self.t.locate_block()
    #     self.t.move_block(pos, 0)
    #     self.t.locate_block()

    # def auto_place(self):
    #     self.t.vertical_fall()
    #     self.t.next_block()
    #     self.t.erase_line()

    def auto_place(self, s):
        pos, rot = self.find_optimized_position()
        
        if s < 4 and rot != 0:
            self.t.rotate_block()

        elif s <= 9:
            lamb = lambda i: np.sign(pos) * (i - 3) if (i - 3) < np.sign(pos) else pos
            self.t.move_block(lamb(s), 0)
        
        if s == 9:
            self.t.vertical_fall()
            self.t.next_block()
            self.t.erase_line()

        if s != 8 and not (rot * rot):
            return True
        
        return False