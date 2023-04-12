from agent import Agent
from randomplayer import RandomPlayer
import random

def printBoard( board, status ):
   if status == 0: # tie game
      print( 'Tie game - no winner' )
   elif status == 1: # player 1 wins (numbers)
      print( 'Player 1 wins (numbers)' )
   else: # status = 2
      print( 'Player 2 wins (letters)' )
   print( board[0:3] )
   print( board[3:6] )
   print( board[6:9] )
   print( "" )

def transformBoard( board ):
   for i in range(9):
      if board[i].isdigit():
         board = board[:i] + 'X' + board[i+1:]
      elif board[i].isalpha():
         board = board[:i] + 'O' + board[i+1:]
   return board

def checkWin( board ):
   global gameover
   
   b = transformBoard(board)

   # not worth checking just from piece played, since only 8 win conditions
   over = (( b[0] != '-' and b[0] == b[1] and b[1] == b[2]) # top row
       or ( b[3] != '-' and b[3] == b[4] and b[4] == b[5] ) # mid row
       or ( b[6] != '-' and b[6] == b[7] and b[7] == b[8] ) # bot row
       or ( b[0] != '-' and b[0] == b[3] and b[3] == b[6] ) # lef col
       or ( b[1] != '-' and b[1] == b[4] and b[4] == b[7] ) # mid col
       or ( b[2] != '-' and b[2] == b[5] and b[5] == b[8] ) # rig col
       or ( b[6] != '-' and b[6] == b[4] and b[4] == b[2] ) # slash
       or ( b[0] != '-' and b[0] == b[4] and b[4] == b[8] )); # backslash
   gameover = over
   return over

def checkTie( board ):
   global gameover
   
   for i in range(9):
      if board[i] == '-':
         return False
   
   gameover = True
   return True

# global variables
gameboard = "---------"
gameover = False

A = RandomPlayer('X')
B = Agent('O')

numWinA = 0
numWinB = 0
numTied = 0

for g in range(100):
   # reset global variables
   gameboard = "---------"
   gameover = False
   
   # play game until done
   move = 1
   while( not gameover ):

      # player A : X, numbers
      play = -1
      b = transformBoard(gameboard)
      while( play < 0 or play > 8 or gameboard[play] != '-' ):
         play = A.getMove( b ) # get valid move
      gameboard = gameboard[:play] + chr(ord('0')+move) + gameboard[play+1:]
   #   print "received " + chr(ord('0') + play) + " : " + chr(ord('0')+move)

      if( checkWin(gameboard) ): 
         # A just won
         b = transformBoard(gameboard)
         A.endGame(1,b)
         B.endGame(-1,b)
         #printBoard(gameboard,1) # player 1 wins
         numWinA = numWinA + 1
      elif( checkTie(gameboard) ):
         # tie game
         b = transformBoard(gameboard)
         A.endGame(0,b)
         B.endGame(0,b)
         #printBoard(gameboard,0)
         numTied = numTied + 1
      
      if gameover: 
         continue
         
      # player B : O, letters
      play = -1
      b = transformBoard(gameboard)
      while( play < 0 or play > 8 or gameboard[play] != '-' ):
         play = B.getMove( b ) # get valid move
      gameboard = gameboard[:play] + chr( ord('A') + move - 1 ) + gameboard[play+1:]
   #   print "received " + chr(ord('0') + play) + " : " + chr( ord('A') + move - 1 )
      
      if( checkWin(gameboard) ): 
         # B just won
         b = transformBoard(gameboard)
         A.endGame(-1,b)
         B.endGame(1,b)
         numWinB = numWinB + 1
         #printBoard(gameboard,2) # player 2 wins
      elif( checkTie(gameboard) ):
         # tie game
         b = transformBoard(gameboard)
         A.endGame(0,b)
         B.endGame(0,b)
         #printBoard(gameboard,0)
         numTied = numTied + 1
         
      move = move + 1

A.stopPlaying()
B.stopPlaying()

print( "A   : " + str(numWinA)  + " games" )
print( "B   : " + str(numWinB)  + " games" )
print( "Tie : " + str(numTied)  + " games" )
