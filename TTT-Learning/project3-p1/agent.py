import random
from os.path import exists

class Agent:

   lfactor = .5
   ldecay = .5

   kb = []
   gamesteps = []
   dChances = [.11, .11, .11, .11, .11, .11, .11, .11, .11]

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

         for x in range(9): #make taken spots unreachable 
            if gameboard[x] != '-': 
               temp[x+1] = -1
         self.kb.append(temp)
      
      # Decide where to play
      for i in self.kb:
         if i[0] == gameboard:     #find the gameboard in kb 
            options = []
            canChoose = False

            while canChoose == False:  #loop and reroll until there are options to pick from 
               p = random.uniform(0,1)
               #print(p)
               j = 1
               while j < len(i):
                  if p < i[j]:
                     canChoose = True
                     options.append(j)
                  j += 1
            #print(options)
            choice = random.choice(options)     #make a choice between those that the p value was under
            self.gamesteps.append(gameboard)    #add board and choice taken to gamesteps
            self.gamesteps.append(choice)

            return choice-1


   def endGame( self, status, gameboard ):
      # learn from the result
      if status == 1: 
         # you won the game
         factor = self.lfactor
         m = len(self.gamesteps)-1

         while m >= 0: 
            state = self.gamesteps[m]    #current step
            if(isinstance(state, str)):   
               chose = self.gamesteps[m+1]   #spot chosen
               for i in self.kb:
                  if i[0] == state:     #find the gameboard in kb 
                     factor *= self.ldecay
                     diff = (i[chose] - (i[chose] + (i[chose] * factor)) )*-1   #the difference taken will be spread across the other possible choices   
                     i[chose] = i[chose] + (i[chose] * factor)         #subtract a percentage of the current value
                     if i[chose] > 1: 
                        i[chose] = 1
                     
                     

                     c = 1
                     optCount = 0
                     while c < len(i):    #find total other options in order to split the remaining num 
                        if i[c] != -1 and c != chose: 
                           optCount += 1
                        c += 1

                     c = 1
                     while c < len(i):    #go to these options and increase them 
                        if i[c] != -1 and c != chose: 
                           i[c] -= diff / optCount
                           if(i[c] < .000006):
                              i[c] = 0
                        c += 1

            m = m - 1

         self.gamesteps = []
      elif status == -1:
         # you lost the game
         factor = self.lfactor
         m = len(self.gamesteps)-1

         while m >= 0: 
            state = self.gamesteps[m]    #current step
            if(isinstance(state, str)):   
               chose = self.gamesteps[m+1]   #spot chosen
               for i in self.kb:
                  if i[0] == state:     #find the gameboard in kb 
                     diff = i[chose] - (i[chose] - (i[chose] * factor))    #the difference taken will be spread across the other possible choices   
                     i[chose] = i[chose] - (i[chose] * factor)         #subtract a percentage of the current value
                     if i[chose] < 0.00006: 
                        i[chose] = 0
                     
                     factor *= self.ldecay

                     c = 1
                     optCount = 0
                     while c < len(i):    #find total other options in order to split the remaining num 
                        if i[c] != -1 and c != chose: 
                           optCount += 1
                        c += 1

                     c = 1
                     while c < len(i):    #go to these options and increase them 
                        if i[c] != -1 and c != chose: 
                           i[c] += diff / optCount
                           if(i[c] > 1):
                              i[c] = 1
                        c += 1

            m = m - 1
            
         self.gamesteps = []
      else: # status == 0
         # no winner
         self.gamesteps = []


   #update knowledge base file 
   def stopPlaying(self):
      with open(self.datafile, 'w') as file: 
         for x in self.kb: 
            file.write(x[0] + ', ')

            for i in x[1:len(x)-1]: 
               file.write(str(i) + ', ')
            file.write(str(x[len(x)-1])+'\n')
            
            # print(x)
      # print(self.gamesteps)
      return
