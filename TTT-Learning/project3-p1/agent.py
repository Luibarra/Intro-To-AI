import random
from os.path import exists

class Agent:

   lFactor = .5
   ldecay = .2

   kb = []
   gamesteps = []
   dChances = [0.11,0.11,0.11,0.11,0.11,0.11,0.11,0.11,0.11]

   symbol = 'X'
   datafile = ''
   
   def __init__( self, xORo ):
      self.symbol = xORo
      # create data file if it doesn't exist
      if(xORo == 'X'): 
         self.datafile = 'learningdata/X-Data.txt'
         if( not exists('learningdata/X-Data.txt')):
            open('learningdata/X-Data.txt', 'x')
         else:
            with open(self.datafile) as textFile:
               for line in textFile:
                  x = [item.strip() for item in line.split(',')]
                  i = 1
                  while(i < len(x)):
                     x[i] = float(x[i])
                     i += 1
                  
                  self.kb.append(x)
         # print(self.kb)

      elif(xORo == 'O'): 
         self.datafile = 'learningdata/O-Data.txt'
         if( not exists('learningdata/O-Data.txt')): 
            open('learningdata/O-Data.txt', 'x')
         else:
            with open(self.datafile) as textFile:
               for line in textFile:
                  x = [item.strip() for item in line.split(',')]
                  i = 1
                  while(i < len(x)):
                     x[i] = float(x[i])
                     i += 1
                  
                  self.kb.append(x)
         # print(self.kb)
      
   def getMove( self, gameboard ):
      saved = False
      self.gamesteps.append(gameboard)
      temp = [gameboard]

      #check if cur gameboard is saved
      for x in self.kb:
         if gameboard in x:
            saved = True
            break
      #add unknown board to kb 
      if not saved:  
         for x in self.dChances: #add default probabilities 
            temp.append(x)
         self.kb.append(temp)
      
      # Decide where to play
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

   #update knowledge base file 
   def stopPlaying(self):
      with open(self.datafile, 'w') as file: 
         for x in self.kb: 
            file.write(x[0] + ', ')
            
            for i in x[1:len(x)-1]: 
               file.write(str(i) + ', ')
            file.write(str(x[len(x)-1])+'\n')
            
            # print(x)

      return
