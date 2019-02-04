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
assert (boardWidth * boardHeight) % 2 == 0, 'blah bored'
xMargin = int((windowWidth - (boardWidth * (boxSize + gapSize))) / 2)
yMargin = int((windowHeight - (boardHeight * (boxSize + gapSize))) / 2)

gray = (100, 100, 100)
navyblue = (60, 60, 100)
white = (255, 255, 255)
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


def main():
    global fpsclock, dispsurf
    pygame.init()
    fpsclock = pygame.time.Clock()
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

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx is not None and boxy is not None:
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True
                if firstSelection is None:
                    firstSelection = (boxx, boxy)
                else:
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)

                    if icon1shape != icon2shape or icon1color != icon2color:
                        pygame.time.wait(1000)
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes):
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)

                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealedBoxesData(False)
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        startGameAnimation(mainBoard)
                    firstSelection = None

        pygame.display.update()
        fpsclock.tick(fps)


def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(boardWidth):
        revealedBoxes.append([val] * boardHeight)
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


def drawIcon(shape, color, boxx, boxy):
    quarter = int(boxSize * 0.25)
    half = int(boxSize * 0.5)

    left, top = leftTopCoordsOfBox(boxx, boxy)

    if shape == donut:
        pygame.draw.circle(dispsurf, color, (left+half, top+half), half - 5)
        pygame.draw.circle(dispsurf, bgcolor, (left+half, top+half), quarter - 5) #TODO: check if not working with the sourcecode
    elif shape == square:
        pygame.draw.rect(dispsurf, color, (left + quarter, top + quarter, boxSize - half, boxSize - half))
    elif shape == diamond:
        pygame.draw.polygon(dispsurf, color, ((left + half, top), (left + boxSize - 1, top + half), (left + half, top + boxSize - 1), (left, top + half)))
    elif shape == lines:
        for i in range (0, boxSize, 4):
            pygame.draw.line(dispsurf, color, (left, top + i), (left + i, top))
            pygame.draw.line(dispsurf, color, (left + i, top + boxSize - 1), (left + boxSize - 1, top + i))
    elif shape == oval:
        pygame.draw.ellipse(dispsurf, color, (left, top + quarter, boxSize, half))


def getShapeAndColor(board, boxx, boxy):
    return board[boxx][boxy][0], board[boxx][boxy][1]

def drawBoxCovers(board, boxes, coverage):
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(dispsurf, bgcolor, (left, top, boxSize, boxSize))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0:
            pygame.draw.rect(dispsurf, boxcolor, (left, top, coverage, boxSize))
    pygame.display.update()
    fpsclock.tick(fps)


def revealBoxesAnimation(board, boxesToReveal):
    for coverage in range(boxSize, (-revealSpeed)-1, - revealSpeed):
        drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesToCover):
    for coverage in range(0, boxSize + revealSpeed, revealSpeed):
        drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(board, revealed):
    for boxx in range(boardWidth):
        for boxy in range(boardHeight):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                pygame.draw.rect(dispsurf, boxcolor, (left, top, boxSize, boxSize))
            else:
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(dispsurf, highlightcolor, (left - 5, top - 5, boxSize + 10, boxSize + 10), 4)


def startGameAnimation(board):
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(boardWidth):
        for y in range(boardHeight):
            boxes.append((x, y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)
    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


def gameWonAnimation(board):
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = lightbgcolor
    color2 = bgcolor
    for i in range(13):
        color1, color2 = color2, color1
        dispsurf.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)


def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False
    return True


if __name__ == '__main__':
    main()