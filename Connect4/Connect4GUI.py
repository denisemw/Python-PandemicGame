from graphics import *
from Connect4 import *
import time

OFFSET = 65

def pixelToXCoord(pixel):
    x = (pixel.getX() - OFFSET)//45
    return x


def main():

    win = GraphWin("Connect4",450,500)
    win.setBackground('blue')
    OFFSET = 65

    textX = 250
    textY = 500

    # initialize a 2D playing board
    for row in range(7):
        for col in range(6):
            i = row*45 + OFFSET
            j = col*45 + OFFSET
            rect = Rectangle(Point(i,j),Point(i+45,j + 45))
            rect.setFill('grey')
            rect.draw(win)
            circ = Circle(Point(i+22,j+22), 19)
            circ.setFill('blue')
            circ.draw(win)

    # draw title of game
    title = Text(Point(45*3+OFFSET + 22.5,OFFSET-30), 'Connect Four')
    title.setSize(16)
    title.draw(win)

    # board is set up

    # get user names
    entry1 = Entry(Point(3*45 + OFFSET + 22.5, 375), 35)
    entry1.setText('Player 1 name: ')
    entry1.draw(win)
    
    entry2 = Entry(Point(3*45 + OFFSET + 22.5, 375+30), 35)
    entry2.setText('Player 2 name: ')
    entry2.draw(win)

    cont = Text(Point(3*45 + OFFSET + 22.5, 375+70), "Please enter your names, and click to continue")
    cont.draw(win)
    
    win.getMouse()

    # get names from entry boxes
    name1 = entry1.getText()[15:]
    name2 = entry2.getText()[15:]

    if name1=='':
        name1 = 'Player 1'
    if name2=='':
        name2 = 'Player 2'
    
    entry1.undraw()
    entry2.undraw()
    cont.undraw()
    
    text = Text(Point(3*45 + OFFSET + 22.5, 375), "Welcome " + name1 + " and " + name2 + "!")
    text.draw(win)
    
    cont = Text(Point(3*45 + OFFSET + 22.5, 375+40), "Click to continue")
    cont.draw(win)
    
    game = Connect4(name1, name2)
    win.getMouse()
    text.undraw()
    cont.undraw()

    # main game loop
    while not game.boardIsFull():

        # player 1's turn
        play1Turn = Text(Point(3*45 + OFFSET + 22.5, 375), name1 + "'s turn:")
        play1Turn.setFill('red2')
        play1Turn.draw(win)
        
        colNumText = Text(Point(3*45 + OFFSET + 22.5, 375+30), "Click where you would like to drop your piece")
        colNumText.setFill('red2')
        colNumText.draw(win)
        
        coord = win.getMouse()
        col = pixelToXCoord(coord)
        if col > 6:
            col = 6
        if col < 0:
            col = 0
        row = game.makeMove(name1, col)
        
        circ = Circle(Point(col*45+OFFSET+22, OFFSET+22), 19)
        circ.setFill('red')
        circ.draw(win)

        # animate the red checker dropping
        for i in range((row+1)*2):
            circ.undraw()
            coord = i//2
            circ = Circle(Point(col*45+OFFSET+22, coord*45+OFFSET+22), 19)
            circ.setFill('red')
            circ.draw(win)
            time.sleep(.05)

        time.sleep(.3)
        play1Turn.undraw()
        colNumText.undraw()

        # check if player 1 won the game
        if game.checkWin():
            text = Text(Point(3*45 + OFFSET + 22.5, 375), name1 + " wins! :D")
            text.setFill('red')
            text.draw(win)
            break

        # player 2's turn
        play2Turn = Text(Point(3*45 + OFFSET + 22.5, 375), name2 + "'s turn:")
        play2Turn.setFill('black')
        play2Turn.draw(win)
        
        colNumText = Text(Point(3*45 + OFFSET + 22.5, 375+30), "Click where you would like to drop your piece")
        colNumText.setFill('black')
        colNumText.draw(win)
        
        coord = win.getMouse()
        col = pixelToXCoord(coord)
        if col > 6:
            col = 6
        if col < 0:
            col = 0
        row = game.makeMove(name2, col)
        
        circ = Circle(Point(col*45+OFFSET+22, 0*45+OFFSET+22), 19)
        circ.setFill('black')

        # animate the black checker dropping
        for i in range((row+1)*2):
            circ.undraw()
            coord = i//2
            circ = Circle(Point(col*45+OFFSET+22, coord*45+OFFSET+22), 19)
            circ.setFill('black')
            circ.draw(win)
            time.sleep(.05)

        time.sleep(.3)
        play2Turn.undraw()
        colNumText.undraw()

        # check if player 2 won the game
        if game.checkWin():
            text = Text(Point(3*45 + OFFSET + 22.5, 375), name2 + " wins! :D")
            text.setFill('black')
            text.draw(win)
            break

    # if the board is full and no one has 4 in a row, then it's a tie game
    if game.boardIsFull():
        text = Text(Point(3*45 + OFFSET + 22.5, 375), "Tie Game")
        text.draw(win)

    # close the window
    win.getMouse()
    win.close()
    
main()
