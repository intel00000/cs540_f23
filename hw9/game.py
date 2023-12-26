import random

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.

        """
        # detect drop phase
        piece_number = len([cell for row in state for cell in row if cell != ' '])
        drop_phase = piece_number < 8
        move = []
        
        if not drop_phase:
            # assume we are the max player, use a depth limit of 3 during the move phase
            max_value, max_state = self.max_value(state, 0, depth_limit = 3)

            # find the difference between the max_state and the current state
            for row in range(5):
                for col in range(5):
                    # if the state piece is the player's piece, this is the source piece, append the position to the end of the move list
                    if state[row][col] != max_state[row][col] and state[row][col] == self.my_piece:
                        # insert the source piece position to the end of the move list
                        move.append((row, col))

                    # find the destination piece position
                    if state[row][col] != max_state[row][col] and state[row][col] == ' ':
                        # insert the destination piece position to the beginning of the move list
                        move.insert(0, (row, col))
            return move

        # minimax algorithm during the drop phase
        # assume we are the max player, use a depth limit of 3 during the drop phase
        max_value, max_state = self.max_value(state, 0, depth_limit = 3)
        # find the difference between the max_state and the current state
        for row in range(5):
            for col in range(5):
                # if the state piece is the player's piece, this is the source piece, append the position to the end of the move list
                if state[row][col] != max_state[row][col] and state[row][col] == self.my_piece:
                    # insert the source piece position to the end of the move list
                    move.append((row, col))

                # find the destination piece position
                if state[row][col] != max_state[row][col] and state[row][col] == ' ':
                    # insert the destination piece position to the beginning of the move list
                    move.insert(0, (row, col))
        return move
    
    # default depth limit is 3
    def max_value(self, state, depth, depth_limit = 3):
        # check for terminal state
        game_value = self.game_value(state)
        if game_value != 0:
            return game_value, state
        
        # if we reach the depth limit, stop the recursion and return the heuristic value
        if depth >= depth_limit:
            return self.heuristic_game_value(state), state

        # initialize max_value, max_state
        max_value = float('-inf')
        max_state = state
        # for each successor, recursively call min_value and compare that with max_value
        for successor in self.succ(state):
            successor_value, successor_state  = self.min_value(successor, depth + 1, depth_limit)
            if successor_value > max_value:
                max_value = successor_value
                max_state = successor

        return max_value, max_state
    
    # default depth limit is 3
    def min_value(self, state, depth, depth_limit = 3):
        # check for terminal state
        game_value = self.game_value(state)
        if game_value != 0:
            return game_value, state
        
        # if we reach the depth limit, stop the recursion and return the heuristic value
        if depth >= depth_limit:
            return self.heuristic_game_value(state), state

        # initialize min_value, min_state
        min_value = float('inf')
        min_state = state
        # for each successor, recursively call max_value and compare that with min_value
        for successor in self.succ(state):
            successor_value, successor_state = self.max_value(successor, depth + 1, depth_limit)
            if successor_value < min_value:
                min_value = successor_value
                min_state = successor

        return min_value, min_state
    
    def succ(self, state):
        """ Generates the successor states for the current state of the game.\
        
        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

        Returns:
            list of lists: a list of successor states, each of which is a list of lists
                representing the board state after a valid move.

        """
        # check if drop phase
        drop_phase = len([cell for row in state for cell in row if cell != ' ']) < 8
        successors = []

        # generate drop phase successors
        if drop_phase:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == ' ':
                        # deep copy the board
                        successor = [row[:] for row in state]
                        # place a piece on the empty space
                        successor[row][col] = self.my_piece
                        successors.append(successor)
        else:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == self.my_piece:
                        # check all adjacent spaces
                        for row_move in range(-1,2):
                            for col_move in range(-1,2):
                                # if the space is empty, move the piece there
                                if 0 <= row + row_move < 5 and 0 <= col + col_move < 5 and state[row + row_move][col + col_move] == ' ':
                                    # deep copy the board
                                    successor = [row[:] for row in state]
                                    # place a piece on the empty space
                                    successor[row + row_move][col + col_move] = self.my_piece
                                    # remove the piece from its previous location
                                    successor[row][col] = ' '
                                    successors.append(successor)
        return successors

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board

        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1
        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1
        # check \ diagonal wins
        for i in range(2):
            if state[i][i] != ' ' and state[i][i] == state[i+1][i+1] == state[i+2][i+2] == state[i+3][i+3]:
                return 1 if state[i][i]==self.my_piece else -1
        # check / diagonal wins
        for i in range(2):
            if state[i][4-i] != ' ' and state[i][4-i] == state[i+1][3-i] == state[i+2][2-i] == state[i+3][1-i]:
                return 1 if state[i][4-i]==self.my_piece else -1
        # check box wins
        for i in range(4):
            for j in range(4):
                if state[i][j] != ' ' and state[i][j] == state[i+1][j] == state[i][j+1] == state[i+1][j+1]:
                    return 1 if state[i][j]==self.my_piece else -1

        return 0 # no winner yet
    
    def heuristic_game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            A score where terminal state where your AI player wins should have the maximal positive score (1), and a terminal state where the opponent wins should have the minimal negative score (-1). This function should return some floating-point value between 1 and -1 when the game is not over.

        """
        # call game_value to check wining conditions
        score = self.game_value(state)
        if score != 0:
            return score
        
        # evaluate the board
        # define one of the heuristic function as the number pieces present in a row, column, diagonal, or box win situation, divided by 4 to normalize the score to 1
        # this heuristic function evaluate the board matching any wining conditions, the larger the score, the more likely the board will win
        my_score = 0
        my_score_max = 0
        opp_score = 0
        opp_score_max = 0

        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] == self.my_piece:
                    my_score += 1
                elif row[i] == self.opp:
                    opp_score += 1
            if my_score > my_score_max:
                my_score_max = my_score
            if opp_score > opp_score_max:
                opp_score_max = opp_score
            my_score = 0
            opp_score = 0
        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] == self.my_piece:
                    my_score += 1
                elif state[i][col] == self.opp:
                    opp_score += 1
            if my_score > my_score_max:
                my_score_max = my_score
            if opp_score > opp_score_max:
                opp_score_max = opp_score
            my_score = 0
            opp_score = 0
        # check \ diagonal wins
        for i in range(2):
            if state[i][i] == self.my_piece:
                my_score += 1
            elif state[i][i] == self.opp:
                opp_score += 1
        if my_score > my_score_max:
            my_score_max = my_score
        if opp_score > opp_score_max:
            opp_score_max = opp_score
        my_score = 0
        opp_score = 0
        # check / diagonal wins
        for i in range(2):
            if state[i][4-i] == self.my_piece:
                my_score += 1
            elif state[i][4-i] == self.opp:
                opp_score += 1
        if my_score > my_score_max:
            my_score_max = my_score
        if opp_score > opp_score_max:
            opp_score_max = opp_score
        my_score = 0
        opp_score = 0
        # check box wins
        for i in range(4):
            for j in range(4):
                if state[i][j] == self.my_piece:
                    my_score += 1
                elif state[i][j] == self.opp:
                    opp_score += 1
            if my_score > my_score_max:
                my_score_max = my_score
            if opp_score > opp_score_max:
                opp_score_max = opp_score
            my_score = 0
            opp_score = 0

        # define an additional heuristic score as the sum of minimum move from each piece to other pieces, diagonal move count as 1
        # the minimum score is will be the box win situation, where the move of each piece to other pieces is 3, and the sum of them is 12
        # this heuristic function evaluate the closeness of the pieces, the larger the score, the closer the pieces are
        my_distance_sum = 0
        opp_distance_sum = 0

        for row in range(5):
            for col in range(5):
                if state[row][col] == self.my_piece:
                    for i in range(5):
                        for j in range(5):
                            # check for diagonal piece
                            if state[i][j] == self.my_piece and abs(row - i) == 1 and abs(col - j) == 1:
                                my_distance_sum += 1
                            elif state[i][j] == self.my_piece:
                                col_distance = abs(col - j)
                                row_distance = abs(row - i)
                                # consider diagonal move when calculating distance
                                my_distance_sum += min(col_distance, row_distance) + abs(col_distance - row_distance)

                elif state[row][col] == self.opp:
                    for i in range(5):
                        for j in range(5):
                            # check for diagonal piece
                            if state[i][j] == self.opp and abs(row - i) == 1 and abs(col - j) == 1:
                                opp_distance_sum += 1
                            elif state[i][j] == self.opp:
                                col_distance = abs(col - j)
                                row_distance = abs(row - i)
                                # consider diagonal move when calculating distance
                                opp_distance_sum += min(col_distance, row_distance) + abs(col_distance - row_distance)

        # 50% of the combined heuristic score will be distance score, the other 50% will be the matching score.
        # deal with zero division error
        if my_distance_sum == 0:
            my_score_max = (my_score_max/4)/2
        else:
            my_score_max = (my_score_max/4 + 2/my_distance_sum)/2
        
        # deal with zero division error
        if opp_distance_sum == 0:
            opp_score_max = (opp_score_max/4)/2
        else:
            opp_score_max = (opp_score_max/4 + 2/opp_distance_sum)/2

        # return the combined heuristic score, if the opponent has a higher score, return a negative score
        if my_score_max > opp_score_max:
            return my_score_max
        else:
            return -opp_score_max

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
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
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
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
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
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

if __name__ == "__main__":
    main()
