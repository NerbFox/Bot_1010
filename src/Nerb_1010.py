from Figure import *
from pygame_vars import *
import copy
from algo import *
import numpy as np
import pygame
from constants import * 
# import os
minimum_value = 0

# all_posibilities_figure is all figure type and rotation
all_posibilities_figure = []
figure_temp = Figure(0, 0)
number_type = figure_temp.get_number_type()
for i in range(number_type):
    figure_temp.type = i
    number_rotation = figure_temp.get_number_rotation()
    for j in range(number_rotation):
        figure_temp.rotation = j
        all_posibilities_figure.append(copy.deepcopy(figure_temp))
# print("len(all_posibilities_figure) = " + str(len(all_posibilities_figure)))
# for figure in all_posibilities_figure:
#     print("figure.type = " + str(figure.type) + ", figure.rotation = " + str(figure.rotation))

class Nerb_1010:
    def __init__(self, height, width):
        self.level = 2
        self.score = 0
        self.state = "start"
        self.field = []
        self.height = 0
        self.width = 0
        self.param = 0
        self.x = 100
        self.y = 60
        self.zoom = 20
        self.figures = []
        self.figure = None
    
        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)
            
        self.total_types_figure = [0 for i in range(number_type)]
        self.play_sound(start_sound)
        self.play_sound_channel(background_sound, 0.2, -1, channel2)

    def play_sound(self, file_sound, volume=0.7, loop=1):
        pygame.mixer.music.load(file_sound)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loop, 0.0, 0)
    
    def play_sound_channel(self, file_sound, volume=0.7, loop=1, channel=channel1):
        # play sound on channel 1 by default
        sound = pygame.mixer.Sound(file_sound)
        channel.play(sound, loop)
        channel.set_volume(volume)
    
    def new_figure(self):
        # add three figures
        self.figures = [Figure(fig1_x, y_fig), Figure(fig2_x, y_fig), Figure(fig3_x, y_fig)]
        self.figure = self.figures[0]
        self.param = 0
        # update the total types figure
        for i in range(len(self.figures)):
            self.total_types_figure[self.figures[i].type] += 1
        # print("self.total_types_figure = " + str(self.total_types_figure))

    def figure_clicked(self, param):
        self.figure = self.figures[param]
        self.param = param
        # self.rotate(param)
        # bring the figure move with the mouse movement
        # pos = pygame.mouse.get_pos()
        # print("figure {} with x = {} and y = {} is clicked".format(param, self.figures[param].x, self.figures[param].y))
        # print("pos = " + str(pos))
        # posi = self.convert_mouse_pos_to_figure(pos)
        # self.figures[param].x = posi[0]
        # self.figures[param].y = posi[1]
        
    def intersects(self):
        # print("intersects")
        intersection = False
        if self.figure is not None:
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in self.figure.image():
                        # print("self.field[{}][{}] === {}".format(i + self.figure.y, j + self.figure.x, self.figure.color))
                        # print(self.field[i + self.figure.y][j + self.figure.x] != 0)
                        if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 : 
                            intersection = True
        # print("field = " + str(self.field))
        return intersection  

    def break_lines(self):
        lines = 0
        for i in range(self.height): 
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0: # if the line is full
                # print("---------line is full-----------")
                # play a sound
                self.play_sound(success_sound)
                lines += 1
                # fill the line with black color
                for ji in range(self.width):
                    self.field[i][ji] = 0
                # for i1 in range(i, 1, -1):
                #     for j in range(self.width):
                #         self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    try :
                        # check if the field already has a figure
                        if self.field[i + self.figure.y][j + self.figure.x] != 0:
                            self.state = "gameover"
                        else:
                            self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
                    except IndexError:
                        self.state = "gameover"
        self.break_lines()
        if self.intersects():
            self.state = "gameover"
        if self.state == "gameover":
            self.play_sound(game_over_sound)
            
    def can_be_freeze(self):       
        temp_field = copy.deepcopy(self.field)
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    try :
                        if self.field[i + self.figure.y][j + self.figure.x] != 0:
                            self.field = copy.deepcopy(temp_field)
                            return False
                        # else:
                        #     self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
                    except IndexError:
                        self.field = copy.deepcopy(temp_field)
                        return False
        if self.intersects():
            self.field = copy.deepcopy(temp_field)
            return False
        self.field = copy.deepcopy(temp_field)
        return True

    def rotate(self):
        if self.figure != None:
            self.figure.rotate()
    
    def ai_move(self):
        # Use is_there_a_place function to check if there is a valid move for each figure
        # print("ai_move")
        b, pos_figures = self.is_there_a_place()
        if b :
            print("--bot moves--")
            # i, fig, _= best_move(self, pos_figures)
            i, fig, _= best_move(self, pos_figures, all_posibilities_figure, self.total_types_figure)
            # for i in range(len(pos_figures)):
            #     print("pos_figures[{}] = {}".format(i, pos_figures[i]))
            # print all pos figure that in first tuple of element is 0
            
            # print("pos_figures[0] = " + str(pos_figures[0]))
            # i, fig, _ = copy.deepcopy(pos_figures[0])
            self.figure = fig
            self.freeze()
            self.figures[i] = None
            # print("i = " + str(i))
            # print("x, y = " + str(self.figure.x) + ", " + str(self.figure.y))
            if self.figures[0] == None and self.figures[1] == None and self.figures[2] == None:
                self.new_figure()
                # print("new figure")
        
        # move = best_move(self)
        # if move == None:
        #     # self.state = "gameover"
        #     print("The AI has reached a dead end")
        #     print("It is time to start a new game")
        #     self.state = "gameover"
        #     return
        # self.figure.rotation = move[0]
        # self.figure.x = move[1]
        # self.figure.y = move[2]
        # self.freeze()
        # for i in range (len(self.figures)):
        #     if self.figures[i] != None:
        #         if self.figures[i].x == self.figure.x and self.figures[i].y == self.figure.y:
        #             self.figures[i] = None
        # if self.figures[0] == None and self.figures[1] == None and self.figures[2] == None:
        #     self.new_figure()
        #     print("new figure")
        
    # return empty place in the field
    def empty_place(self): 
        empty_place = [] 
        for i in range(self.height):
            for j in range(self.width):
                if self.field[i][j] == 0:
                    empty_place.append([j-1, i-1])
        # print("empty_place = " + str(empty_place))
        return empty_place
    
    def can_place_figure(self, figure):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in figure.image():
                    try:
                        if (
                            i + figure.y >= self.height
                            or j + figure.x >= self.width
                            or j + figure.x < 0
                            or self.field[i + figure.y][j + figure.x] != 0
                        ):
                            return False
                    except IndexError:
                        return False
        return True

    def all_posibilities_place(self):
        empty_place = self.empty_place()
        # print("len(empty_place) = " + str(len(empty_place)) )
        # all_posibilities_place = []
        # array of array of [figure_idx, figure, score] 2 dimension
        all_posibilities_place = np.array([[0, Figure(0, 0), 0]])
        # # erase the first element
        all_posibilities_place = np.delete(all_posibilities_place, 0, 0)
        for i in range(len(self.figures)):
            if self.figures[i] is not None:  # if the figure is not None
                figure_copy = copy.deepcopy(self.figures[i])
                for j in range(len(empty_place)):
                    # rotation
                    for k in range(len(figure_copy.all_figures[figure_copy.type])):
                        figure_copy.rotation = k
                        figure_copy.x = empty_place[j][0]
                        figure_copy.y = empty_place[j][1]
                        if self.can_place_figure(figure_copy):
                            # all_posibilities_place.append([i, copy.deepcopy(figure_copy), 0])
                            all_posibilities_place = np.append(all_posibilities_place, np.array([[i, copy.deepcopy(figure_copy), minimum_value]]), axis=0)
        return all_posibilities_place

    def is_there_a_place(self):
        all_place = self.all_posibilities_place()
        if len(all_place) != 0:
            return True, all_place
        else:
            return False, all_place
    
    
    # def all_posibilities_place(self): 
    #     empty_place = copy.deepcopy(self.empty_place())
    #     all_posibilities_place = []
    #     for i in range(len(self.figures)):
    #         if self.figures[i] != None: # if the figure is not None
    #             self.figure = copy.deepcopy(self.figures[i])
    #             for j in range(len(empty_place)):
    #                 # rotation 
    #                 for k in range(len(self.figure.all_figures[self.figure.type])):
    #                     self.figure.rotation = k
    #                     self.figure.x = empty_place[j][0]
    #                     self.figure.y = empty_place[j][1]
    #                     if self.can_be_freeze():
    #                         # all_posibilities_place.append([i, empty_place[j][0], empty_place[j][1]])
    #                         all_posibilities_place.append([i, self.figure])
    #     return all_posibilities_place

    # # check if there is a figure from figures that can be moved to the field
    # def is_there_a_place(self):
    #     all_place = self.all_posibilities_place()
    #     if all_place != []:
    #         return True, all_place
    #     else:
    #         return False, all_place
    
    
    
    
    # def find_best_move(self, figure, empty_places):
    #     best_move = None
    #     best_score = float("-inf")

    #     for rotation in range(len(figure.all_figures[figure.type])):
    #         for x, y in empty_places:
    #             temp_game = copy.deepcopy(self)
    #             temp_game.figure = copy.deepcopy(figure)
    #             temp_game.figure.rotation = rotation
    #             temp_game.figure.x, temp_game.figure.y = x, y

    #             if temp_game.can_be_freeze():
    #                 temp_game.freeze()
    #                 score = temp_game.score_field(temp_game.field)
    #                 if score > best_score:
    #                     best_score = score
    #                     best_move = (rotation, x, y)

    #     return best_move

    # def is_there_a_place(self):
    #     empty_places = self.empty_place()
    #     pos_figures = []

    #     for i, figure in enumerate(self.figures):
    #         if figure is not None:
    #             best_move = self.find_best_move(figure, empty_places)
    #             if best_move is not None:
    #                 pos_figures.append((i, figure))

    #     return len(pos_figures) > 0, pos_figures