import unittest
from Connect4 import *

class Connect4Test(unittest.TestCase):

        def testSeveralMethodsToShowSomeBehavior(self):
            player1 = "John"
            player2 = "Jane"
            game = Connect4(player1, player2)
            game.makeMove(player1, 4)
            game.makeMove(player2, 4)
            game.makeMove(player1, 4)
            game.makeMove(player2, 4)
            game.makeMove(player1, 4)
            self.assertFalse(game.columnIsFull(4))
            game.makeMove(player2, 4)
            self.assertTrue(game.columnIsFull(4))
            # No one won
            self.assertFalse(game.checkWin())
            # Many columns available still
            self.assertFalse(game.boardIsFull())
            # __str__ should now return the output shown in comments
            print(game)
'''
>>> 
- - - - O - - 
- - - - X - - 
- - - - O - - 
- - - - X - - 
- - - - O - - 
- - - - X - -  
'''
            
if __name__ == '__main__':
    try: unittest.main()
    except SystemExit: pass  
