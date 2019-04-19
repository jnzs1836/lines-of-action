from game.agent import Agent, Node, traversal, RandomAgent, AIAgent
from game.game import Game, BLACK, BLANK, WHITE
if __name__ == '__main__':
    game = Game()

    game.show()
    opponent = RandomAgent(game.agents[WHITE], WHITE)
    ai = AIAgent(game.agents[BLACK],BLACK)
    r = 0
    for i in range(1000):
        print(i)
        r = ai.play(game)
        if r < 0:
            break
        r = opponent.play(game)
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
