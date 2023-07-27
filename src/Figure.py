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