# from game.constants import BLACK, WHITE
BLACK = 2
WHITE = 1
BLANK = 0

def opposite_side(side):
    if side == WHITE:
        return BLACK
    else:
        return WHITE


DIRECTION = {
    'UP': 0,
    'UP-RIGHT':1,
    'RIGHT':2,
    'DOWN-RIGHT':3,
    'DOWN':4,
    'DOWN-LEFT':5,
    'LEFT':6,
    'UP-LEFT':7
}


class Game(object):
    def __init__(self, board=None, status=BLACK):
        self.last_operation = None
        self.agents = {
            BLACK: [],
            WHITE: []
        }
        if board:
            self.board = board
            self.status = BLACK
            self.count = [0,0,0]

            self.init_agents()

        else:
            self.board = []
            self.status = BLACK
            self.count = [
                0,12,12
            ]
            # self.black_count = 8
            # self.white_count = 8
            for i in range(8):
                row = []
                for j in range(8):
                    row.append(0)
                self.board.append(row)
            self.init_board()
            self.init_agents()

    def init_agents(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == BLACK:
                    self.count[BLACK] += 1
                    self.agents[BLACK].append(8 * i + j)
                elif self.board[i][j] == WHITE:
                    self.count[WHITE] += 1
                    self.agents[WHITE].append(8 * i + j)
                else:
                    pass

    def init_board(self):
        for i in range(6):
            self.board[0][i+1] = BLACK
            self.board[7][i+1] = BLACK
            self.board[i+1][0] = WHITE
            self.board[i+1][7] = WHITE

    def show(self):
        shown_text = [' ','W','B']
        for i in range(8):
            print(" | ",end='')
            for j in range(8):
                print(shown_text[self.board[i][j]],end=' | ')
            print("")
        print("")

    # def play_by_pos(self, chess, next_pos):
    #     if self.valid(chess,next_pos):
    #         self.board[next_pos[0]][next_pos[1]] = self.status
    #         self.board[chess[0]][chess[1]] = BLANK
    #         self.switch()
    # @staticmethod
    def parse_direction(self, direction):
        parsed_direction = [0, 0]
        if direction > 6 or direction < 2:
            parsed_direction[0] = -1
        elif (direction - 2) % 4 == 0:
            parsed_direction[0] = 0
        else:
            parsed_direction[0] = 1
        if direction % 4 == 0:
            parsed_direction[1] = 0
        elif direction < 4:
            parsed_direction[1] = 1
        else:
            parsed_direction[1] = -1
        return parsed_direction

    def check_pos(self, checking_pos):
        if checking_pos[0] < 0 or checking_pos[0] >= 8 or checking_pos[1] < 0 or checking_pos[1] >=8:
            return False
        return True

    def play_by_direction(self, chess, direction, next_pos=None):
        if not next_pos:
            next_pos = self.get_next_pos(chess, direction)
        self.last_operation = [chess, direction]
        # if not self.check_pos(next_pos):
        #     return -3
        # print("here")
        if not self.move(chess, next_pos):
            return -3
        # print("not 3")
        # self.show()
        if self.judge(WHITE) or len(self.agents[BLACK]) <= 1:
            return (-1) * WHITE
        elif self.judge(BLACK) or len(self.agents[WHITE]) <= 1:
            return (-1) * BLACK
        # print("black and white")
        self.switch()
        return next_pos[0] * 8 + next_pos[1]
        if self.valid_direction(chess,direction):
            # steps = self.next_steps(chess,direction)
            # parsed_direction = self.parse_direction(direction)
            # pos = (chess[0] + parsed_direction[0] * steps, chess[1] + parsed_direction[1] * steps)
            if not next_pos:
                next_pos = self.get_next_pos(chess, direction)
            self.last_operation = [chess,direction]
            # if not self.check_pos(next_pos):
            #     return -3
            # print("here")
            if not self.move(chess, next_pos):
                return -3
            # print("not 3")
            # self.show()
            if self.judge(WHITE) or len(self.agents[BLACK]) <= 1 :
                return (-1) * WHITE
            elif self.judge(BLACK) or len(self.agents[WHITE]) <= 1:
                return (-1) * BLACK
            # print("black and white")
            self.switch()
            return next_pos[0] * 8 + next_pos[1]
        else:
            print("???")
            return -3

    def move(self,chess,next_pos):
        if self.board[next_pos[0]][next_pos[1]] == self.status:
            return False
        elif self.board[next_pos[0]][next_pos[1]] == BLACK:
            self.count[BLACK] -= 1
            self.agents[BLACK].remove(next_pos[0] * 8 + next_pos[1])
        elif self.board[next_pos[0]][next_pos[1]] == WHITE:
            self.count[WHITE] -= 1
            self.agents[WHITE].remove(next_pos[0] * 8 + next_pos[1])
        else:
            pass
        self.board = self.change_board(self.board,chess,next_pos,self.status)
        # self.board[chess[0]][chess[1]] = BLANK
        # self.board[next_pos[0]][next_pos[1]] = self.status
        self.agents[self.status].append(next_pos[0] * 8 + next_pos[1])
        self.agents[self.status].remove(chess[0] * 8 + chess[1])
        return True

    def switch(self):
        if self.status == BLACK:
            self.status = WHITE
        else:
            self.status = BLACK

    def valid_direction(self,chess,direction):
        if self.board[chess[0]][chess[1]] == self.status:
            return True
        else:
            return False

    def get_next_pos(self, chess, direction):
        steps = self.next_steps(chess, direction)
        parsed_direction = self.parse_direction(direction)
        get_pos = (chess[0] + parsed_direction[0] * steps, chess[1] + parsed_direction[1] * steps)
        return get_pos

    @staticmethod
    def change_board(board, chess, next_pos, side):
        if next_pos[0] >= 8 or next_pos[0] < 0 or next_pos[1] >= 8 or next_pos[1] < 0:
            return False
        if board[next_pos[0]][next_pos[1]] == side:
            return False
        new_board = []
        for i in range(8):
            row = []
            for j in range(8):
                row.append(board[i][j])
            new_board.append(row)
        new_board[chess[0]][chess[1]] = BLANK
        new_board[next_pos[0]][next_pos[1]] = side
        return new_board

    def next_steps(self,chess,direction):
        steps = 0
        side = self.board[chess[0]][chess[1]]
        pos = []
        if direction % 4 == 0:
            for i in range(8):
                if self.board[i][chess[1]] != BLANK:
                    steps += 1
        elif direction % 4 == 1:
            if chess[0] + chess[1] >= 7:
                for i in range(chess[0] + chess[1] - 7, 8):
                    if self.board[i][chess[0] + chess[1] - i] != BLANK:
                        steps += 1
            else:
                for i in range(chess[0] + chess[1] + 1):
                    if self.board[i][chess[0] + chess[1] - i] != BLANK:
                        steps += 1
        elif direction % 4 == 2:
            for i in range(8):
                if self.board[chess[0]][i] != BLANK:
                    steps += 1
        elif direction % 4 == 3:
            if chess[0] > chess[1]:
                l = chess[0] - chess[1]
                for i in range(8 - l):
                    if self.board[l + i][i] != BLANK:
                        steps += 1
            else:
                l = chess[1] - chess[0]
                for i in range(8 - l):
                    if self.board[i][l + i] != BLANK:
                        steps += 1
        return steps

    # def valid(self, chess, next_pos):
    #     return True

    @staticmethod
    def construct_pos(id):
        return [int(id/8), id%8]

    def valid_operation(self, chess_id, direction):
        chess = self.construct_pos(chess_id)
        steps = self.next_steps( chess, direction)
        parsed_direction = self.parse_direction(direction)
        next_pos = self.get_next_pos(chess, direction)
        if not self.check_pos(next_pos):
            return None
        for i in range(1,steps):
            if self.board[chess[0] + parsed_direction[0] * i][chess[1] + parsed_direction[1] * i] \
                    == opposite_side(self.status):
                return None

        result = self.change_board(self.board, chess, next_pos, self.status)
        if result:
            return [chess, direction, result, next_pos]
        else:
            return None

    def get_valid_operations(self):
        operations = []
        for chess_id in self.agents[self.status]:
            for i in range(8):
                operation = self.valid_operation(chess_id,i)
                if operation:
                    operations.append(operation)
        return operations

    def judge(self, side):
        first_found_chess = [-1,-1]
        for i in range(8):
            flag = 0
            for j in range(8):
                if self.board[i][j] == side:
                    first_found_chess = [i,j]
                    flag = 1
                    break
            if flag == 1:
                break
        if first_found_chess[0] == -1:
            return False
        side_set = set()
        to_expand_set = set()
        side_count = 1
        next_chess = first_found_chess
        side_set.add(next_chess[0]* 8 + next_chess[1])
        while True:
            for pos_id in self.adjacent_set(next_chess[0]* 8 + next_chess[1]):
                y = int ( (pos_id - pos_id % 8 )/ 8)
                x = pos_id % 8
                if self.board[y][x] == side and pos_id not in side_set:
                    side_set.add(pos_id)
                    to_expand_set.add(pos_id)
                    side_count += 1
            if len(to_expand_set) == 0:
                break
            next_id = to_expand_set.pop()
            next_chess = [int(next_id/8),next_id %8]
        if side_count == self.count[side]:
            return True
        else:
            return False

    @staticmethod
    def adjacent_set(index):
        ans = [index-1,index+1,index+9,index+7,index-8,index-9,index-7,index+8]
        if index % 8 == 0:
            ans.remove(index - 1)
            ans.remove(index + 7)
            ans.remove(index - 9)
        if index % 8 == 7:
            ans.remove(index + 1)
            ans.remove(index + 9)
            ans.remove(index - 7)
        if index < 8:

            if index - 7 in ans:
                ans.remove(index - 7)
            ans.remove(index -8)
            if index - 9 in ans:
                ans.remove(index -9)
        if index + 8 > 63:
            if index + 9 in ans:
                ans.remove(index + 9)
            if index + 7 in ans:
                ans.remove(index + 7)
            ans.remove(index + 8)
        return ans

    def get_last_operation(self):
        if not self.last_operation:
            return self.last_operation
        if len(self.last_operation) == 2:
            self.last_operation.append(self.board)
        return self.last_operation

if __name__ == '__main__':
    game = Game()
    # game.show()
    # print(game.adjacent_set(0))
    pos = game.play_by_direction((0,1),DIRECTION['DOWN-RIGHT'])
    print(pos)
    game.show()