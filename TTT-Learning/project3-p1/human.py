import random

class Human:
   
   symbol = 'X'
   
   def __init__( self, xORo ):
      self.symbol = xORo
      print("Ready to play Tic-Tac-Toe?\nYou'll be playing the ",xORo," pieces.\n")
   
   def showboard( self, gameboard ):
      # show current board state
      for i in range(9):
         if gameboard[i] == "-":
            gameboard = gameboard[:i] + chr(48+i) + gameboard[i+1:]
      print( "Current board : enter index of selected space" )
      print( gameboard[0:3] )
      print( gameboard[3:6] )
      print( gameboard[6:9] )
      print( "" )
   
   def getMove( self, gameboard ):
      self.showboard(gameboard)
      # get available move
      move = int(input("Where do you want to play? "))
      while move < 0 or move > 8 or gameboard[move] == "X" or gameboard[move] == "O":
              move = int(input("Invalid move. Try again: "))
      return move
         
   def endGame( self, status, gameboard ):
      
      # learn from the result... ?
      if status == 1: 
         # you won the game
         p = 1
      elif status == -1:
         # you lost the game
         p = -1
      else: # status == 0
         # no winner
         p = 0
