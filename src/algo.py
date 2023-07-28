# algorithm of the game with expectiminimax
import random
import copy

def expectiminimax(game, depth, maximizing_player):
    if depth == 0 or game.state == "gameover":
        return evaluate_state(game)

    if maximizing_player:
        max_eval = float('-inf')
        for i in range(len(game.figures)):
            if game.figures[i] is not None:
                for move in all_posibilities_place(game, i):
                    temp_field = temp_freeze(game, game.figures[i], move[1], move[2])
                    game.figures[i].x, game.figures[i].y = move[1], move[2]
                    game.figures[i].rotation = move[0]
                    eval = expectiminimax(game, depth - 1, False)
                    max_eval = max(max_eval, eval)
                    # game.field = temp_field  # Undo the move
        return max_eval
    else:
        chance_nodes = 0
        sum_eval = 0
        for i in range(len(game.figures)):
            if game.figures[i] is not None:
                for move in all_posibilities_place(game, i):
                    temp_field = temp_freeze(game, game.figures[i], move[1], move[2])
                    game.figures[i].x, game.figures[i].y = move[1], move[2]
                    game.figures[i].rotation = move[0]
                    eval = expectiminimax(game, depth - 1, True)
                    chance_nodes += 1
                    sum_eval += eval
                    # game.field = temp_field  # Undo the move
        return sum_eval / chance_nodes if chance_nodes != 0 else 0

def best_move(game):
    game_temp = copy.deepcopy(game)
    best_score = float('-inf')
    best_move = None
    for i in range(len(game_temp.figures)):
        if game_temp.figures[i] is not None:
            for move in all_posibilities_place(game_temp, i):
                print ("len = " + str(len(all_posibilities_place(game_temp, i))))
                temp_field = temp_freeze(game_temp, game_temp.figures[i], move[1], move[2])
                game_temp.figures[i].x, game_temp.figures[i].y = move[1], move[2]
                game_temp.figures[i].rotation = move[0]
                eval = expectiminimax(game_temp, 2, False)
                # game_temp.field = temp_field  # Undo the move

                if eval > best_score:
                    best_score = eval
                    best_move = move

    return best_move

def evaluate_state(game):
    # Define your heuristic evaluation function here (same as before)
    return game.score + len(game.empty_place())

def all_posibilities_place(game, idx):
    empty_place = game.empty_place()
    all_posibilities_place = []
    if game.figures[idx] is not None:
        for j in range(len(empty_place)):
            for k in range(len(game.figures[idx].all_figures[game.figures[idx].type])):
                game.figures[idx].rotation = k
                game.figures[idx].x = empty_place[j][0]
                game.figures[idx].y = empty_place[j][1]
                if game.can_be_freeze():
                    all_posibilities_place.append([k, empty_place[j][0], empty_place[j][1]])
    return all_posibilities_place

def temp_freeze(game, figure, x, y):
    temp_field = game.field
    # print("u temp_field = " + str(game.field))
    for i in range(4):
        for j in range(4):
            if i * 4 + j in figure.image():
                try:
                    if temp_field[i + y][j + x] != 0:
                        return None
                    else:
                        temp_field[i + y][j + x] = figure.color
                except IndexError:
                    return None
    return temp_field