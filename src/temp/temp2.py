

# total_types_figure = [0 for _ in range(7)]
# accuracies = []
# for i in range(15000):
#     for i in range(100):
#         typef = random.randint(0, 6)
#         total_types_figure[typef] += 1
#     next_3_types = predict_next_types(total_types_figure, num_predictions=3)
#     actual_next_3_types = []
#     for i in range(3):
#         typef = random.randint(0, 6)
#         total_types_figure[typef] += 1
#         actual_next_3_types.append(typef)
#     accuracy = sum([1 for i in range(3) if next_3_types[i] == actual_next_3_types[i]]) / 3
#     accuracies.append(accuracy)
# avg_accuracy = sum(accuracies) / len(accuracies)
# print("Average accuracy:", avg_accuracy)



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