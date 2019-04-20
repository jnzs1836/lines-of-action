import time
from game.agent import Agent, Node, traversal, PlayerAgent, AIAgent
from game.game import Game, BLACK, BLANK, WHITE
if __name__ == '__main__':
    game = Game()

    game.show()
    while True:
        PlayerMode = input("Choose a Side, Black or White:")
        if PlayerMode == "White":
            opponent = PlayerAgent(game.agents[WHITE], WHITE)
            ai = AIAgent(game.agents[BLACK],BLACK)
            break
        elif PlayerMode == "Black":
            opponent = PlayerAgent(game.agents[BLACK], BLACK)
            ai = AIAgent(game.agents[WHITE],WHITE)
            break
        else:
            continue
    r = 0
    i = 0
    while True:
        print(i)
        i = i + 1
        Flag = WHITE
        if PlayerMode == "White":
            time_start = time.time()
            r = ai.play(game)
            time_end = time.time()
            time_used = time_end - time_start
            print("Time Used:", time_used)
            game.show()
            if r < 0 or time_used > 60:
                break
            Flag = BLACK
        time_start = time.time()
        r = opponent.play(game)
        time_end = time.time()
        time_used = time_end - time_start
        print("Time Used:", time_used)
        game.show()
        if r < 0 or time_used > 60:
            break
        Flag = BLACK
        if PlayerMode == "Black":
            time_start = time.time()
            r = ai.play(game)
            time_end = time.time()
            time_used = time_end - time_start
            print("Time Used:", time_used)
            game.show()
            if r < 0 or time_used > 60:
                break
    if time_used > 60 and Flag == WHITE:
        print("White wins: Black Out of Time")
    elif time_used > 60 and Flag == BLACK:
        print("Black wins: White Out of Time")
    elif (-1) * r == BLACK:
        print("Black wins")
    else:
        print("White wins")
    game.show()
