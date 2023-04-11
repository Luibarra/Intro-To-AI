import time
import random
import numpy as np

#function creates starting pop
def initPop(nPop, nArray):              # **change from true random** #
    pop = []        #population list
    for i in range(nPop):
        genotype = []       #current genotype
        for j in range(nArray):
            flip = random.randint(0,1)      #randomly pick each gene in genotype
            if flip == 0:
                genotype.append(0)
            else:
                genotype.append(1)
        
        pop.append(genotype)        #add genotype to population

    return pop

#average eval of population used in fitness function
def avgEval(pop, values, weights):
    e = 0       #average eval e 
    evals = []      #list of evaluations to be averaged

    #loop through each genotype
    for i in pop:       
        eval = 0    #current eval of genotype
        v = 0   #attribute variables
        w = 0

        #loop through current genotype
        j = 0       #index of current genotype
        while j < len(i):
            if i[j] == 1:       #if this index is taken, add to total attributes
                v += values[j]
                w += weights[j]
                eval = v / w        #update eval 
            j += 1

        # print("V:", v, "W:", w)#Debug: print genotype eval
        # print(eval, "\n")
        evals.append(eval)  #add eval to list

    e = np.mean(evals)  #average list
    return e

#returns fitness of given genotype
def fitness(genotype, e, values, weights):
    eval = 0
    v = 0
    w = 0

    #loop through current genotype
    j = 0       #index of current genotype
    while j < len(genotype):
        if genotype[j] == 1:       #if this index is taken, add to total attributes
            v += values[j]
            w += weights[j]
            eval = v / w        #update eval 
        j += 1

    return eval / e

#alternate avgEval and fitness function
def altfitness(genotype, e, values, weights):
    eval = 0
    v = 0
    w = 0

    #loop through current genotype
    j = 0       #index of current genotype
    while j < len(genotype):
        if genotype[j] == 1:       #if this index is taken, add to total attributes
            v += values[j]
            w += weights[j]
            eval = v        #update eval 
        j += 1
    
    if w > cap:     #if weight over cap, minimize eval rating
        eval = eval * .01

    return eval / e

def alteval(pop, values, weights):
    e = 0       #average eval e 
    evals = []      #list of evaluations to be averaged

    #loop through each genotype
    for i in pop:       
        eval = 0    #current eval of genotype
        v = 0   #attribute variables
        w = 0

        #loop through current genotype
        j = 0       #index of current genotype
        while j < len(i):
            if i[j] == 1:       #if this index is taken, add to total attributes
                v += values[j]
                w += weights[j]
                eval = v      #update eval 
            j += 1

        # print("V:", v, "W:", w)#Debug: print genotype eval
        # print(eval, "\n")
        if w > cap:
            eval = eval * .01
        evals.append(eval)  #add eval to list

    e = np.mean(evals)  #average list
    return e

#function runs odds of mutation
def mutate(child, chance):
    for x in child:
        if rnd.random() < chance:
            if x == 1:
                x = 0
            else:
                x = 1
    return child

#Init Values
data = []       #item label, weight, value
numGens = 200    #number of generations   
initsize = 100      #initial population size
mutateChance = 0.5
rnd = np.random.RandomState(20)     #rng state

#input
filename = input('What file would you like to test? ')
print()
print('Testing Knapsack using Genetic Algorithm...')
print('Testing using', filename, 'dataset...') #comma places a space, plus concatonates(only on str).
print()

#------------- file directory ----------------
with open('testcases/'+filename) as textFile:
    for line in textFile:
        x = [item.strip() for item in line.split(',')]
        x = [int(i) if i.isdigit() else i for i in x]   #change str integers to int
        data.append(x)      #integer list of testcase

#save capacity and length of list 
cap = data[0][1]
n = data[0][0]

#create attribute lists
values = []
weights = []
for x in data[1:]:      #move attributes into seperate arrays
    values.append(x[2])
    weights.append(x[1])

#create random starting population
start = time.time()     #time before function
initpop = initPop(initsize, n)
#e = avgEval(initpop, values, weights)
e = alteval(initpop, values, weights)                                                                                   #Alternate Function

#print("e =", e,"\n")
#end = time.time()       #time after function
#print("\nInitial population + avg runtime:", ((end - start) * 1000),"\n")  #Debug: time taken in milliseconds to create initial population

#Debug: print init population
# for x in initpop:
#     print("[", end = " ")
#     for y in x:
#        print(y, end = " ")
#     print("]")
# print()

#---- Build Intermidate Population ----     #remainder stochastic sampling
interpop = []
for g in initpop:
    #gfit = fitness(g,e,values,weights)
    gfit = altfitness(g,e,values,weights)                                                                                #Alternate Function

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
#print("interpop len:", len(interpop), "\n")
# for x in interpop:
#     print("[", end = " ")
#     for y in x:
#        print(y, end = " ")
#     print("]")
# print()

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

        d4 = random.randint(1,4)    
        if d4 == 1:     #1 in 4 chance to add parents to next gen
            nextGen.append(parent1) 
            nextGen.append(parent2)
        else:
            p1_a = []       #create lists for each half of each parent
            p1_b = []
            p2_a = []
            p2_b = []
            crossPoint = random.randint(1, n - 1)       #choose random crossing point

            #create halves
            i = 0
            while i < crossPoint:   #fill first half of both 
                p1_a.append(parent1[i])
                p2_a.append(parent2[i])
                i += 1
            while i < n:        #fill second half     
                p1_b.append(parent1[i])
                p2_b.append(parent2[i])
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
        #fit = fitness(x,e,values,weights)
        fit = altfitness(x,e,values,weights)                                                                           #Alternate Function
        if fit > bestFitness:
            bestFitness = fit
            bestGenotype = x
            print("Best Fit:", bestFitness)

end = time.time()       #time after function


finalW = 0
finalV = 0
i = 0
while i < n:        #total up final values
    if bestGenotype[i] == 1:
        finalW += weights[i]
        finalV += values[i]
    i += 1

print()
print("--- Output ---")
print("Haul Value:", finalV)
print("Haul Weight:", finalW)
print("Runtime:", ((end - start) * 1000))

