import heapq

def get_manhattan_distance(from_state, to_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    INPUT: 
        Two states (if second state is omitted then it is assumed that it is the goal state)

    RETURNS:
        A scalar that is the sum of Manhattan distances for all tiles.
    """
    distance = 0
    total_rows = 3
    total_columns = 3

    # consider the 1D array as a 3x3 matrix, calculate manhattan distance for each tile
    for from_state_row in range(total_rows):
        for from_state_column in range(total_columns):
            # read the tile number in from_state
            tile = from_state[from_state_row * 3 + from_state_column]
            # if the tile is not 0, calculate the manhattan distance
            if tile != 0:
                # calculate the position of that tile in to_state
                to_state_row = to_state.index(tile) // total_rows
                to_state_column = to_state.index(tile) % total_columns

                # calculate the manhattan distance
                distance += abs(from_state_row - to_state_row) + abs(from_state_column - to_state_column)

    return distance

def print_succ(state):
    """
    INPUT: 
        A state (list of length 9)

    WHAT IT DOES:
        Prints the list of all the valid successors in the puzzle. 
    """
    succ_states = get_succ(state)

    for succ_state in succ_states:
        print(succ_state, "h={}".format(get_manhattan_distance(succ_state)))


def get_succ(state):
    """
    INPUT: 
        A state (list of length 9), there is two empty tiles in the 3x3 puzzle, represented by 0.

    RETURNS:
        A list of all the valid successors in the puzzle (don't forget to sort the result as done below). 
    """
    total_columns = 3
    succ_states = []

    # find the position of the two empty tiles
    empty_tile1 = state.index(0)
    empty_tile2 = state.index(0, empty_tile1 + 1)
    empty_tiles = [empty_tile1, empty_tile2]

    # for each empty tile, generate their corresponding successors
    for empty_tile in empty_tiles:
        # if the empty tile can be moved up
        if empty_tile - total_columns >= 0 and state[empty_tile - total_columns] != 0:
            # create a copy of the current state
            new_state = state.copy()
            # swap the empty tile with the tile above it
            new_state[empty_tile] = new_state[empty_tile - total_columns]
            new_state[empty_tile - total_columns] = 0
            # add the new state to the list of successors
            succ_states.append(new_state)

        # if the empty tile can be moved down
        if empty_tile + total_columns < len(state) and state[empty_tile + total_columns] != 0:
            # create a copy of the current state
            new_state = state.copy()
            # swap the empty tile with the tile below it
            new_state[empty_tile] = new_state[empty_tile + total_columns]
            new_state[empty_tile + total_columns] = 0
            # add the new state to the list of successors
            succ_states.append(new_state)

        # if the empty tile can be moved left
        if empty_tile % total_columns != 0 and state[empty_tile - 1] != 0:
            # create a copy of the current state
            new_state = state.copy()
            # swap the empty tile with the tile to its left
            new_state[empty_tile] = new_state[empty_tile - 1]
            new_state[empty_tile - 1] = 0
            # add the new state to the list of successors
            succ_states.append(new_state)

        # if the empty tile can be moved right
        if empty_tile % total_columns != total_columns - 1 and state[empty_tile + 1] != 0:
            # create a copy of the current state
            new_state = state.copy()
            # swap the empty tile with the tile to its right
            new_state[empty_tile] = new_state[empty_tile + 1]
            new_state[empty_tile + 1] = 0
            # add the new state to the list of successors
            succ_states.append(new_state)

    return sorted(succ_states)

def solve(state, goal_state=[1, 2, 3, 4, 5, 6, 7, 0, 0]):
    """
    INPUT: 
        An initial state (list of length 9)

    WHAT IT SHOULD DO:
        Prints a path of configurations from initial state to goal state along  h values, number of moves, and max queue number in the format specified in the pdf.
    """
    
    # initialize the priority queue
    open_list = []
    closed_list = []
    # push the initial state in the format of heapq.heappush(pq ,(cost, state, (g, h, parent_index)))
    # cost = g + h
    # state = current state
    # g = number of moves from initial state to current state
    # h = heuristic value of current state
    heapq.heappush(open_list, (get_manhattan_distance(state), state, (0, get_manhattan_distance(state), -1)))
    # initialize the maximum length of the priority queue
    max_length = 1

    # while the priority queue is not empty
    while open_list:
        # pop the state with the lowest cost:
        current_state = heapq.heappop(open_list)
        # track current state index in closed list for reconstructing path
        current_state_index = len(closed_list)
        # add the current state to a list of visited states
        closed_list.append(current_state)

        # if the current state is the goal state, end the search loop
        if current_state[1] == goal_state:
            break

        # for each successor of the current state
        for successor in get_succ(current_state[1]):
            # calculate the number of moves from initial state to the successor
            g = current_state[2][0] + 1
            # calculate the heuristic value of the successor
            h = get_manhattan_distance(successor)
            # calculate the cost of the successor
            cost = g + h

            # if the successor is not in the priority queue or the list of visited states
            if successor not in [state[1] for state in open_list] and successor not in [state[1] for state in closed_list]:
                # push the successor to the priority queue
                heapq.heappush(open_list, (cost, successor, (g, h, current_state_index)))
                # track maximum length of the priority queue
                max_length = max(max_length, len(open_list))
            
            # if the successor is in the priority queue or the list of visited states
            if successor in [state[1] for state in open_list] or successor in [state[1] for state in closed_list]:
                # if the successor is in the priority queue
                if successor in [state[1] for state in open_list]:
                    successor_index = [state[1] for state in open_list].index(successor)
                    # if the new moves in the new successor is less than that in the priority queue
                    if g < open_list[successor_index][2][0]:
                        # push the successor to the priority queue
                        heapq.heappush(open_list, (cost, successor, (g, h, current_state_index)))
                        # track maximum length of the priority queue
                        max_length = max(max_length, len(open_list))

                # if the successor is in the list of visited states
                else:
                    successor_index = [state[1] for state in closed_list].index(successor)
                    if g < closed_list[successor_index][2][0]:
                        # push the successor to the priority queue
                        heapq.heappush(open_list, (cost, successor, (g, h, current_state_index)))
                        # track maximum length of the priority queue
                        max_length = max(max_length, len(open_list))

        # track maximum length of the priority queue at the end of the for loop
        max_length = max(max_length, len(open_list))

    # rebuild the path from the initial state to the goal state
    state_info_list = []
    while current_state[2][2] != -1:
        # add the current state to the list of states in the path
        state_info_list.append((current_state[1], current_state[2][1], current_state[2][0]))
        # get the parent state of the current state
        current_state = closed_list[current_state[2][2]]
    # add the initial state to the list of states in the path
    state_info_list.append((current_state[1], current_state[2][1], current_state[2][0]))
    # reverse the list of states in the path
    state_info_list.reverse()

    # This is a format helper.
    # build "state_info_list", for each "state_info" in the list, it contains "current_state", "h" and "move".
    # define and compute max length
    # it can help to avoid any potential format issue.
    for state_info in state_info_list:
        current_state = state_info[0]
        h = state_info[1]
        move = state_info[2]
        print(current_state, "h={}".format(h), "moves: {}".format(move))
    print("Max queue length: {}".format(max_length))

if __name__ == "__main__":
    """
    Feel free to write your own test code here to examine the correctness of your functions. 
    Note that this part will not be graded.
    """
    print_succ([2,5,1,4,0,6,7,0,3])
    print()

    print(get_manhattan_distance([2,5,1,4,0,6,7,0,3], [1, 2, 3, 4, 5, 6, 7, 0, 0]))
    print()

    solve([2,5,1,4,0,6,7,0,3])
    print()

    solve([4,3,0,5,1,6,7,2,0])
    print()

    solve([3, 4, 6, 0, 0, 1, 7, 2, 5])
    print()
    solve([6, 0, 0, 3, 5, 1, 7, 2, 4])
    print()
    solve([0, 4, 7, 1, 3, 0, 6, 2, 5])
    print()