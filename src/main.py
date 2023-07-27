import pygame
import random

colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]

start_fig = -2
y_fig = 12
dist_fig = 5
fig1_x = start_fig
fig2_x = start_fig + dist_fig
fig3_x = start_fig + 2 * dist_fig

class Figure:
    x = 0
    y = 0

    all_figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.all_figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.all_figures[self.type][self.rotation]

    def rotate(self):
        print("rotate the figure")
        print("+self type: " + str(self.type))
        print("+self rotation: " + str(self.rotation))
        self.rotation = (self.rotation + 1) % len(self.all_figures[self.type])
        print("-self type: " + str(self.type))
        print("-self rotation: " + str(self.rotation))


class Tetris:
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
                            j + self.figure.x < 0 : # if the figure is out of the field or intersects with another figure > 0 cause the color of the figure is > 0.                                
                            # print("i+self.figure.y = " + str(i+self.figure.y))
                            # print("j+self.figure.x = " + str(j+self.figure.x))
                            # print("self.field hmm = " + str(self.field[i + self.figure.y][j + self.figure.x]))
                            # print("field = " + str(i + self.figure.y) + " " + str(j + self.figure.x))
                        
                            intersection = True
        # print("fig = " + str(self.figure.x) + " " + str(self.figure.y))
        # print("self height = " + str(self.height))
        # print("self width = " + str(self.width))
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
                print("-----------------------------------------line is full------------------------------------------")
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
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
        # old_rotation = self.figures[param].rotation
        if self.figure != None:
            self.figure.rotate()
        # if self.intersects(param):
        #     print("intersects")
        #     self.figures[param].rotation = old_rotation
            


# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (400, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Nerb 1010! Game")

# Loop until the user clicks the close button.
game_height = 10
game_width = 10
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(game_height, game_width)
counter = 0
up = False
down = False
left = False
right  = False
ctrl = False
pressing_down = False
speed = 2

while not done:
    # print("counter: " + str(counter))
    if game.figures == []:
        a = game.new_figure()
        
    counter += 1
    if counter > 100000:
        counter = 0

    # if counter % (fps // game.level // 2) == 0 or pressing_down:
    #     if game.state == "start":
            # game.go_down()
    # pygame.time.wait(1000)
    if ctrl:
        if up:
            if counter % speed ==0:
                print("up")
                game.figure.y -= 1
        if down:
            if counter % speed ==0:
                print("down")
                game.figure.y += 1
        if left:
            if counter % speed ==0:
                print("left")
                game.figure.x -= 1
        if right:
            if counter % speed ==0:
                print("right")
                game.figure.x += 1
        
    for event in pygame.event.get():
    #  if the key is pressed down and hold it down
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                up = False
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                down = False
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                left = False
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                right = False
            elif event.key == pygame.K_LCTRL:
                ctrl = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                game.rotate()
            if event.key == pygame.K_q:
                pygame.quit()
            # UP DOWN LEFT RIGHT to be used for the movement of the figure
            if game.figure != None:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    up = True
                    game.figure.y -= 1    
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    down = True
                    game.figure.y += 1
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    left = True
                    game.figure.x -= 1
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    right = True
                    game.figure.x += 1
                elif event.key == pygame.K_LCTRL:
                    ctrl = True
                # if enter is pressed freeze the figure
                elif event.key == pygame.K_SPACE:
                    game.freeze()
                    game.figures[game.param] = None
                    # game.param = None
                    # game.figure = None
                    if game.figures[0] == None:
                        print("game.figures[0] is None")
                    if game.figures[0] == None and game.figures[1] == None and game.figures[2] == None:
                        game.new_figure()
                    else :
                        game.param = game.param + 1
                        game.figure = game.figures[game.param]
                        
            # if event.key == pygame.K_DOWN:
            #     pressing_down = True
            # if event.key == pygame.K_LEFT:
            #     game.go_side(-1)
            # if event.key == pygame.K_RIGHT:
            #     game.go_side(1)
            # if event.key == pygame.K_SPACE:
            #     game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(game_height, game_width)
        # if left click on mouse on the figure
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if mouse click on the area of the figure set the figure as selected and move the figure with the mouse movement 
            #  if the area is in game.figures[0] or game.figures[1] or game.figures[2]
            # set the figure as selected
            fig = -1
            tres_are = 3
            x1 = 60
            x2 = 340
            x = 93
            # if fig1_x + tres_are < pos[0] < fig1_x + tres_are 
            if 300 < pos[1] and pos[1] < 350 :
                print("y_fig")
                if x1 < pos[0] and pos[0] < x1 + x:
                    fig = 0
                elif x1 + x < pos[0] and pos[0] < x1 + 2 * x:
                    fig = 1
                elif x1 + 2 * x < pos[0] and pos[0] < x1 + 3 * x:
                    fig = 2
            if fig != -1:
                print("fig = " + str(fig))
                game.figure_clicked(fig)
            
            # game.figure_clicked(0)
            # print("pos = " + str(pos))
            
            # game.figures_clicked(param)

    if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.fill(BLACK)

    # draw the grid
    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])
    # draw the all figures
    if game.figures != []:
        for i in range(len(game.figures)):
            if game.figures[i] != None:
                for j in range(4):
                    for k in range(4):
                        p = j * 4 + k
                        if p in game.figures[i].image():
                            pygame.draw.rect(screen, colors[game.figures[i].color],
                                            [game.x + game.zoom * (k + game.figures[i].x) + 1,
                                            game.y + game.zoom * (j + game.figures[i].y) + 1,
                                            game.zoom - 2, game.zoom - 2])

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("Score: " + str(game.score), True, WHITE)
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

    screen.blit(text, [0, 0])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()