import pygame
import sys
from pygame.locals import *

pygame.init()

fps = 30
fpsClock = pygame.time.Clock()
board_h = 302
board_w = 302
line_w = 1
cell_size = 100
ds = pygame.display.set_mode((board_h, board_w), 0, 32)
colors = {
    'black': (0, 0, 0,),
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
}

mousex, mousey = 0, 0
turn = 'X'
haswon = False

def drawlines():
    pygame.draw.line(ds, colors['black'], (cell_size, 0), (cell_size, board_h), line_w)
    pygame.draw.line(ds, colors['black'], (cell_size*2, 0), (cell_size*2, board_h), line_w)
    pygame.draw.line(ds, colors['black'], (0, cell_size), (board_w, cell_size), line_w)
    pygame.draw.line(ds, colors['black'], (0, cell_size*2), (board_w, cell_size*2), line_w)


def makeboard():
    board = []
    for x in range(3):
        col = []
        for y in range(3):
            col.append('empty')
        board.append(col)
    return board


def drawcell(x, y, filling):
    if filling == 'empty':
        pygame.draw.rect(ds, colors['white'], (x, y, cell_size-(line_w*2), cell_size-(line_w*2)), 1)
    elif filling == 'X':
        pygame.draw.line(ds, colors['blue'], (x, y), (x + 100, y + 100), 3)
        pygame.draw.line(ds, colors['blue'], (x + 100, y), (x, y + 100), 3)
    elif filling == 'O':
        pygame.draw.circle(ds, colors['red'], (x + 50, y + 50), 40, 3)


def drawboard(board):
    for x in range(3):
        for y in range(3):
            drawcell(x*(cell_size-(line_w*2)), y*(cell_size-(line_w*2)), board[x][y])


def checkcell(x, y):
    for i in range(3):
        for j in range(3):
            cell = pygame.Rect(i*100, j*100, cell_size-(line_w*2), cell_size-(line_w*2))
            if cell.collidepoint(x, y):
                return i, j
    return None, None


def victory_text(won):
    fontObj = pygame.font.Font('freesansbold.ttf', 32)
    tf = fontObj.render('Победили '+won, True, colors['green'], colors['blue'])
    textRect = tf.get_rect()
    textRect.center = (151, 151)
    ds.blit(tf, textRect)


def checkvictory():
    if board[0][0]==board[1][0]==board[2][0] != 'empty':
        haswon = True
        if board[0][0]=='X':
            victory_text('X')
        else:
            victory_text('O')
    elif board[0][1] == board[1][1] == board[2][1] != 'empty':
        haswon = True
        if board[0][1]=='X':
            victory_text('X')
        else:
            victory_text('O')
    elif board[0][2] == board[1][2] == board[2][2] != 'empty':
        haswon = True
        if board[0][2]=='X':
            victory_text('X')
        else:
            victory_text('O')
    elif board[0][0] == board[0][1] == board[0][2] != 'empty':
        haswon = True
        if board[0][0]=='X':
            victory_text('X')
        else:
            victory_text('O')
    elif board[1][0] == board[1][1] == board[1][2] != 'empty':
        haswon = True
        if board[1][1]=='X':
            victory_text('X')
        else:
            victory_text('O')
    elif board[2][0] == board[2][1] == board[2][2] != 'empty':
        haswon = True
        if board[2][2]=='X':
            victory_text('X')
        else:
            victory_text('O')
    elif board[0][0] == board[1][1] == board[2][2] != 'empty':
        haswon = True
        if board[0][0]=='X':
            victory_text('X')
        else:
            victory_text('O')
    elif board[2][0] == board[1][1] == board[0][2] != 'empty':
        haswon = True
        if board[0][2]=='X':
            victory_text('X')
        else:
            victory_text('O')

board = makeboard()

while True:
    ds.fill(colors['white'])
    mouseclicked = False
    drawlines()
    drawboard(board)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
        elif event.type == MOUSEBUTTONUP:
            mousex, mousey = event.pos
            mouseclicked = True
            if haswon is True:
                board = makeboard()

    if mouseclicked and not haswon:
        x, y = checkcell(mousex, mousey)
        if board[x][y] == 'empty':
            board[x][y] = turn
            if turn == 'X':
                turn = 'O'
            else:
                turn = 'X'
    checkvictory()

    pygame.display.update()
    fpsClock.tick(fps)
