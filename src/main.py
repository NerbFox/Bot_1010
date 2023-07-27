from pygame_vars import *
from algo import *

# Loop until the user clicks the close button or 'q' is pressed
while not done:
    try:
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
        # print("Bot = " + str(Bot))
        if ctrl:
            if up:
                if counter % speed == 0:
                    print("up")
                    game.figure.y -= 1
            if down:
                if counter % speed == 0:
                    print("down")
                    game.figure.y += 1
            if left:
                if counter % speed == 0:
                    print("left")
                    game.figure.x -= 1
            if right:
                if counter % speed == 0:
                    print("right")
                    game.figure.x += 1
            
            
        for event in pygame.event.get():
        #  if the key is pressed down and hold it down
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL:
                    ctrl = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    up = False
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    down = False
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    left = False
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    right = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    game.rotate()
                if event.key == pygame.K_q:
                    pygame.quit()
                if event.key == pygame.K_LCTRL:
                    print("ctrl pressed")
                    ctrl = True
                if event.key == pygame.K_b:
                    print("B pressed")
                    if ctrl:
                        Bot = not Bot
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
                    # if enter is pressed freeze the figure
                    if event.key == pygame.K_SPACE:
                        game.freeze()
                        game.figures[game.param] = None
                        # game.param = None
                        # game.figure = None
                        if game.figures[0] == None:
                            print("game.figures[0] is None")
                        if game.figures[0] == None and game.figures[1] == None and game.figures[2] == None:
                            game.new_figure()
                        else :
                            game.param = (game.param + 1) % fig_options
                            while game.figures[game.param] == None:
                                game.param = (game.param + 1) % fig_options
                            game.figure = game.figures[game.param]
                            
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
        # if event.type == pygame.KEYUP:
        #         if event.key == pygame.K_DOWN:
        #             pressing_down = False
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
    except Exception as e:
        done = True
print("Thank you for playing Nerb 1010! Game")
print("Game Over")
print("Your score is: " + str(game.score))
pygame.quit()