import math
import random
from game.game import Game, BLACK, WHITE
import copy
import time


agent_side = BLACK


class Node(object):
    def __init__(self, operation, side=BLACK):
        self.q = 0
        self.n = 0
        self.side = side
        self.choose_node = operation[0]
        self.direction = operation[1]
        self.board = operation[2]
        self.children = []
        self.hash = 0

    def expand(self):
        flag = 0
        game = Game(self.board)
        operations = game.get_valid_operations()
        if len(self.children) == len(operations):
            return None
        else:
            created_node = Node(operations[len(self.children)])
            self.children.append(created_node)
            return created_node
        # for operation in game.get_valid_operations():
        #     flag = 1
        #     self.children.append(created_node)
        # if flag == 0:
        #     return 0

    def optimal(self):
        optimal_value = -0.1
        optimal_node = None
        for child in self.children:
            if float(child.q)/float(child.n) > optimal_value:
                optimal_value = float(child.q)/float(child.n)
                optimal_node = child
        return optimal_node, optimal_value

    def get_child_by_operation(self, game):
        operation = game.get_last_operation()
        for child in self.children:
            if child.choose_node[0] == operation[0][0] and child.choose_node[1] == operation[0][1] and child.direction == operation[1]:
                return child
        return Node(operation,opposite_side(self.side))
# def construct_board(operation)


class Agent(object):
    def __init__(self, chess_ids, side):
        self.side = side
        self.chess_ids = chess_ids

    def play(self,game):
        while True:
            operations = game.get_valid_operations()
            operation = operations[int(random.random() * len(operations))]
            # chess_id = self.chess_ids[int(random.random() * len(self.chess_ids))]
            # chess_id = copy.deepcopy(chess_id)
            # chess = game.construct_pos(chess_id)
            # print(self.chess_ids)
            result = game.play_by_direction(operation[0], operation[1])
            # print(self.chess_ids)
            if result == -3:
                continue
            elif result < 0:
                # print(result)
                # game.show()
                return result
            else:
                return result
            # if result >= 0:
                # self.update(chess_id,result)

    def remove(self,r):
        if r in self.chess_ids:
            self.chess_ids.remove(r)

    def update(self,old, r):
        print(old)
        print(self.chess_ids)
        self.chess_ids.remove(old)
        self.chess_ids.append(r)


class AIAgent(Agent):
    def __init__(self, chess_ids, side):
        super( AIAgent, self).__init__(chess_ids, side)
        game = Game()
        self.node = Node([-1, -1, game.board], )
        self.traversal_times = 40

    def play(self,game):
        # traversal(node)
        self.process_opponent_operation(game)
        for i in range(self.traversal_times):
            traversal(self.node, self.side)
        next_node, operation_value = self.node.optimal()
        if not next_node:
            return (-1) * opposite_side(self.side)
        self.node = next_node
        print(next_node)
        chess = next_node.choose_node
        direction = next_node.direction
        return game.play_by_direction(chess, direction)

    def process_opponent_operation(self, game):
        operation = game.get_last_operation()
        if operation:
            self.node = self.node.get_child_by_operation(game)
        else:
            pass


class RandomAgent(Agent):
    # def play(self,game):
    #     while True:
    #         chess_id = self.chess_ids[int(random.random() * len(self.chess_ids))]
    #         chess_id = copy.deepcopy(chess_id)
    #         chess = game.construct_pos(chess_id)
    #         # print(self.chess_ids)
    #         result = game.play_by_direction(chess, int(8 * random.random()))
    #         # print(self.chess_ids)
    #         if result == -3:
    #             continue
    #         elif result < 0:
    #             # print(result)
    #             # game.show()
    #             return result
    #         else:
    #             return result
    def play(self,game):
        operations = game.get_valid_operations()
        operation = operations[int(random.random() * len(operations))]
        # chess_id = self.chess_ids[int(random.random() * len(self.chess_ids))]
        # chess_id = copy.deepcopy(chess_id)
        # chess = game.construct_pos(chess_id)
        # print(self.chess_ids)
        return game.play_by_direction(operation[0], operation[1])
        # print(self.chess_ids)


def upper_confidence_bounds( q, n, n_parent):
        c = math.sqrt(2)
        return q/n + c * math.sqrt(math.log(n_parent) / n)


def traversal(node, side):
    delta = 0
    simulation_times = 10
    expand_node = node.expand()
    if expand_node:
        for i in range(simulation_times):
            delta += simulation(expand_node, side)
        expand_node.n += simulation_times
        expand_node.q += delta
    else:
        chosen_node = tree_policy(node)
        delta = traversal(chosen_node, side)
    node.q += delta
    node.n += simulation_times
    # print(delta)
    return delta


def tree_policy(node):
    chosen_node = None
    max_bounds = 0
    for child in node.children:
        if child.n == 0:
            return child
        if upper_confidence_bounds(child.q,child.n,node.n) > max_bounds:
            chosen_node = child
            max_bounds = upper_confidence_bounds(child.q,child.n,node.n)
    return chosen_node


def simulation(node, side):
    game = Game(node.board,agent_side)

    black_agent = Agent(game.agents[BLACK],BLACK)
    white_agent = Agent(game.agents[WHITE],WHITE)
    r = 0
    a = time.time()
    while True:
        r = black_agent.play(game)
        if r < 0:
            break
        r = white_agent.play(game)
        if r < 0:
            break
    b = time.time()
    # print(b - a)
    if (-1) * r == side:
        return 0
    elif (-1) * r == opposite_side(side):
        return 1
    # if ((-1*r) & agent_side):
    #     return 1
    # else:
    #     return 0


def opposite_side(side):
    if side == WHITE:
        return BLACK
    else:
        return WHITE