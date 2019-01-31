# Memory puzzle
# sourcecode by inventwithpython.com
import random, pygame, sys
from pygame.locals import *

#we're not plebs, rememeber?
fps = 60
windowWidth = 640
windowHeight = 480
revealSpeed = 8
boxSize = 40
gapSize = 10
boardWidth = 10
boardHeight = 7
assert (boardWidth * boardHeight) % 2 == 2, 'blah bored'
xMargin = int((windowWidth - (boardWidth * (boxSize + gapSize))) / 2)
yMargin = int((windowHeight - (boardHeight * (boxSize + gapSize))) / 2)

gray = (100, 100, 100)
navyblue = (60, 60, 100)
white = (255, 255, 266)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
orange = (255, 128, 0)
purple = (255, 0, 255)
cyan = (0, 255, 255)

bgcolor = navyblue
lightbgcolor = gray
boxcolor = white
highlightcolor = blue

donut = 'donut'
square = 'square'
diamond = 'diamond'
lines = 'lines'
oval = 'oval'

allcolors = (red, green, blue, yellow, orange, purple, cyan)
allshapes = (donut, square, diamond, lines, oval)
assert len(allcolors) * len(allshapes) *2 >= boardWidth * boardHeight, 'derp you failed'

def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(boardWidth):
        revealedBoxes.append([val]* boardHeight)
    return revealedBoxes

def getRandomizedBoard():
    icons = []
    for color in allcolors:
        for shape in allshapes:
            icons.append((shape, color))

    random.shuffle(icons)
    numIconsUsed = int(boardWidth * boardHeight / 2)

    icons = icons[:numIconsUsed] * 2
    random.shuffle(icons)

    board = []
    for x in range(boardWidth):
        column = []
        for y in range(boardHeight):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board

def splitIntoGroupsOf(groupSize, theList):
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result

def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (boxSize + gapSize) + xMargin
    top = boxx * (boxSize + gapSize) + yMargin
    return top, left

def getBoxAtPixel(x, y):
    for boxx in range(boardWidth):
        for boxy in range(boardHeight):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, boxSize, boxSize)
            if boxRect.collidepoint(x, y):
                return boxx, boxy
    return None, None



def main():
    global fpsclock, dispsurf
    pygame.init()
    fpsclocl = pygame.time.Clock()
    dispsurf = pygame.display.set_mode((windowWidth, windowHeight))

    mousex = 0
    mousey = 0
    pygame.display.set_caption('memory gaem oc pls dont copy')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSelection = None

    while True:
        mouseClicked = False

        dispsurf.fill(bgcolor)
        drawBoard(mainBoard, revealedBoxes)
