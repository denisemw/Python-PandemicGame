class Connect4:

    def __init__(self, name1, name2):

        self.player1 = name1
        self.player2 = name2
        self.board = [['-', '-', '-', '-', '-', '-', '-'] for i in range(6)]
        self.rows = 6
        self.cols = 7
        self.won = False

    def makeMove(self, player, col):
        for row in range(self.rows-1, -1, -1):
            if self.board[row][col]=='-':
                if player==self.player1:
                    self.board[row][col] = 'X'
                else:
                    self.board[row][col] = 'O'
                return row
    
    def checkWin(self):
        return self.checkWinHorizontal() or self.checkWinVertical() or self.checkWinDiagonal()
        
    def checkWinHorizontal(self):
        for row in range(0, self.rows):
            for col in range(0, self.cols-3):
                if self.board[row][col]=='X' and self.board[row][col+1]=='X' and self.board[row][col+2]=='X' and self.board[row][col+3]=='X':
                    return True

                if self.board[row][col]=='O' and self.board[row][col+1]=='O' and self.board[row][col+2]=='O' and self.board[row][col+3]=='O':
                    return True
        return False

    def checkWinVertical(self):
        for row in range(0, self.rows-3):
            for col in range(0, self.cols):
                if self.board[row][col]=='X' and self.board[row+1][col]=='X' and self.board[row+2][col]=='X' and self.board[row+3][col]=='X':
                    return True

                if self.board[row][col]=='O' and self.board[row+1][col]=='O' and self.board[row+2][col]=='O' and self.board[row+3][col]=='O':
                    return True
        return False

    def checkWinDiagonal(self):
        # check upper left to lower right diagonal
        for r in range(self.rows-3):
            for c in range(self.cols-3):
                if self.board[r][c]=='X' and self.board[r+1][c+1]=='X' and self.board[r+2][c+2]=='X' and self.board[r+3][c+3]=='X':
                    print('yuuuuuuuup')
                    return True

                if self.board[r][c]=='O' and self.board[r+1][c+1]=='O' and self.board[r+2][c+2]=='O' and self.board[r+3][c+3]=='O':
                    return True
                
        # check upper right to lower left diagonal        
        for row in range(self.rows-3):
            for col in range(3, self.cols):
                if self.board[row][col]=='X' and self.board[row+1][col-1]=='X' and self.board[row+2][col-2]=='X' and self.board[row+3][col-3]=='X':
                    return True

                if self.board[row][col]=='O' and self.board[row+1][col-1]=='O' and self.board[row+2][col-2]=='O' and self.board[row+3][col-3]=='O':
                    return True
        return False


    def columnIsFull(self, column):
        return self.board[0][column] != '-'


    def boardIsFull(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == '-':
                    return False
        return True


    def __str__(self):
        boardStr = ''
        for row in range(len(self.board)):
            for col in range(7):
                boardStr += self.board[row][col] + ' '
            boardStr += '\n'
        return boardStr

def main():
    # get player names
    player1 = input("Player 1's name: ")
    player2 = input("Player 2's name: ")
    print()
    game = Connect4(player1, player2)
    print(game)

    # main game loop
    while not game.boardIsFull():

        # player 1 goes first
        print()
        col = int(input(player1 + "'s turn.\nEnter a column number to drop your piece: "))
        if col > 6 or col < 0 or game.columnIsFull(col):
            print("Invalid choice, you lose your turn.")
        else:
            game.makeMove(player1, col)
            print()
            print(game)
            # check if player 1 won of there is a tie
            if game.checkWin():
                print(player1 + " wins! :D")
            if game.boardIsFull():
                print("The board is full.  Tie Declared.")
        
        
        # player 2's turn
        print()
        col = int(input(player2 + "'s turn.\nEnter a column number to drop your piece: "))
        if col > 6 or col < 0 or game.columnIsFull(col):
            print("Invalid choice, you lose your turn.")
        else:
            game.makeMove(player2, col)
            print()
            print(game)
            # check if player 2 won or there is a tie
            if game.checkWin():
                print(player2 + " wins! :D")
                break
            if game.boardIsFull():
                print("The board is full.  Tie Declared.")
                break
        
if __name__=='__main__':
    main()
