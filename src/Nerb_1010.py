from Figure import *

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

    def new_figure(self):
        # add three figures
        self.figures = [Figure(fig1_x, y_fig), Figure(fig2_x, y_fig), Figure(fig3_x, y_fig)]
        self.figure = self.figures[0]
        self.param = 0
    
    # def convert_mouse_pos_to_figure(self, pos) -> int:
    #     return pos[0] // self.zoom, pos[1] // self.zoom

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
        print("intersects")
        intersection = False
        if self.figure is not None:
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in self.figure.image():
                        print("self.field[{}][{}] === {}".format(i + self.figure.y, j + self.figure.x, self.figure.color))
                        # print(self.field[i + self.figure.y][j + self.figure.x] != 0)
                        if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 : 
                            intersection = True
        print("field = " + str(self.field))
        return intersection
        

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0: # if the line is full
                print("---------line is full-----------")
                lines += 1
                # fill the line with black color
                for ji in range(self.width):
                    self.field[i][ji] = 0
                # for i1 in range(i, 1, -1):
                #     for j in range(self.width):
                #         self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figures.y += 1
        self.figures.y -= 1
        self.freeze()

    def go_down(self):
        self.figures.y += 1
        if self.intersects():
            self.figures.y -= 1
            self.freeze()

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

    def go_side(self, dx):
        old_x = self.figures.x
        self.figures.x += dx
        if self.intersects():
            self.figures.x = old_x

    def rotate(self):
        if self.figure != None:
            self.figure.rotate()