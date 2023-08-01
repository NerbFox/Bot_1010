import random
import copy
import numpy as np

# predict_next_types function is used to predict the next types of the figures
def predict_next_types(total_types_figure, num_predictions=3):
    # Calculate the total number of types and their frequencies
    total_types = len(total_types_figure)
    total_freq = sum(total_types_figure)

    # Calculate the probability of each type
    type_probabilities = [freq / total_freq for freq in total_types_figure]

    # Generate the next types based on probabilities
    next_types = []
    for _ in range(num_predictions):
        next_type = random.choices(range(total_types), weights=type_probabilities)[0]
        next_types.append(next_type)
        # update type_probabilities
        total_types_figure[next_type] += 1
        total_freq += 1
        type_probabilities = [freq / (total_freq) for freq in total_types_figure]
    # next_types = random.choices(range(total_types), weights=type_probabilities, k=num_predictions)

    return next_types

# greedy with heuristic
def best_move(game, pos_figures, all_posibilities_figure, total_types_figure):
    # calculate the probability of getting each figure in the next 10 moves from the current position
    # all_p = []
    # next_figures = predict_next_types(total_types_figure, num_predictions=3)
    # for i in range(len(all_posibilities_figure)):
    #     for j in range(len(next_figures)):
    #         if all_posibilities_figure[i].type == next_figures[j]:
    #             all_p.append(all_posibilities_figure[i])
    best_score = -1
    best_move = pos_figures[0]
    game_temp = game
    for i, pos_figure in enumerate(pos_figures):
        temp_field = temp_freeze(game_temp.field, pos_figure[1])
        score = score_field(temp_field)
        # score_all_p = score_all_pos(all_p, game_temp)
        # score = max(score, score_all_p)
        # update the score of the figure
        pos_figures[i][2] = score
        if score > best_score:
            best_score = score
            best_move = pos_figure
    # return pos_figures[np.argmax(pos_figures[:, 2])]
    return best_move

# score_all_pos function is used to score all the possible positions of the figure
# but it consumes a lot of time and memory so it is not used
def score_all_pos(all_p, game_temp):
    game = copy.deepcopy(game_temp)
    temp_fielddd = copy.deepcopy(game.field)
    # game.figures = all_p
    # pos_figures = game.all_posibilities_place()
    width = len(temp_fielddd[0])
    height = len(temp_fielddd)
    best_score = -1
    for i in range(len(all_p)):
        # print("all_p{} x = ".format(i) + str(all_p[i].x))
        p = all_p[i]
        # for k in range(width):
        #     for l in range(height):
                # p.x = k
                # p.y = l
        try :
            temp_field = temp_freeze(temp_fielddd, p)
            score = score_field(temp_field)
        except :
            score = 0
        best_score = max(score, best_score)
    return best_score
  
# try to change the figure in figures
# cek ketersebaran zero in a row, sum it 
# ----0-0000
# ---0---000   2 + 2 + 1 + 1 = 6
# ---------0
# 0000000000

# -----00000
# ------0000   1 + 1 + 1 + 1 = 4  pilih ini 
# ---------0
# 0000000000

# Heuristic approach
# 1. the number of lines that can be formed (the more lines, the better)
# 2. the minimum number of zeroes in a row (the minimum zero in a row, the better)
# 3. the number of groups of zeroes in each row (the minimum number of groups, the better)

# score_field function is used to score the field
def score_field(field):
    lines = 0
    cols = len(field)
    rows = len(field[0])
    min_zeroes = cols
    sum_of_group_zeroes = 0
    for i in range(rows):
        # count the number of zeroes, and the number of groups of zeroes in a row
        zeroes = 0
        if field[i][0] == 0:
            sum_of_group_zeroes += 1
            zeroes += 1
        for j in range(1, cols):
            if field[i][j] == 0:
                zeroes += 1
                if field[i][j - 1] != 0:
                    sum_of_group_zeroes += 1
        min_zeroes = min(min_zeroes, zeroes)
        # if the line is full or there are no zeroes in the line, increment the lines
        if zeroes == 0:
            lines += 1
            
        # z = field[i].count(0)
        # min_zeroes = min(min_zeroes, z)
        # if z == 0:
        #     lines += 1
        
    # coba gausah score_all_pos + yg score rows gausah dikali atau ga diikutin aja
    score_lines = lines ** 2
    score_rows = rows - min_zeroes
    score_group_zeroes = rows*cols - sum_of_group_zeroes
    # score = score_lines * 3 * rows + score_rows 
    # score = rows*cols * score_lines * 3 + score_rows * rows + score_group_zeroes
    score = rows*cols * score_lines * 3 + score_group_zeroes
    return score

def temp_freeze(field, figure):  # change to field
    temp_field = copy.deepcopy(field)  # important to use deepcopy
    for i in range(4):
        for j in range(4):
            if i * 4 + j in figure.image():
                try:
                    if temp_field[i + figure.y][j + figure.x] != 0:
                        return None
                    else:
                        temp_field[i + figure.y][j + figure.x] = figure.type + 1
                except IndexError:
                    return None
    return temp_field