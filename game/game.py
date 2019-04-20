# from game.constants import BLACK, WHITE
BLACK = 2
WHITE = 1
BLANK = 0
import copy
import time


DIRECTED = 1
NOT_DIRECTED = 0

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
        self.valid_operations = {
            BLACK: [],
            WHITE: []
        }
        self.agents = {
            BLACK: [],
            WHITE: []
        }
        self.agents_operation_candidates = {
            BLACK: {},
            WHITE: {}
        }
        if board:
            self.board = board
            self.status = status
            self.count = [0, 0, 0]

            self.init_agents()

        else:
            self.board = []
            self.status = status
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
        self.build_operation_candidates()

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
        if checking_pos[0] < 0 or checking_pos[0] >= 8 or checking_pos[1] < 0 or checking_pos[1] >= 8:
            return False
        return True

    def play_by_direction_unsafe(self,  chess, direction):
        if self.valid_direction(chess, direction):
            # steps = self.next_steps(chess,direction)
            # parsed_direction = self.parse_direction(direction)
            # pos = (chess[0] + parsed_direction[0] * steps, chess[1] + parsed_direction[1] * steps)
            next_pos = self.get_next_pos(chess, direction)
            self.last_operation = [chess,direction]
            if not self.check_pos(next_pos):
                return -3

            if not self.move(chess, next_pos):
                return -3
            if self.judge(WHITE) :
                return (-1) * WHITE
            elif self.judge(BLACK):
                return (-1) * BLACK
            self.switch()
            return next_pos[0] * 8 + next_pos[1]
        else:
            return -3

    def play_by_direction(self, chess, direction, next_pos=None):
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
            return -3

    def move(self,chess,next_pos):
        chess_id = chess[0] * 8 + chess[1]
        next_pos_id = next_pos[0] * 8 + next_pos[1]
        if self.board[next_pos[0]][next_pos[1]] == self.status:
            return False
        self.update_operation_candidates(chess_id, chess, next_pos_id, next_pos, self.board[chess[0]][chess[1]])
        if self.board[next_pos[0]][next_pos[1]] == BLACK:
            self.count[BLACK] -= 1
            self.agents[BLACK].remove(next_pos_id)
        elif self.board[next_pos[0]][next_pos[1]] == WHITE:
            self.count[WHITE] -= 1
            self.agents[WHITE].remove(next_pos_id)
        else:
            pass
        self.board = self.change_board(self.board,chess,next_pos,self.status)
        # self.board[chess[0]][chess[1]] = BLANK
        # self.board[next_pos[0]][next_pos[1]] = self.status
        self.agents[self.status].append(next_pos_id)
        self.agents[self.status].remove(chess_id)
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
        # if next_pos[0] >= 8 or next_pos[0] < 0 or next_pos[1] >= 8 or next_pos[1] < 0:
        #     return False
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

    def check_side(self, next_pos, side):
        if self.board[next_pos[0]][next_pos[1]] == side:
            return False
        else:
            return True

    def get_direction(self, move):
        if move[0] != 0:
            if move[1] != 0:
                if abs(move[1]) != abs(move[0]):
                    return -1
                elif move[0] < 0:
                    if move[1] < 0:
                        direction = DIRECTION['UP-LEFT']
                    else:
                        direction = DIRECTION['UP-RIGHT']
                elif move[1] < 0:
                    direction = DIRECTION['DOWN-LEFT']
                else:
                    direction = DIRECTION['DOWN-RIGHT']
            else:
                direction = 2 * move[0]/abs(move[0]) + 2
        elif move[1] != 0:
            direction = (-2) * move[1] / abs(move[1]) + 4
        else:
            return -1
        return int(direction)

    def build_operation_candidates_of_chess(self, chess, side):
        direction = -1
        operation_candidates = []
        for i in range(8):
            operation_candidates.append({
                'stopped': 8,
                'steps': 1,
                'mate_distance': {},
                'opponent_distance': {},
            })
        for candidate_chess_id in self.agents[side]:
            candidate_chess = self.construct_pos(candidate_chess_id)
            move = [candidate_chess[0] - chess[0], candidate_chess[1] - chess[1]]
            direction = self.get_direction(move)
            if direction < 0:
                continue
            operation_candidates[direction]['steps'] += 1
            operation_candidates[(4 + direction) % 8]['steps'] += 1
            distance = 0
            if direction % 4 == 0:
                distance = abs(candidate_chess[0] - chess[0])
            else:
                distance = abs(candidate_chess[1] - chess[1])
            operation_candidates[direction]['mate_distance'][candidate_chess_id] = distance
        for candidate_chess_id in self.agents[opposite_side(side)]:
            candidate_chess = self.construct_pos(candidate_chess_id)
            move = [candidate_chess[0] - chess[0], candidate_chess[1] - chess[1]]
            direction = self.get_direction(move)
            if direction < 0:
                continue
            operation_candidates[direction]['steps'] += 1
            operation_candidates[(4 + direction) % 8]['steps'] += 1
            change = 0
            if direction % 4 == 0:
                distance = abs(candidate_chess[0] - chess[0])
            else:
                distance = abs(candidate_chess[1] - chess[1])
            operation_candidates[direction]['opponent_distance'][candidate_chess_id] = distance
            if abs(move[0]) > abs(move[1]):
                change = abs(move[0])
            else:
                change = abs(move[1])
            if change < operation_candidates[direction]['stopped']:
                operation_candidates[direction]['stopped'] = change
        return operation_candidates

    def build_operation_candidates(self):
        for key, chess_ids in self.agents.items():
            for chess_id in chess_ids:
                self.agents_operation_candidates[key][chess_id] = self.build_operation_candidates_of_chess(self.construct_pos(chess_id), key)

    def build_valid_operations_from_chess_operation_candidates(self, chess, operation_candidates):
        valid_operations = []
        for i in range(8):
            operation = operation_candidates[i]
            parsed_direction = self.parse_direction(i)
            next_pos = [chess[0] + parsed_direction[0] * operation['steps'],
                        chess[1] + parsed_direction[1] * operation['steps']]
            if not self.check_pos(next_pos):
                continue
            if operation['stopped'] >= operation['steps']:
                flag = 0
                for value in operation['mate_distance'].values():
                    if value == operation['steps']:
                        flag = 1
                        break
                if flag == 1:
                    continue
                valid_operations.append([chess, i, True, next_pos])
        return valid_operations

    def find_influenced_chess(self, chess, side):
        influenced = {
            'mate': [],
            'opponent': [],
        }
        for candidate_chess_id in self.agents[side]:
            candidate_chess = self.construct_pos(candidate_chess_id)
            move = [chess[0] - candidate_chess[0],  chess[1] - candidate_chess[1]]
            direction = self.get_direction(move)
            if direction < 0:
                continue
            influenced['mate'].append([candidate_chess_id, direction, DIRECTED])
            influenced['mate'].append([candidate_chess_id, (4 + direction) % 8, NOT_DIRECTED])

        for candidate_chess_id in self.agents[opposite_side(side)]:
            candidate_chess = self.construct_pos(candidate_chess_id)
            move = [ chess[0] - candidate_chess[0], chess[1] - candidate_chess[1]]
            direction = self.get_direction(move)
            if direction < 0:
                continue
            influenced['opponent'].append([candidate_chess_id, direction, DIRECTED])
            influenced['opponent'].append([candidate_chess_id, (4 + direction) % 8, NOT_DIRECTED])

        return influenced

    def update_operation_candidates(self, old_id, old, target_id, target, side):
        old_influenced = self.find_influenced_chess(old, side)
        for item in old_influenced['mate']:
            operation_candidate = self.agents_operation_candidates[side][item[0]][item[1]]
            operation_candidate['steps'] -= 1
            if item[2] == DIRECTED:
                del operation_candidate['mate_distance'][old_id]
        for item in old_influenced['opponent']:
            operation_candidate = self.agents_operation_candidates[opposite_side(side)][item[0]][item[1]]
            operation_candidate['steps'] -= 1
            if item[2] == NOT_DIRECTED:
                continue
            if operation_candidate['opponent_distance'][old_id] == operation_candidate['stopped']:
                del operation_candidate['opponent_distance'][old_id]
                operation_candidate['stopped'] = 8
                for chess_id, distance in operation_candidate['opponent_distance'].items():
                    if distance < operation_candidate['stopped']:
                        operation_candidate['stopped'] = distance
            else:
                del operation_candidate['opponent_distance'][old_id]
        del self.agents_operation_candidates[side][old_id]
        target_influenced = self.find_influenced_chess(target, side)
        for item in target_influenced['mate']:
            if item[0] == old_id:
                continue
            operation_candidate = self.agents_operation_candidates[side][item[0]][item[1]]
            operation_candidate['steps'] += 1
            if item[2] == NOT_DIRECTED:
                continue
            distance = 0
            if item[1] % 4 == 0:
                distance = abs(self.construct_pos(item[0])[0] - target[0])
            else:
                distance = abs(self.construct_pos(item[0])[1] - target[1])
            operation_candidate['mate_distance'][target_id] = distance
        for item in target_influenced['opponent']:
            operation_candidate = self.agents_operation_candidates[opposite_side(side)][item[0]][item[1]]
            operation_candidate['steps'] += 1
            if item[2] == NOT_DIRECTED:
                continue
            distance = 0
            if item[1] % 4 == 0:
                distance = abs(self.construct_pos(item[0])[0] - target[0])
            else:
                distance = abs(self.construct_pos(item[0])[1] - target[1])
            operation_candidate['opponent_distance'][target_id] = distance
            if distance < operation_candidate['stopped']:
                operation_candidate['stopped'] = distance
        self.agents_operation_candidates[side][target_id] = self.build_operation_candidates_of_chess(target, side)

    def get_operations_of_chess(self, chess):
        chess_id = chess[0] * 8 + chess[1]
        # operation_candidates = self.agents_operation_candidates[self.board[chess[0]][chess[1]]][chess_id]
        operation_candidates = self.build_operation_candidates_of_chess(chess, self.board[chess[0]][chess[1]])
        return self.build_valid_operations_from_chess_operation_candidates(chess, operation_candidates)

    def get_operations_from_index(self):
        valid_operations = []
        for chess_id, operation_candidates in self.agents_operation_candidates[self.status].items():
            valid_operations.extend(self.build_valid_operations_from_chess_operation_candidates(self.construct_pos(chess_id), operation_candidates))
        return valid_operations
            # distance = candidate_chess_id - chess_id
            #
            # if distance % 9 == 0 and distance / 9 < 7 - (chess_id % 8) :
            #     direction = 3
            # elif distance % 7 == 0 and distance / 7 < (chess_id % 8):
            #     direction = 5
            # elif distance % 8 == 0:
            #     direction = 4
            # elif chess_id /8 == candidate_chess_id / 8:
            #     direction = 5
            # else:
            #     pass
            # if candidate_chess_id % 8 < chess_id :
            #     direction = 4 + direction



    # candidate_chess = self.construct_pos(candidate_chess_id)
    # if chess[0] - candidate_chess[0] == 0:
    #     if chess[1] - candidate_chess[1] == 0:
    #
    #     continue
    def next_steps(self,chess,direction):
        steps = 0
        side = self.board[chess[0]][chess[1]]
        pos = []
        # stopped = []
        # for candidate_chess_id in self.agents[self.status]:
            # distance = candidate_chess_id -
            # candidate_chess = self.construct_pos(candidate_chess_id)
            # if chess[0] - candidate_chess[0] == 0:
            #     if chess[1] - candidate_chess[1] == 0:
            #
            #     continue
            #
            # move = [chess[0] - candidate_chess[0], chess[1] - candidate_chess[1]]


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
                    == opposite_side(self.board[chess[0]][chess[1]]):
                return None
        # result = self.check_side(next_pos, self.board[chess[0]][chess[1]])
        result = self.change_board(self.board, chess, next_pos, self.board[chess[0]][chess[1]])
        if result:
            return [chess, direction, result, next_pos]
        else:
            return None

    def valid_operation_for_evaluation(self, chess_id, direction):

        chess = self.construct_pos(chess_id)

        steps = self.next_steps( chess, direction)

        parsed_direction = self.parse_direction(direction)
        next_pos = (chess[0] + parsed_direction[0] * steps, chess[1] + parsed_direction[1] * steps)


        if not self.check_pos(next_pos):
            return None

        for i in range(1,steps):
            if self.board[chess[0] + parsed_direction[0] * i][chess[1] + parsed_direction[1] * i] \
                    == opposite_side(self.board[chess[0]][chess[1]]):
                return None

        result = self.check_side(next_pos, self.board[chess[0]][chess[1]])
        # result = self.change_board(self.board, chess, next_pos, self.board[chess[0]][chess[1]])

        # if b -a > 0.:
        #     print(b-a)

        if result:
            return [chess, direction, result, next_pos]
        else:
            return None

    def get_valid_operations_for_evaluation(self):
        operations = []
        for chess_id in self.agents[self.status]:
            operations.extend(self.get_operations_of_chess(self.construct_pos(chess_id)))

            # for i in range(8):
            #     operation = self.valid_operation_for_evaluation(chess_id, i)
            #     if operation:
            #         operations.append(operation)
        return operations

    def get_opposite_valid_operations_for_evaluation(self):
        operations = []
        for chess_id in self.agents[opposite_side(self.status)]:
            for i in range(8):
                operation = self.valid_operation_for_evaluation(chess_id, i)
                if operation:
                    operations.append(operation)
        return operations

    def get_valid_operations(self):
        operations = []
        for chess_id in self.agents[self.status]:
            for i in range(8):
                operation = self.valid_operation(chess_id,i)
                if operation:
                    operations.append(operation)
        return operations

    def get_opposite_valid_operations(self):
        operations = []
        for chess_id in self.agents[opposite_side(self.status)]:
            for i in range(8):
                operation = self.valid_operation(chess_id, i)
                if operation:
                    operations.append(operation)
        return operations

    def get_invalid_operations(self):
        operations = []
        for chess_id in self.agents[self.status]:
            chess = self.construct_pos(chess_id)
            for i in range(8):
                next_pos = self.get_next_pos(chess,i)
                result = self.change_board(self.board, chess, next_pos, self.status)
                if result:
                    operations.append((chess, i, result))
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

    def update(self, chess, next_pos, side):
        for operation in self.valid_operations[side]:
            if not self.check_operation(operation):
                self.valid_operations[side].remove(operation)

    def check_operation(self, operation):
        return True

    def get_related_operations(self, chess):
        test_pos = []
        related = []
        for i in range(8):
            parsed_direction = self.parse_direction(i)
            test_pos = [chess[0] + parsed_direction[0], chess[1] + parsed_direction[1]]
            while self.check_pos(test_pos):
                test_pos[0] += parsed_direction[0]
                test_pos[1] += parsed_direction[1]
                if self.board[test_pos[0]][test_pos[1]] != BLANK:
                    related.append([[test_pos[0], test_pos[1]], i])
                    related.append([[test_pos[0], test_pos[1]], 7 - i])
        return related


def evaluate(game):
    return evaluate_mobility(game)


def evaluate_mobility(game):
    my_score = calculate_mobility(game.get_valid_operations_for_evaluation())
    opponent_score = calculate_mobility(game.get_opposite_valid_operations_for_evaluation())
    return my_score - opponent_score


def calculate_mobility(operations):
    score = 0.
    for operation in operations:
        if operation[3] != BLANK:
            if (operation[3][0] == 0 or operation[3][0] == 7) and( operation[3][1] == 7 or operation[3][1] == 0):
                score += 0.5
            elif operation[3][0] == 0 or operation[3][0] == 7 or operation[3][1] == 0 or operation[3][1] == 7:
                score += 0.5
            else:
                score += 2.
        else:
            score += 1.
    return score

if __name__ == '__main__':
    game = Game()
    # game.show()
    # print(game.adjacent_set(0))
    pos = game.play_by_direction((0,1),DIRECTION['DOWN-RIGHT'])
    print(pos)
    game.show()