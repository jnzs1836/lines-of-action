from game.agent import Agent, Node, traversal, RandomAgent, AIAgent
from game.game import Game, BLACK, BLANK, WHITE, evaluate_mobility
if __name__ == '__main__':
    game = Game()

    game.show()
    random_side = BLACK
    ai_side = WHITE
    agents = {
        ai_side: AIAgent(game.agents[ai_side],ai_side),
        random_side: RandomAgent(game.agents[random_side], random_side)
    }
    # white_agent = RandomAgent(game.agents[random_side], random_side)
    # black_agent = AIAgent(game.agents[ai_side],ai_side)
    r = 0
    print(evaluate_mobility(game))
    for i in range(1000):
        print(i, end=': ')
        r = agents[BLACK].play(game)
        if r < 0:
            break
        r = agents[WHITE].play(game)
        if r < 0:
            break
    if (-1) * r == BLACK:
        print("Black wins")
    else:
        print("White wins")
    game.show()
    # print(r
    # node = Node([-1,-1,game.board], WHITE)
    # # traversal(node)
    # for i in range(100):
    #     traversal(node)
    # print(node)
    # next_operation, operation_value = node.optimal()
    # opponent = RandomAgent(game.agents[WHITE],WHITE)
    # chess = next_operation.choose_node
    # direction = next_operation.direction
    # game.play_by_direction(chess, direction)
    # game.show()
    # print(next_operation)
    # opponent.play(game)
    # game.show()
