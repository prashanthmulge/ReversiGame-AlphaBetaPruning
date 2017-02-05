import math
import copy

file_read = open('input.txt', 'r')
file_write = open('output.txt', 'w')

player = file_read.readline().strip()
opponent = 'X'
if player == 'X':
    opponent = 'O'

depth = int(file_read.readline().strip())

depth_count = 0
board = []

pass_game = 0

for line in file_read:
    tree_list = list(line.strip())
    board.append(tree_list)

score_board = [[99, -8, 8, 6, 6, 8, -8, 99],
               [-8, -24, -4, -3, -3, -4, -24, -8],
               [8, -4, 7, 4, 4, 7, -4, 8],
               [6, -3, 4, 0, 0, 4, -3, 6],
               [6, -3, 4, 0, 0, 4, -3, 6],
               [8, -4, 7, 4, 4, 7, -4, 8],
               [-8, -24, -4, -3, -3, -4, -24, -8],
               [99, -8, 8, 6, 6, 8, -8, 99]
               ]


def map_fuc(value):
    i = int(value/8)
    return chr(96+(value%8)) + chr(49 + i)


def update_value(val):
    if val == -float('Inf'):
        val = "-Infinity"
    elif val == float('Inf'):
        val = "Infinity"
    return val


def print_fuc(value, d, v, alpha, beta):
    if value == "root":
        temp = "root"
        #print "root", d, v, alpha, beta
    elif value == "pass":
        temp = "pass"
        #print "pass", d, v, alpha, beta
    else:
        temp = map_fuc(value)
    v= update_value(v)
    alpha = update_value(alpha)
    beta = update_value(beta)
    print temp, d, v, alpha, beta


def evaluation(state, cur_player):
    val_cur = 0
    val_opp = 0
    for i in xrange(len(state)):
        for j in xrange(len(state[i])):
            if state[i][j] == cur_player:
                val_cur += score_board[i][j]
            elif state[i][j] != cur_player and state[i][j] != '*':
                val_opp += score_board[i][j]
    return val_cur - val_opp


def place_dict(plc, new_state, val):
    for i in xrange(8):
        if val in plc.keys():
            val += 64
        else:
            plc[val] = new_state
            break
    return plc


def generate_states(state, cur_player):
    plc = {}
    new_state = copy.deepcopy(state)
    opp_player = 'O'
    if cur_player == 'O':
        opp_player = 'X'
    for i in xrange(len(state)):
        for j in xrange(len(state[i])):

            # TODO: Handling when boundary is reached
            if state[i][j] == cur_player:
                # UP
                if i > 0 and state[i - 1][j] == opp_player:
                    for k in xrange(i - 1, -1, -1):
                        if state[k][j] == opp_player:
                            new_state[k][j] = cur_player
                        elif state[k][j] == cur_player:
                            break
                        else:
                            new_state[k][j] = cur_player
                            plc = place_dict(plc, new_state, k * 8 + j+ 1)
                            #plc[k * 8 + j + 1] = new_state
                            break
                    new_state = copy.deepcopy(state)
                # DOWN
                if (i + 1) < 8 and state[i + 1][j] == opp_player:
                    for k in xrange(i + 1, 8):
                        if state[k][j] == opp_player:
                            new_state[k][j] = cur_player
                        elif state[k][j] == cur_player:
                            break
                        else:
                            new_state[k][j] = cur_player
                            plc = place_dict(plc, new_state, k * 8 + j + 1)
                            #plc[k * 8 + j + 1] = new_state
                            break
                    new_state = copy.deepcopy(state)
                # LEFT
                if j > 0 and state[i][j - 1] == opp_player:
                    for k in xrange(j - 1, -1, -1):
                        if state[i][k] == opp_player:
                            new_state[i][k] = cur_player
                        elif state[i][k] == cur_player:
                            break
                        else:
                            new_state[i][k] = cur_player
                            plc = place_dict(plc, new_state, i * 8 + k + 1)
                            #plc[i * 8 + k + 1] = new_state
                            break
                    new_state = copy.deepcopy(state)
                # RIGHT
                if (j + 1) < 8 and state[i][j + 1] == opp_player:
                    for k in xrange(j + 1, 8):
                        if state[i][k] == opp_player:
                            new_state[i][k] = cur_player
                        elif state[i][k] == cur_player:
                            break
                        else:
                            new_state[i][k] = cur_player
                            plc = place_dict(plc, new_state, i * 8 + (k + 1))
                            #plc[i * 8 + (k + 1)] = new_state
                            break
                    new_state = copy.deepcopy(state)
                # DIAG LEFT TOP
                if i > 0 and j > 0 and state[i - 1][j - 1] == opp_player:
                    k = i - 1
                    m = j - 1
                    while k >= 0 and m >= 0:
                        if state[k][m] == opp_player:
                            new_state[k][m] = cur_player
                            k -= 1
                            m -= 1
                        elif state[k][m] == cur_player:
                            break
                        else:
                            new_state[k][m] = cur_player
                            plc = place_dict(plc, new_state, k * 8 + m + 1)
                            #plc[k * 8 + m + 1] = new_state
                            break
                    new_state = copy.deepcopy(state)

                # DIAG RIGHT TOP
                if (i + 1) < 8 and (j + 1) < 8 and state[i + 1][j + 1] == opp_player:
                    k = i + 1
                    m = j + 1
                    while k < 8 and m < 8:
                        if state[k][m] == opp_player:
                            new_state[k][m] = cur_player
                            k += 1
                            m += 1
                        elif state[k][m] == cur_player:
                            break
                        else:
                            new_state[k][m] = cur_player
                            plc = place_dict(plc, new_state, k * 8 + m + 1)
                            #plc[k * 8 + m + 1] = new_state
                            break
                    new_state = copy.deepcopy(state)

                # DIAG LEFT BOTTOM
                if (i + 1) < 8 and j > 0 and state[i + 1][j - 1] == opp_player:
                    k = i + 1
                    m = j - 1
                    while k < 8 and m >= 0:
                        if state[k][m] == opp_player:
                            new_state[k][m] = cur_player
                            k += 1
                            m -= 1
                        elif state[k][m] == cur_player:
                            break
                        else:
                            new_state[k][m] = cur_player
                            plc = place_dict(plc, new_state, k * 8 + m + 1)
                            #plc[k * 8 + m + 1] = new_state
                            break
                    new_state = copy.deepcopy(state)

                # DIAG RIGHT BOTTOM
                if i > 0 and (j + 1) < 8 and state[i - 1][j + 1] == opp_player:
                    k = i - 1
                    m = j + 1
                    while k >= 0 and m < 8:
                        if state[k][m] == opp_player:
                            new_state[k][m] = cur_player
                            k -= 1
                            m += 1
                        elif state[k][m] == cur_player:
                            break
                        else:
                            new_state[k][m] = cur_player
                            plc = place_dict(plc, new_state, k * 8 + m + 1)
                            #plc[k * 8 + m + 1] = new_state
                            break
                    new_state = copy.deepcopy(state)
    #plc.keys().sort()

    return plc


def Terminal_Test(state, actions_list):
    a = 0
    if depth == 0:
        return 1
    global pass_game

    if actions_list:
        # TODO: Handle pass
        pass_game = 0
        return 0
    else:
        if pass_game < 2:
            pass_game += 1
            return 0
        else:
            return 1


def MAX(a, b):
    if a > b:
        return a
    else:
        return b


def MIN(a, b):
    if a < b:
        return a
    else:
        return b


def Max_Value(value, state, alpha, beta):
    global depth
    global depth_count
    v = -float('Inf')

    action_list = generate_states(state, player)
    if Terminal_Test(state, action_list):
        v = evaluation(state, player)
        print_fuc(value, depth_count, v, alpha, beta)
        return v

    depth -= 1

    if pass_game == 1 or pass_game == 2:
        print_fuc(value, depth_count, v, alpha, beta)
        depth_count += 1
        #print "pass", depth_count, v, alpha, beta
        v = MAX(v, Min_Value("pass", state, alpha, beta))
        depth_count -= 1
        #print "pass", depth_count, v, alpha, beta
        if v >= beta:
            print_fuc(value, depth_count, v, alpha, beta)
            return v
        alpha = MAX(alpha, v)
        print_fuc(value, depth_count, v, alpha, beta)
        return v

    for a in sorted(action_list.keys()):

        key = a
        while True:
            print_fuc(value, depth_count, v, alpha, beta)
            depth_count += 1
            #print a, depth_count, v, alpha, beta
            v = MAX(v, Min_Value(a, action_list[key], alpha, beta))
            depth_count -= 1
            if v >= beta:
                print_fuc(value, depth_count, v, alpha, beta)
                return v
            alpha = MAX(alpha, v)

            del action_list[key]
            if (key + 64) in action_list.keys():
                key += 64
                continue
            else:
                break

        #print a, depth_count, v, alpha, beta

    print_fuc(value, depth_count, v, alpha, beta)
    return v


def Min_Value(value, state, alpha, beta):
    global depth
    global depth_count
    v = float('Inf')

    action_list = generate_states(state, opponent)
    if Terminal_Test(state, action_list):
        v = evaluation(state, player)
        print_fuc(value, depth_count, v, alpha, beta)
        return v

    depth -= 1

    if pass_game == 1 or pass_game == 2:
        print_fuc(value, depth_count, v, alpha, beta)
        depth_count += 1

        v = MIN(v, Max_Value("pass", state, alpha, beta))
        depth_count -= 1

        if v <= alpha:
            print_fuc(value, depth_count, v, alpha, beta)
            return v
        beta = MIN(beta, v)
        print_fuc(value, depth_count, v, alpha, beta)
        return v

    for a in sorted(action_list.keys()):

        key = a
        while True:
            print_fuc(value, depth_count, v, alpha, beta)
            depth_count += 1

            v = MIN(v, Max_Value(a, action_list[a], alpha, beta))
            depth_count -= 1
            if v <= alpha:
                print_fuc(value, depth_count, v, alpha, beta)
                return v
            beta = MIN(beta, v)
            del action_list[key]
            if (key + 64) in action_list.keys():
                key += 64
                continue
            else:
                break

    print_fuc(value, depth_count, v, alpha, beta)
    return v


def alpha_beta_pruning(state):
    global player
    print "Node,Depth,Value,Alpha,Beta"

    v = Max_Value("root", state, -float('Inf'), float('Inf'))

    action_list = generate_states(state, player)
    for s in action_list:
        if v == evaluation(action_list[s], player):
            for i in action_list:
                l = action_list[i]
                for lin in l:
                    print "".join(lin)+"\n"
    for lin in state:
        print "".join(lin)

alpha_beta_pruning(board)
