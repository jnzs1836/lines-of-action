import math
import random
from game.game import Game, BLACK, WHITE, evaluate
import copy
import time
from multiprocessing import Pool


class Node(object):
    def __init__(self, operation, side=WHITE):
        self.q = 0
        self.n = 0
        self.side = side
        self.choose_node = operation[0]
        self.direction = operation[1]
        self.board = operation[2]
        game = Game(self.board, opposite_side(self.side))
        self.children = []
        self.hash = 0
        self.operations = game.get_valid_operations()

    def expand(self):
        flag = 0
        if len(self.children) == len(self.operations):
            return None
        else:
            created_node = Node(self.operations[len(self.children)], opposite_side(self.side))
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
        test_count = 0

        while True:
            if test_count > len(self.chess_ids) * 8:
                return (-1) * opposite_side(self.side)
            # operations = game.get_invalid_operations()
            # b = time.time()
            # print(b-a)
            # operation = operations[int(random.random() * len(operations))]
            if len(self.chess_ids) <= 1:
                return opposite_side(self.side)
            index = int(random.random() * float(len(self.chess_ids)))
            chess_id = self.chess_ids[index]
            chess_id = copy.deepcopy(chess_id)
            chess = game.construct_pos(chess_id)
            # print(self.chess_ids)
            # a = time.time()
            # result = game.play_by_direction(chess, operation[1])

            # print(self.chess_ids)
            result = game.play_by_direction_unsafe(chess, int(8 * random.random()))
            if result == -3:
                test_count += 1
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

    def corrective_strategy(self, game, operations):
        bound = 3.
        default_value = evaluate(game.board, self.side)
        score_sum = 0.
        epsilon = 0.001
        scores = []
        for operation in operations:
            value = evaluate(operation[2], self.side)
            if value > bound:
                return operation
            elif value <= default_value:
                scores.append(epsilon)
                # operation.append(epsilon)
            else:
                scores.append(value)
            score_sum += value
        score_sum += random.random()
        for i in range(len(operations)):
            score_sum -= scores[i]
            if score_sum < 0:
                return operations[i]



class AIAgent(Agent):
    def __init__(self, chess_ids, side):
        super( AIAgent, self).__init__(chess_ids, side)
        game = Game()
        self.node = Node([-1, -1, game.board], WHITE)
        self.traversal_times = 40

    def play(self,game):
        # traversal(node)
        self.process_opponent_operation(game)
        a = time.time()
        for i in range(self.traversal_times):
            traversal(self.node, self.side)

        next_node, operation_value = self.node.optimal()
        if not next_node:
            return (-1) * opposite_side(self.side)
        self.node = next_node
        chess = next_node.choose_node
        direction = next_node.direction
        r = game.play_by_direction(chess, direction)
        b = time.time()
        print(b-a)
        return r

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


def get_simulation_func(expand_node, side):
    def func(i):
        return simulation(expand_node,side)
    return func


def traversal(node, side):
    delta = 0
    simulation_times = 1
    expand_node = node.expand()
    if expand_node:
        # func = get_simulation_func(expand_node,side)
        # results = list(pool.map(f,[0,0]))
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
    a = time.time()
    game = Game(node.board, opposite_side(node.side))

    node_agent = Agent(game.agents[node.side], node.side)
    opponent_agent = Agent(game.agents[opposite_side(node.side)],opposite_side(node.side))
    r = 0
    count = 0
    while True:
        r = opponent_agent.play(game)
        if r < 0:
            break
        r = node_agent.play(game)
        if r < 0:
            break
        if len(game.agents[side]) <= 2:
            r = (-1) * opposite_side(side)
            break
        count += 1
        if count > 250:
            print(count)

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

