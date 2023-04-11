import os
import time
import random
import numpy as np
    
#function creates starting population
def initPop(nPop):           
    pop = ['s010&e000&m000', 's000&e010&m000', 's000&e000&m010', 's010&e010&m000','s010&e000&m020', 
           's025|e015&m000','s030|e030|m030','s010&s025|e000','s900&e950|m950','s008&e008|m050']        #starting population list genotypes
    
    for i in range(nPop - 10):
        genotype = ''       #current genotype
        
        for j in range(14):
            alle = ''
        
            match j:
                case 0:
                    three = random.randint(0,2)
                    if(three == 0):
                        alle = 'e'
                    elif(three == 1):
                        alle = 's'
                    else:
                        alle = 'm'
                case 5:
                    three = random.randint(0,2)
                    if(three == 0):
                        alle = 'e'
                    elif(three == 1):
                        alle = 's'
                    else:
                        alle = 'm'
                case 10:
                    three = random.randint(0,2)
                    if(three == 0):
                        alle = 'e'
                    elif(three == 1):
                        alle = 's'
                    else:
                        alle = 'm'
                case 4:
                    flip = random.randint(0,1)
                    if flip == 0:
                        alle = '&'
                    else:
                        alle = '|'
                case 9:
                    flip = random.randint(0,1)
                    if flip == 0:
                        alle = '&'
                    else:
                        alle = '|'
                case _:
                    alle = str(random.randint(0,9))
            
            genotype += alle

        #print(genotype)
        pop.append(genotype)        #add genotype to population

    return pop

#function runs odds of mutation, forced switch mutation
def mutate(child, chance):
    for x in child:
        if rnd.random() < chance:
            match x:
                case 'e':
                    flip = random.randint(0,1)
                    if flip == 0:
                        x = 's'
                    else:
                        x = 'm'
                case 's':
                    flip = random.randint(0,1)
                    if flip == 0:
                        x = 'e'
                    else:
                        x = 'm'
                case 'm':
                    flip = random.randint(0,1)
                    if flip == 0:
                        x = 'e'
                    else:
                        x = 's'
                case '&':
                    x = '|'
                case '|':
                    x = '&'
                case _:
                    num = str(random.randint(0,9))
                    while num == x:
                        num = str(random.randint(0,9))
                    x = num

    return child

#average eval of population used in fitness function
def avgEval(pop, allowance):
    e = 0       #average eval e 
    evals = []      #list of evaluations to be averaged

    #loop through each genotype
    for i in pop:       
        eval = fitness(i, allowance)
        # print(eval, "\n")
        evals.append(eval)  #add eval to list

    e = np.mean(evals)  #average list
    return e

#returns fitness of given genotype
def fitness(genotype, allowance):

    fit = 0
    mod1 = genotype[4]
    mod2 = genotype[9]
    days1 = int(genotype[1:4])
    days2 = int(genotype[6:9])
    days3 = int(genotype[11:14])
    #print(genotype) 
    for filename in os.listdir('testdata/'):
        data = []
        mainFund = allowance
        savingFund = 0
        shares = 0
        #------------- file directory ----------------
        with open('testdata/'+filename) as textFile:
            for line in textFile:
                x = [item.strip() for item in line.split(' ')]   
                for i in x:         #change each str num to float variable
                    if(isfloat(i)):
                        data.append(float(i))      
        data = data[2:]
        #print(data, '\n')

        day = 0
        purchased = 0
        while day < len(data):
            buy = False

            rule1 = stockpick(genotype[0:4], data, data[day], day)
            rule2 = stockpick(genotype[5:9], data, data[day], day)
            rule3 = stockpick(genotype[10:14], data, data[day], day)

            #Determine whether to buy: uses num days to check if 0 and rule results to perform the operator logic
            buy = buyorsell(days1, days2, days3, rule1, rule2, rule3, mod1, mod2)
            
            #sell or buy based on result
            if(buy): 
                purchased += 1
                while mainFund > data[day]:
                    shares += 1
                    mainFund -= data[day]
            else: 
                while shares > 0: 
                    shares -= 1
                    mainFund += data[day]

            #if selling has brought the mainFund over 20k,
            if(mainFund > allowance):    #add difference to savings and set mainFund     
                savingFund += mainFund - allowance      
                mainFund = allowance
            elif (mainFund < allowance):    #if under allowance
                dif = allowance - mainFund
                if(savingFund > dif):       #make sure savings can add full dif
                    savingFund -= dif
                    mainFund = allowance
                else:
                    mainFund += savingFund  #if not, add full saving fund

            #if final day, sell out with final day price
            if(day == len(data)-1): 
                while shares > 0: 
                    shares -= 1
                    mainFund += data[day]
            
            day += 1
        #print(filename, f'Fit:{mainFund+savingFund: ,.2f}')     #Debug

        #punish those who do not act    
        if(purchased < 1):
            mainFund /= 2
            savingFund /= 2
        fit += mainFund + savingFund        #add money made to fit 

    #print(f'Fit {fit: .2f}\n')     #Debug
    return fit

#determines if rule in genotype was met 
def stockpick(rule, data, price, i):
    law = rule[0]
    days = int(rule[1:4])

    if(i > days):   #ensure we have enough past days to continue
        if(law == 'm'):     #if price is greater than max over N days
            max = 0
            index = i - 1
            for x in range(days): 
                if(data[index] > max): 
                    max = data[index]
                index -= 1
            if(price > max): 
                return True
            
        elif(law == 's'):   #if price is greater than sma over N days
            sma = 0
            index = i - 1
            for x in range(days): 
                sma += data[index]      #add up prices of N days
                index -= 1
            if days != 0:
                sma = sma / days    #divide by N
            if(price > sma): 
                return True
            
        elif(law == 'e'):   #if price is greater than ema over N days
            num = data[i - 1]
            den = 1
            index = i - 2
            alpha = 2 / (days+1)
            for x in range(days - 1): 
                num += ((1 - alpha)**x) * data[index]
                den += ((1 - alpha)**x)
            ema = num / den    
            if(price > ema): 
                return True

    return False

#logical operation given rule results
def buyorsell(days1, days2, days3, rule1, rule2, rule3, mod1, mod2): 
    buy  = False
    
    if(days1 == 0 and days2 == 0 and days3 == 0):   #first check if all are 0 and return false
        buy = False
    else:
        #change rule bools based on first logical pair
        if(mod1 == '&'): 
            if(days1 == 0 and days2 == 0):      
                if(mod2 == '|'):     #edge case, if both were switch to true when zero, they would affect an or statement
                    rule1 = False
                    rule2 = False
                else:
                    rule1 = True
                    rule2 = True
            elif(days1 == 0): 
                rule1 = True
            elif(days2 == 0):
                rule2 = True
        else:
            if(days1 == 0 and days2 == 0):      
                if(mod2 == '&'):     #edge case, if both were switched to false when zero, they would affect an and statement
                    rule1 = True
                    rule2 = True
                else:
                    rule1 = False
                    rule2 = False
            elif(days1 == 0): 
                rule1 = False
            elif(days2 == 0):
                rule2 = False
        
        if(mod2 == '&' and days3 == 0):
            rule3 = True 
        elif(mod2 == '|' and days3 == 0):
            rule3 = False

    #commit operator logic with results
    if(mod1 == mod2):
        if(mod1 == '&'):    #2 and
            if(rule1 and rule2) and rule3: 
                buy = True      
        else:   #2 or
            if(rule1 or rule2) or rule3: 
                buy = True       
    else: 
        if(mod1 == '&' and mod2 == '|'):    #and or
            if(rule1 and rule2) or rule3: 
                buy = True     
        else:   
            if(rule1 or rule2) and rule3:   #or and
                buy = True 

    return buy

#returns bool if string is float
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


#Init Values
data = []       #item label, weight, value
numGens = 200    #number of generations   
initsize = 50      #initial population size

n = 14      #length of genotype
allowance = 20000       #starting fund per run 

mutateChance = 0.01
rnd = np.random.RandomState(20)     #rng state

#input
print('Testing Stock Picks using Genetic Algorithms...')
print()

#create random starting population
start = time.time()     #time before function
initpop = initPop(initsize)     #create initial population
#Debug: print init population
print(len(initpop))
for x in initpop:
    print("[", end = " ")
    for y in x:
       print(y, end = " ")
    print("]")
print()

e = avgEval(initpop, allowance)     #find average fitness over initpop 
print("e =", e,"\n")       #Debug

#---- Individual Evaluation ----
#General Comparison -- remove penalty from fit func, 100000 allowance -- BAC,GRMN,KR DATA
# naive = ['s010&s010&s010','s030&s030&s030','e010&e010&e010','e030&e030&e030','m010&m010&m010','m030&m030&m030','s010|e010|m010','s030|e030|m030']
# best = 's119|s010|m635'
# print('Evaluating Naive vs Best Fit Genotypes...\n')
# print('--- Naive Approaches ---')

# for x in naive:
#     print('Genotype:', x, f' Fit: {fitness(x, allowance): ,.2f}')

# print('\n--- Best Fit Genotype ---')
#print('Genotype:', best, f' Fit: {fitness(best, allowance): ,.2f}')

#Varied Time Eval -- printline in fit func -- AMAZON DATA
# print('Evaluating Over Varied Time Ranges...\n')
# print('--- Best Fit Genotype ---')
# print(best)
# fitness(best, allowance)
# print()

# print('--- Naive Approaches ---')
# for x in naive:
#     print(x)
#     fitness(x, allowance)
#     print()

#---- Build Intermidate Population ----     #remainder stochastic sampling
interpop = []
for g in initpop:
    gfit = fitness(g,allowance) / e

    if gfit > 1:        #if the fit is over 1, include
        #print(gfit)
        interpop.append(g)

        chance = gfit - 1
        p = rnd.random()
        if p < chance:      #remainder percentage chance of copy 
            #print(gfit)
            interpop.append(g)

    elif rnd.random() < gfit:       #else, use fit as percentage chance
        #print(gfit)
        interpop.append(g)


#Debug: print out interpop
print("interpop len:", len(interpop), "\n")
for x in interpop:
    print("[", end = " ")
    for y in x:
       print(y, end = " ")
    print("]")
print()

#---- Generations ----
currentGen = interpop       #set current gen
nCurrentGen = len(interpop)
bestGenotype = []       #set current best solution
bestFitness = 0

#loop through set generations
for gen in range(numGens):
    nextGen = []
    for i in range(int(initsize / 2)):
        parent1 = random.randint(0, nCurrentGen - 1)     #pick parents
        parent2 = random.randint(0, nCurrentGen - 1)
        while parent2 == parent1:       #replace parent 2 if same as 1, continue if repeat
            parent2 = random.randint(0, nCurrentGen - 1)

        parent1 = currentGen[parent1]
        parent2 = currentGen[parent2]

        d5 = random.randint(1,5)    
        if d5 == 1:     #parents are copied over at a rate of .2 aka 20%
            nextGen.append(parent1) 
            nextGen.append(parent2)
        else:
            p1_a = ''       #create lists for each half of each parent
            p1_b = ''
            p2_a = ''
            p2_b = ''
            crossPoint = random.randint(1, n - 1)       #choose random crossing point

            #create halves
            i = 0
            while i < crossPoint:   #fill first half of both 
                p1_a += parent1[i]
                p2_a += parent2[i]
                i += 1
            while i < n:        #fill second half     
                p1_b += parent1[i]
                p2_b += parent2[i]
                i += 1
            
            #create children
            child1 = p1_a + p2_b
            child2 = p2_a + p1_b

            #mutation check
            child1 = mutate(child1, mutateChance)
            child2 = mutate(child2, mutateChance)

            #add to generation
            nextGen.append(child1)
            nextGen.append(child2)

    #replace current gen 
    currentGen = nextGen
    nCurrentGen = len(nextGen)

    #find if best result is in current generation
    for x in currentGen:
        fit = fitness(x, allowance) / e
        if fit > bestFitness:
            bestFitness = fit
            bestGenotype = x
            print("Best Genotype:", bestGenotype, "Fit:", bestFitness)

end = time.time()       #time after function

print()
print("--- Output ---")
print("e =", e)
print("Best Genotype:", bestGenotype)
print("Runtime:", ((end - start) * 1000))

