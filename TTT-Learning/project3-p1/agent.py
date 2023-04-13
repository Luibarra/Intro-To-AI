import random
from os.path import exists

class Agent:
   
   symbol = 'X'
   
   def __init__( self, xORo ):
      self.symbol = xORo

      if(xORo == 'X'): 
         if( not exists('learningdata/X-Data.txt')): 
            open('learningdata/X-Data.txt', 'x')
      elif(xORo == 'O'): 
         if( not exists('learningdata/O-Data.txt')): 
            open('learningdata/O-Data.txt', 'x')
               
   
   def getMove( self, gameboard ):
      # play in the next open space, looking from top corner
      for i in range(9):
         if gameboard[i] == "-":
            return i
         
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

   def stopPlaying():
      return
