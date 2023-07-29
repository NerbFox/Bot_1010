import random
import copy
import numpy as np
# greedy 
def best_move(game, pos_figures): # pos_figures = [(figure, pos), (figure, pos), (figure, pos)]
    # game_temp = copy.deepcopy(game)
    best_score = -1
    bet_move = pos_figures[0]
    game_temp = game
    for i, pos_figure in enumerate(pos_figures):
        score = score_field(temp_freeze(game_temp, pos_figure[1]))
        # update the score of the figure
        pos_figures[i][2] = score
        if score > best_score:
            best_score = score
            bet_move = pos_figure
    # return pos_figures[np.argmax(pos_figures[:, 2])]
    return bet_move

# return a score of the field
def score_field(field):
    lines = 0
    for i in range(len(field)):
        if 0 not in field[i]:
            lines += 1
            field[i] = [0] * len(field[i])

    score = lines ** 2
    return score

def temp_freeze(game, figure):
    temp_field = copy.deepcopy(game.field)
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



# for pos_figure in pos_figures:
#         temp_field = temp_freeze(game_temp, pos_figure[1])
#         # pos_figure[0].x, pos_figure[0].y = pos_figure[1].x, pos_figure[1].y
#         # pos_figure[0].rotation = pos_figure[1].rotation
#         game_temp.field = temp_field # Undo the move
#         eval = expectiminimax(game_temp, 2, False)
#         if eval > best_score:
#             best_score = eval
#             best_move = pos_figure
#     return best_move

# def expectiminimax(game, depth, is_chance):
#     if game.field is None:
#         print("game field is None")
#         return 0
#     if depth == 0:
#         # print("game field: " + str(game.field))
#         return game.score_field(game.field)

#     if is_chance:
#         total_score = 0
#         total_possibilities = 0
#         pos_figures = game.all_posibilities_place()

#         for pos_figure in pos_figures:
#             temp_field = temp_freeze(game, pos_figure[1])
#             # pos_figure[0].x, pos_figure[0].y = pos_figure[1].x, pos_figure[1].y
#             # pos_figure[0].rotation = pos_figure[1].rotation
#             # game.field = temp_field

#             # if game.can_place_figure(pos_figure[0]):
#             if temp_field is not None:
#                 game.field = temp_field
#                 total_possibilities += 1
#                 total_score += expectiminimax(game, depth - 1, False)

#         return total_score / (1 if total_possibilities == 0 else total_possibilities)

#     else:
#         min_score = float('inf')
#         pos_figures = game.all_posibilities_place()

#         for pos_figure in pos_figures:
#             temp_field = temp_freeze(game, pos_figure[1])
#             # pos_figure[0].x, pos_figure[0].y = pos_figure[1].x, pos_figure[1].y
#             # pos_figure[0].rotation = pos_figure[1].rotation
#             if temp_field is not None:
#                 game.field = temp_field

#                 # if game.can_place_figure(pos_figure[0]):
#                 # game.freeze()
#                 score = expectiminimax(game, depth - 1, True)

#                 if score < min_score:
#                     min_score = score

#         return min_score