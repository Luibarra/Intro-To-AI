import random

class RandomPlayer:
   
   symbol = 'X'
   
   def __init__( self, xORo ):
      self.symbol = xORo
   
   def getMove( self, gameboard ):
      # picks a random point, then cycles to the next available space
      m = random.randint(0,8)
      while( gameboard[m] != '-' ):
         m = ( m + 1 ) % 9
      return m
         
   def endGame( self, status, gameboard ):
      # a good agent would learn here
      status = status
