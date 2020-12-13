from boardstate import *
from AI import *


def main():
    g = Boardstate(8)
    Boardstate.DEBUG_MODE = True
    print (g)
    while not g.is_game_over:
        if g.next_turn == BLACK:
            r = int(input("Enter r: "))
            c = int(input("Enter c: "))
            next_move = (r, c)
        else:
            score, next_move = AI(g, 1)
            print ("score predicted:", score)
        g, is_valid = get_next_state(g, next_move)
        if not is_valid:
            print ("Invalid move!!!")
        print (g)
    print ("Game over!!")
    if g.winner == BLACK:
        print ("Black wins!")
    elif g.winner == WHITE:
        print ("White wins!")
    else:
        print ("Draw!!")
main()
