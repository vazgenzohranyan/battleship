import pygame
import numpy as np
import copy
import os
from utils import generate_board
from pygame.locals import *

SCREEN_WIDTH = 400
SCREEN_LENGTH = 1000
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
GREY = [105,105,105]
FPSCLOCK = pygame.time.Clock()
SPLASH = True
BLUE = [0,0,255]
LIGHT_BLUE = [135,206,250]
BAR_X = SCREEN_LENGTH/2 - 100
BAR_Y = SCREEN_WIDTH/2 + 20
BANNER_X = SCREEN_LENGTH/2 - 150
BANNER_y = 2
PLAYER_BOARD = None
COMPUTER_BOARD = None
BOARD_CORNER_X = 200
BOARD_CORNER_y = 50
PARTICLE_WIDTH = 20
PARTICLE_HEIGHT = 20
COMPUTER_BOARD_X = SCREEN_LENGTH / 2 + 100
COMPUTER_BOARD_Y = 50
FOUND_SHIP = None

pygame.init()
screen = pygame.display.set_mode((SCREEN_LENGTH, SCREEN_WIDTH),HWSURFACE | DOUBLEBUF | RESIZABLE)
pygame.display.set_caption('Battleship')

bg = pygame.image.load(os.path.abspath('res/splash_background.jpg'))
splash_picture = pygame.transform.scale(bg, (SCREEN_LENGTH, SCREEN_WIDTH))

bg = pygame.image.load(os.path.abspath('res/background.png'))
picture = pygame.transform.scale(bg, (SCREEN_LENGTH, SCREEN_WIDTH))

banner = pygame.image.load(os.path.abspath('res/battleship_banner.png'))

new_game = pygame.image.load(os.path.abspath('res/new_game.png'))
help = pygame.image.load(os.path.abspath('res/help.png'))
exit = pygame.image.load(os.path.abspath('res/exit.png'))
menu = pygame.image.load(os.path.abspath('res/menu.png'))
start = pygame.image.load(os.path.abspath('res/start.png'))

ship_1_white = pygame.image.load(os.path.abspath('res/ship_1_white.png'))
ship_1_white = pygame.transform.scale(ship_1_white, (40, 40))

ship_2_white = pygame.image.load(os.path.abspath('res/ship_2_white.png'))
ship_2_white = pygame.transform.scale(ship_2_white, (40, 60))

ship_3_white = pygame.image.load(os.path.abspath('res/ship_3_white.png'))
ship_3_white = pygame.transform.scale(ship_3_white, (40, 80))

ship_4_white = pygame.image.load(os.path.abspath('res/ship_4_white.png'))
ship_4_white = pygame.transform.scale(ship_4_white, (40, 100))

BLOWUP_EXPLOSION = [
    pygame.image.load(os.path.abspath('res/blowup1.png')),
    pygame.image.load(os.path.abspath('res/blowup2.png')),
    pygame.image.load(os.path.abspath('res/blowup3.png')),
    pygame.image.load(os.path.abspath('res/blowup4.png')),
    pygame.image.load(os.path.abspath('res/blowup5.png')),
    pygame.image.load(os.path.abspath('res/blowup6.png'))
]

FAIL_EXPLOSION = [
    pygame.image.load(os.path.abspath('res/fail1.png')),
    pygame.image.load(os.path.abspath('res/fail2.png')),
    pygame.image.load(os.path.abspath('res/fail3.png')),
    pygame.image.load(os.path.abspath('res/fail4.png')),
    pygame.image.load(os.path.abspath('res/fail5.png')),
    pygame.image.load(os.path.abspath('res/fail6.png'))
]


def finish(player=None):
    Finish = True
    MENU_POS = (SCREEN_LENGTH / 2 - 100, BANNER_y + 300)
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    if player is False:
        victory_string = myfont.render('Congratulations, you win', True, WHITE)
    else:
        victory_string = myfont.render('Sorry, you lost', True, WHITE)

    while Finish:
        screen.blit(picture, (0, 0))
        screen.blit(menu, MENU_POS)
        screen.blit(victory_string, (SCREEN_LENGTH / 2 - 120 , 170) )
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type is QUIT:
                pygame.quit()
            elif event.type is MOUSEBUTTONDOWN and button_selector(event.pos, [MENU_POS], [menu.get_rect()[2:]]) is not None:
                main()
                Finish = False

def fight(player_board):
    PLAYER_BOARD = copy.deepcopy(player_board)
    COMPUTER_BOARD = make_computer_board()
    COMPUTER_BOARD_STATIC = copy.deepcopy(COMPUTER_BOARD)
    COMP = generate_board()
    Fight = True
    FOUND_SHIP = None
    turn = False
    count = 0
    START_NEW_GAME_POS = (SCREEN_LENGTH / 2 - 100, BANNER_y + 300)
    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    counter_title = myfont.render('Step counts', True, WHITE)

    while Fight:
        screen.blit(picture, (0, 0))
        draw_board(PLAYER_BOARD)
        draw_board(COMPUTER_BOARD)
        counter = myfont.render('{0}'.format(count), True, WHITE)

        screen.blit(new_game, START_NEW_GAME_POS)
        screen.blit(counter_title, (SCREEN_LENGTH / 2 -50, BANNER_y + 100))
        screen.blit(counter, (SCREEN_LENGTH / 2 , BANNER_y + 150))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type is QUIT:
                pygame.quit()
            elif event.type is MOUSEBUTTONDOWN:
                if button_selector(event.pos, [START_NEW_GAME_POS], [new_game.get_rect()[2:]]) is not None:
                    start_new_game()
                elif check_on_board(event.pos, COMPUTER_BOARD, PARTICLE_HEIGHT, PARTICLE_WIDTH) is not None and event.button == 1 and turn is False:
                    brd = check_on_board(event.pos, COMPUTER_BOARD, PARTICLE_HEIGHT, PARTICLE_WIDTH)
                    if turn is False:
                        if COMP[brd[0]][brd[1]] == 1:
                            friend = False
                            show_blowup_animation(COMPUTER_BOARD[brd[0]][brd[1]][1:])
                            COMPUTER_BOARD[brd[0]][brd[1]][0] = 3
                            COMP[brd[0]][brd[1]] = 0
                            positions, diagonals = find_neighboor_computer(COMPUTER_BOARD,brd)
                            for p in positions:
                                if COMP[p[0]][p[1]] == 1:
                                    friend = True
                                    draw_invalid_places(COMPUTER_BOARD, diagonals)
                                    break
                            if friend is False:
                                draw_invalid_places(COMPUTER_BOARD, diagonals + positions)
                            if check_finish_computer(COMP):
                                finish(player=False)
                            count += 1
                            COMPUTER_BOARD_STATIC = copy.deepcopy(COMPUTER_BOARD)

                        elif COMPUTER_BOARD_STATIC[brd[0]][brd[1]][0] is 0:
                            show_fail_animation(COMPUTER_BOARD[brd[0]][brd[1]][1:])
                            turn = True
                            pygame.display.flip()
                            COMPUTER_BOARD[brd[0]][brd[1]][0] = 1
                            COMPUTER_BOARD_STATIC = copy.deepcopy(COMPUTER_BOARD)

                            step = ai_turn(PLAYER_BOARD)
                            while step is not None:
                                draw_board(PLAYER_BOARD)
                                pygame.display.flip()
                                FPSCLOCK.tick(60)
                                if check_finish_player(PLAYER_BOARD):
                                    finish(player=True)
                                step = ai_turn(PLAYER_BOARD)

                            if check_finish_player(PLAYER_BOARD):
                                finish(player=True)
                            draw_board(PLAYER_BOARD)
                            pygame.display.flip()
                            turn = False


            elif event.type == MOUSEMOTION:
                brd = check_on_board(event.pos, COMPUTER_BOARD, PARTICLE_HEIGHT, PARTICLE_WIDTH)
                if brd is not None and COMPUTER_BOARD[brd[0]][brd[1]][0] is not 3:
                    COMPUTER_BOARD = copy.deepcopy(COMPUTER_BOARD_STATIC)
                    COMPUTER_BOARD[brd[0]][brd[1]][0] = 1
                else:
                    COMPUTER_BOARD = copy.deepcopy(COMPUTER_BOARD_STATIC)

def check_finish_computer(board):
    for raw in board:
        for p in raw:
            if p == 1:
                return False
    return True

def check_finish_player(board):
    for raw in board:
        for p in raw:
            if p[0] == 2:
                return False
    return True

def draw_invalid_places(board, positions):
    for p in positions:
        board[p[0]][p[1]][0] = 1

def find_neighboor_computer(board, pos, previous_pos=None):
    i,j = pos
    positions = []
    diagonals = []
    for n in range(i - 1, i + 2):
        for m in range(j - 1, j + 2):
            if m in range(10) and n in range(10) and [i,j] != [n,m]:
                if board[n][m][0] != 3 and board[n][m][0] != 1:
                    if i-n == 0 or j-m == 0:
                        positions.append([n,m])
                    else:
                        diagonals.append([n,m])
                elif board[n][m][0] == 3 and [n,m] != previous_pos:
                    ps, _ = find_neighboor_computer(board, [n,m], previous_pos=pos)
                    positions = positions + ps

    return positions, diagonals

def ai_turn(board):
    particle = None
    particle_posses = []
    index = None
    selected_particle = None
    for i,raw in enumerate(board):
        for j,p in enumerate(raw):
            if p[0] == 3 and particle is None:
                poss = []
                for n in range(i - 1, i + 2):
                    for m in range(j - 1, j + 2):
                        if m in range(10) and n in range(10) and [i, j] != [n, m]:
                            if board[n][m][0] != 3 and board[n][m][0] != 1:
                                poss.append([n,m])
                if len(poss) != 0:
                    particle = p
                    particle_posses = poss.copy()
                    break
    if particle is not None:
        index = np.random.randint(0, len(particle_posses))
        selected_particle = particle_posses[index]
    else:
        particle_posses = []
        for i,raw in enumerate(board):
            for j,p in enumerate(raw):
                if p[0] == 0 or p[0] == 2:
                    particle_posses.append([i,j])
        index = np.random.randint(0,len(particle_posses))
        selected_particle = particle_posses[index]
    if board[selected_particle[0]][selected_particle[1]][0] == 2:
        show_blowup_animation(board[selected_particle[0]][selected_particle[1]][1:])
        FPSCLOCK.tick(5)
        board[selected_particle[0]][selected_particle[1]][0] = 3
        pss, diagonals = find_neighboor_computer(board, selected_particle)
        for p in pss:
            if board[p[0]][p[1]][0] is 2:
                draw_invalid_places(board, diagonals)
                positions, _ = find_neighboor_computer(board, p)
                if positions == []:
                    return None
                else:
                    return p
        draw_invalid_places(board, diagonals + pss)
        return 2
    elif board[selected_particle[0]][selected_particle[1]][0] == 0:
        show_fail_animation(board[selected_particle[0]][selected_particle[1]][1:])
        board[selected_particle[0]][selected_particle[1]][0] = 1
        return None

def show_blowup_animation(pos):
    for image in BLOWUP_EXPLOSION:
        image = pygame.transform.scale(image, (PARTICLE_WIDTH, PARTICLE_HEIGHT))
        screen.blit(image, pos)
        pygame.display.flip()
        FPSCLOCK.tick(20)


def show_fail_animation(pos):
    for image in FAIL_EXPLOSION:
        image = pygame.transform.scale(image, (PARTICLE_WIDTH, PARTICLE_HEIGHT))
        screen.blit(image, pos)
        pygame.display.flip()
        FPSCLOCK.tick(20)

def make_computer_board():
    board = [[] for _ in range(10)]
    for i in range(10):
        for j in range(10):
            board[i].append([0, COMPUTER_BOARD_X + i * (PARTICLE_HEIGHT + 2), COMPUTER_BOARD_Y + j * (PARTICLE_WIDTH + 2)])
    return board

def start_new_game():
    counters = [4,3,2,1]
    CONSTRUCT_BOARD = make_board()
    BOARD = copy.deepcopy(CONSTRUCT_BOARD)
    new_game_starting = True
    MENU_POS = (SCREEN_LENGTH / 2 - 100, BANNER_y + 300)
    START_POS = (SCREEN_LENGTH / 2 + 200, BANNER_y + 300)

    myfont = pygame.font.SysFont('Comic Sans MS', 30)
    textsurface = myfont.render('Please construct your board', True, WHITE)
    SHIP_1_POS = (SCREEN_LENGTH / 2 - textsurface.get_rect()[2] + 300, SCREEN_WIDTH / 2 - textsurface.get_rect()[3])
    SHIP_2_POS = (SCREEN_LENGTH / 2 - textsurface.get_rect()[2] + 350, SCREEN_WIDTH / 2 - textsurface.get_rect()[3])
    SHIP_3_POS = (SCREEN_LENGTH / 2 - textsurface.get_rect()[2] + 400, SCREEN_WIDTH / 2 - textsurface.get_rect()[3])
    SHIP_4_POS = (SCREEN_LENGTH / 2 - textsurface.get_rect()[2] + 450, SCREEN_WIDTH / 2 - textsurface.get_rect()[3])

    selected_ship = None
    vertical = True

    while new_game_starting:
        ship_1_c = myfont.render('{0}'.format(counters[0]), True, WHITE)
        ship_2_c = myfont.render('{0}'.format(counters[1]), True, WHITE)
        ship_3_c = myfont.render('{0}'.format(counters[2]), True, WHITE)
        ship_4_c = myfont.render('{0}'.format(counters[3]), True, WHITE)

        screen.blit(picture, (0, 0))
        draw_board(BOARD)
        screen.blit(menu, MENU_POS)
        if max(counters) == 0:
            screen.blit(start, START_POS)


        screen.blit(textsurface,
                    (SCREEN_LENGTH / 2 - textsurface.get_rect()[2] + 300, SCREEN_WIDTH / 2 - textsurface.get_rect()[3] - 100))

        screen.blit(ship_1_white, SHIP_1_POS)
        screen.blit(ship_2_white, SHIP_2_POS)
        screen.blit(ship_3_white, SHIP_3_POS)
        screen.blit(ship_4_white, SHIP_4_POS)
        screen.blit(ship_1_c, (SCREEN_LENGTH / 2 - textsurface.get_rect()[2] + 315, SCREEN_WIDTH / 2 - textsurface.get_rect()[3] - 25))
        screen.blit(ship_2_c, (SCREEN_LENGTH / 2 - textsurface.get_rect()[2] + 365, SCREEN_WIDTH / 2 - textsurface.get_rect()[3] - 25))
        screen.blit(ship_3_c, (SCREEN_LENGTH / 2 - textsurface.get_rect()[2] + 415, SCREEN_WIDTH / 2 - textsurface.get_rect()[3] - 25))
        screen.blit(ship_4_c, (SCREEN_LENGTH / 2 - textsurface.get_rect()[2] + 465, SCREEN_WIDTH / 2 - textsurface.get_rect()[3] - 25))


        pygame.display.flip()

        for event in pygame.event.get():
            if event.type is QUIT:
                pygame.quit()
            elif event.type is MOUSEBUTTONDOWN and button_selector(event.pos, [MENU_POS], [menu.get_rect()[2:]]) is not None:
                main()
                new_game_starting = False
            elif event.type is MOUSEBUTTONDOWN and button_selector(event.pos, [START_POS],
                                                                       [start.get_rect()[2:]]) is not None and max(counters)==0:
                    fight(CONSTRUCT_BOARD)
                    new_game_starting = False
            elif event.type is MOUSEBUTTONDOWN:
                brd = check_on_board(event.pos, CONSTRUCT_BOARD, PARTICLE_HEIGHT, PARTICLE_WIDTH)
                if brd is not None:
                    if selected_ship is not None:
                        if event.button == 3:
                            vertical = not vertical
                        elif event.button == 1:
                            if check_valid_ship(CONSTRUCT_BOARD, BOARD) is not None:
                                counters[selected_ship-1] -= 1
                                selected_ship = None
                                for raw in BOARD:
                                    for p in raw:
                                        if p[0] == 1:
                                            p[0] = 2
                                CONSTRUCT_BOARD = copy.deepcopy(BOARD)
                    else:
                        pos = copy.deepcopy(brd)
                        CONSTRUCT_BOARD = copy.deepcopy(BOARD)
                        positions = find_ship(CONSTRUCT_BOARD,pos)
                        if len(positions) is not 0:
                            counters[len(positions)-1] += 1
                            for p in positions:
                                BOARD[p[0]][p[1]][0] = 0
                            CONSTRUCT_BOARD = copy.deepcopy(BOARD)

                button = button_selector(event.pos, [SHIP_1_POS,SHIP_2_POS,SHIP_3_POS,SHIP_4_POS], [ship_1_white.get_rect()[2:],
                                                                                                    ship_2_white.get_rect()[2:],
                                                                                                    ship_3_white.get_rect()[2:],
                                                                                                    ship_4_white.get_rect()[2:]])
                if button is not None:
                    if button + 1 == selected_ship:
                        selected_ship = None
                    elif counters[button] is not 0:
                        selected_ship = button + 1

            elif event.type == MOUSEMOTION:
                brd = check_on_board(event.pos, CONSTRUCT_BOARD, PARTICLE_HEIGHT, PARTICLE_WIDTH)
                if brd is not None:
                    if selected_ship is not None:
                        if vertical:
                            x,y = brd
                            les = 9 - x - selected_ship + 1
                            if les<= 0:
                                x += les
                            BOARD = copy.deepcopy(CONSTRUCT_BOARD)
                            for i in range(x, x+selected_ship):
                                BOARD[i][y][0] = 1
                        else:
                            x, y = brd
                            les = 9 - y - selected_ship + 1
                            if les <= 0:
                                y += les
                            BOARD = copy.deepcopy(CONSTRUCT_BOARD)
                            for i in range(y, y + selected_ship):
                                BOARD[x][i][0] = 1
                else:
                    BOARD = copy.deepcopy(CONSTRUCT_BOARD)

def check_on_board(mouse_postion, board, h, w):
    for i,raw in enumerate(board):
        for j,p in enumerate(raw):
            if p[1] + h >= mouse_postion[0] >= p[1] and p[2] + w >=mouse_postion[1] >= p[2]:
                return [i,j]
    return None


def find_ship(board, pos):
    brd = copy.deepcopy(board)
    positions = []
    if brd[pos[0]][pos[1]][0] == 2:
        for _ in range(4):
            nb = find_neighboor(brd, pos)
            if nb is not None:
                positions.append(nb)
                brd[nb[0]][nb[1]][0] = 0
                pos = copy.deepcopy(nb)
    return positions


def find_neighboor(board, pos):
    i,j = pos
    for n in range(i - 1, i + 2):
        for m in range(j - 1, j + 2):
            if m in range(10) and n in range(10) and board[n][m][0] == 2:
                return [n,m]
    return None

def check_valid_ship(board1, board2):
    for i,raw in enumerate(board2):
        for j,p in enumerate(raw):
            if p[0] == 1:
                for m in range(i-1,i+2):
                    for n in range(j-1,j+2):
                        if m in range(10) and n in range(10) and board1[m][n][0] == 2:
                            return None

    return 1


def draw_shadow(positions, h, w):
    for p in positions:
        pygame.draw.rect(screen, GREY, (p[1], p[2], w, h))


def draw_board(board):
    for i,raw in enumerate(board):
        for j,p in enumerate(raw):
            if p[0] == 0:
                pygame.draw.rect(screen, WHITE, (p[1],p[2], PARTICLE_WIDTH, PARTICLE_HEIGHT))
            elif p[0] ==1:
                pygame.draw.rect(screen, GREY, (p[1],p[2], PARTICLE_WIDTH, PARTICLE_HEIGHT))
            elif p[0] ==2:
                pygame.draw.rect(screen, LIGHT_BLUE, (p[1],p[2], PARTICLE_WIDTH, PARTICLE_HEIGHT))
            elif p[0] == 3:
                pygame.draw.rect(screen, BLACK, (p[1],p[2], PARTICLE_WIDTH, PARTICLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (board[0][0][1]-2, board[0][0][2]-2, (PARTICLE_WIDTH + 2)*10 +2, (PARTICLE_HEIGHT+2)*10 + 2), 1)


def splash_screen(canSplash):
    i = 0
    screen.blit(splash_picture, (0,0))
    position = splash_picture.get_rect()
    pygame.display.flip()
    loading = pygame.image.load('res/loading.png')
    loading = pygame.transform.scale(loading,(60,60))

    while canSplash:
        for event in pygame.event.get():
            if event.type is QUIT:
                pygame.quit()
        screen.blit(splash_picture, (0, 0))
        screen.blit(loading, (BAR_X + 5*i, BAR_Y + 30))
        pygame.display.flip()
        FPSCLOCK.tick(10)
        i += 1
        if i == 30:
            canSplash = False

    for i in range(30):
        position = position.move((0,i))
        screen.blit(picture, (0, 0))
        screen.blit(splash_picture, position)
        pygame.display.update()
        pygame.time.delay(10)


def make_board():
    board = [[] for _ in range(10)]
    for i in range(10):
        for j in range(10):
            board[i].append([0, BOARD_CORNER_X + i*(PARTICLE_HEIGHT + 2), BOARD_CORNER_y + j*(PARTICLE_WIDTH + 2)])
    return board


def button_selector(mouse_postion, button_positions, button_sizes):
    for i, button in enumerate(button_positions):
        if button[0] + button_sizes[i][0] >= mouse_postion[0] >= button[0] and button[1] + button_sizes[i][1] >= mouse_postion[1] >= button[1]:
            return i
    return None


def check_for_click(pos, size):
    for event in pygame.event.get():
        if event.type is MOUSEBUTTONDOWN and button_selector(event.pos, [pos], [size]) is not None:
            return 1
        elif event.type == pygame.QUIT:
            pygame.quit()
    return None


def show_help():
    MENU_POS = (SCREEN_LENGTH / 2 - 100, BANNER_y + 300)
    myfont = pygame.font.SysFont('Comic Sans MS', 25)
    textsurface = myfont.render('Battleship is board game constructing to play with 2 players.', True, WHITE)
    textsurface_1 = myfont.render('First you need to place your ships with length 4,3,2,1.', True, WHITE)
    textsurface_2 = myfont.render('To do it use mouse keys.Left key for placing(selecting) and right for changing angle.', True, WHITE)
    textsurface_3 = myfont.render('In order to win you need to place them carefully.(Hint - place ships near to each other and wall).', True, WHITE)
    textsurface_4 = myfont.render('Then start attacking computer.If you beat part of board start finding other parts next to it untill you beat the whole ship.', True, WHITE)
    textsurface_5 = myfont.render('Wins player who first finds all the ships of opponent.', True, WHITE)
    screen.blit(picture, (0, 0))
    screen.blit(textsurface, (SCREEN_LENGTH/2 - textsurface.get_rect()[2]/2, 30+textsurface.get_rect()[3]))
    screen.blit(textsurface_1, (SCREEN_LENGTH/2 - textsurface_1.get_rect()[2]/2,30+ 2*textsurface.get_rect()[3]))
    screen.blit(textsurface_2, (SCREEN_LENGTH/2 - textsurface_2.get_rect()[2]/2, 30+3*textsurface.get_rect()[3]))
    screen.blit(textsurface_3, (SCREEN_LENGTH/2 - textsurface_3.get_rect()[2]/2, 30+4*textsurface.get_rect()[3]))
    screen.blit(textsurface_4, (SCREEN_LENGTH/2 - textsurface_4.get_rect()[2]/2, 30+5*textsurface.get_rect()[3]))
    screen.blit(textsurface_5, (SCREEN_LENGTH/2 - textsurface_5.get_rect()[2]/2, 30+6*textsurface.get_rect()[3]))
    pygame.display.flip()
    screen.blit(menu, MENU_POS)
    pygame.display.flip()

    while check_for_click(MENU_POS, menu.get_rect()[2:]) is None:
        pygame.display.update()
        FPSCLOCK.tick()

    main()


def main():
    a = True
    while a:
        NEW_GAME_POS = (SCREEN_LENGTH / 2 - 100, BANNER_y + 170)
        HELP_POS = (SCREEN_LENGTH / 2 - 100, BANNER_y + 230)
        EXIT_POS = (SCREEN_LENGTH / 2 - 100, BANNER_y + 300)

        sur = pygame.transform.scale(banner, (300, 150))
        screen.blit(sur, (BANNER_X, BANNER_y))
        pygame.display.flip()

        screen.blit(picture, (0, 0))
        screen.blit(new_game, NEW_GAME_POS)
        screen.blit(help, HELP_POS)
        screen.blit(exit, EXIT_POS)

        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            button = button_selector(event.pos, [NEW_GAME_POS,HELP_POS,EXIT_POS],[new_game.get_rect()[2:],
                                                                         help.get_rect()[2:],
                                                                         exit.get_rect()[2:]])
            if button == 0:
                start_new_game()
                a = False
            elif button == 1:
                show_help()
                a = False
            elif button == 2:
                pygame.quit()

def start_game():
    splash = True
    while splash:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()

        splash_screen(SPLASH)
        splash = False
    main()


if __name__ == "__main__":
    start_game()


