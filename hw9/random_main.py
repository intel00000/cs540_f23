import game
import random

def random_main():
    print('Hello, this is Samaritan')
    ai = game.TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:
       
        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
            
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                poss = ai.succ_opp(ai.board,opp=True)

                # pick a random move from the list of possible moves
                player_move = poss[random.randint(0, len(poss)-1)][1]
                print(player_move)
               
                try:
                    ai.opponent_move(player_move)
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:
        
      

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                poss = ai.succ_opp(ai.board, opp=True)
                
                player_move = random.choice(poss)[1]
                
                move_to = player_move[0]
                move_from = player_move[1]
               
                try:
                    ai.opponent_move([(int(move_to[0]),int(move_to[1]) ),
                                    (int(move_from[0]),int(move_to[1])) ])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")



if __name__ == '__main__':
    random_main()