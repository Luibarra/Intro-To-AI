import random
from os.path import exists

#Functions decide if a move is valid.
def flips( board, index, piece, step ):
    other = ('X' if piece == 'O' else 'O')
    # is an opponent's piece in first spot that way?
    here = index + step
    if here < 0 or here >= 36 or board[here] != other:
        return False
        
    if( abs(step) == 1 ): # moving left or right along row
        while( here // 6 == index // 6 and board[here] == other ):
            here = here + step
        # are we still on the same row and did we find a matching endpiece?
        return( here // 6 == index // 6 and board[here] == piece )
    
    else: # moving up or down (possibly with left/right tilt)
        while( here >= 0 and here < 36 and board[here] == other ):
            here = here + step
        # are we still on the board and did we find a matching endpiece?
        return( here >= 0 and here < 36 and board[here] == piece ) 
def isValidMove( b, x, p ): # board, index, piece
    # invalid index
    if x < 0 or x >= 36:
        return False
    # space already occupied
    if b[x] != '-':
        return False 
    # otherwise, check for flipping pieces
    up    = x >= 12   # at least third row down
    down  = x <  24   # at least third row up
    left  = x % 6 > 1 # at least third column
    right = x % 6 < 4 # not past fourth column
    return (        left  and flips(b,x,p,-1)  # left
        or up   and left  and flips(b,x,p,-7)  # up/left
        or up             and flips(b,x,p,-6)  # up
        or up   and right and flips(b,x,p,-5)  # up/right
        or          right and flips(b,x,p, 1)  # right
        or down and right and flips(b,x,p, 7)  #down/right
        or down           and flips(b,x,p, 6)  # down
        or down and left  and flips(b,x,p, 5)) # down/left

class Agent:

    lfactor = .65
    ldecay = .85

    kb = []
    gamesteps = []
    dChances = []
    for i in range(36):
        dChances.append(.028)
    # print(dChances)
    #print(len(dChances))

    numOptions = 36
    symbol = 'O'
    datafile = ''

   #init files    
    def __init__( self, xORo ): 
        self.symbol = xORo
        print('loading kb')
        #~~~potentially put in x playable in the future~~~ would have to fix kb erase issue
        
        # create data file if it doesn't exist
        self.datafile = 'project3-p2/learningdata/O-Data.txt'
        if( not exists(self.datafile)): 
            open(self.datafile, 'x')
        else:   #if it already exists, put existing info into knowledge base
            with open(self.datafile) as textFile:
                for line in textFile:
                    x = [item.strip() for item in line.split(',')]
                    i = 1
                    while(i < len(x)):
                        x[i] = float(x[i])
                        i += 1
                    
                    self.kb.append(x)
            # print(self.kb)

    #use probabilties of board state to choose next move 
    def getMove( self, gameboard ):
        saved = False
        temp = [gameboard]

        #check if cur gameboard is saved
        for i in self.kb:
            if gameboard == i[0]:
                saved = True
                break
        #add unknown board to kb 
        if not saved:  
            for x in self.dChances: #add default probabilities 
                temp.append(x)

            for x in range(self.numOptions): #make taken spots unreachable 
                if not isValidMove(gameboard, x, 'O'): 
                    temp[x+1] = -1
            
            countSlot = 0
            for x in range(self.numOptions): #make taken spots unreachable 
                if gameboard[x] == '-':
                    countSlot += 1
            z = (1 / countSlot)   #create num chance to place in available slots

            index = 1
            while index < len(temp):  #put chances in temp
                if temp[index] != -1:
                    temp[index] = z
                index += 1

            self.kb.append(temp)    
        
        # Decide where to play
        for i in self.kb:
            if i[0] == gameboard:     #find the gameboard in kb 
                options = []
                choice = -1
                while not isValidMove( gameboard, choice, 'O' ): 
                    canChoose = False
                    while (not canChoose):  #loop and reroll until there are options to pick from 
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
                    choice = choice - 1
                    if not isValidMove( gameboard, choice, 'O' ):       #***fix*** this is only here bc the database has preexisiting states with invalid moves. Redoing the db would fix
                        i[choice+1] = -1
                
                self.gamesteps.append(gameboard)    #add board and choice taken to gamesteps
                self.gamesteps.append(choice+1)

                return choice
                        
        print('Bug Found: ', gameboard, 'not found in kb.')
        #edge case: if a valid move is not returned for whatever reason, play first available move
        for x in range(self.numOptions):
            if gameboard[x] == '-' and isValidMove( gameboard, x, 'O' ):
                return x
        
    #update actions based on game result
    def endGame( self, status, gameboard ):
        # learn from the result
        if status == 1: 
            # you won the game
            factor = self.lfactor
            m = len(self.gamesteps)-2   #go back to last state of the game 

            while m >= 0: 
                state = self.gamesteps[m]    #current step
                chose = self.gamesteps[m+1]   #spot chosen
                for i in self.kb:
                    if i[0] == state:     #find the gameboard in kb 
                        if m == len(self.gamesteps)-2:  #set last choice to 1, it won us the game  
                            i[chose] = 1
                            j = 1   #set all other options to -1
                            while j < len(i): 
                                if j != chose:
                                    i[j] = -1
                                j += 1 
                        else:     #all other options are affected by decay
                            
                            diff = (i[chose] - (i[chose] + (i[chose] * factor)) )*-1   #the difference taken will be spread across the other possible choices  
                            i[chose] = i[chose] + (i[chose] * factor)   #add the factor 
                            if i[chose] > 1: 
                                i[chose] = 1

                            factor *= self.ldecay   #decay learning factor for next step
                    
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
                        break

                m = m - 2

            self.gamesteps = []     #empty out the taken steps for this game
        elif status == -1:
            # you lost the game
            factor = self.lfactor
            m = len(self.gamesteps)-2

            while m >= 0: 
                state = self.gamesteps[m]    #current step  
                chose = self.gamesteps[m+1]   #spot chosen
                for i in self.kb:
                    if i[0] == state:     #find the gameboard in kb 
                        if m == len(self.gamesteps)-4:  #set second to last choice to 0 
                            diff = i[chose]
                            i[chose] = 0
                        else:     #all other options are affected by decay
                            if m == len(self.gamesteps)-2:    #check last state and if there was only one option left, set that option to 1 
                                onemove = True
                                movescount = 0
                                for x in state: 
                                    if x == '-':
                                        movescount += 1
                                        if movescount > 1:
                                            onemove = False
                                            break
                                
                                if onemove:
                                    j = 1   #set all other options to -1
                                    while j < len(i): 
                                        if j != chose:
                                            i[j] = -1
                                        j += 1
                                    diff = 0
                                else:   #if there was more than one move do as normal
                                    diff = i[chose] - (i[chose] - (i[chose] * factor))      
                                    i[chose] = i[chose] - (i[chose] * factor)         
                                    if i[chose] < 0.00006: 
                                        i[chose] = 0 
                            else:  
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
                        break

                m = m - 2
            
            self.gamesteps = []     #empty out the taken steps for this game
        else: # status == 0
            # no winner
            self.gamesteps = []

    #update knowledge base file 
    def stopPlaying(self):
        print('updating kb')
        with open(self.datafile, 'w') as file: 
            for x in self.kb: 
                file.write(x[0] + ', ')

                for i in x[1:len(x)-1]: 
                    file.write(str(i) + ', ')
                file.write(str(x[len(x)-1])+'\n')
            
                # print(x)
        #print(self.gamesteps)
        return