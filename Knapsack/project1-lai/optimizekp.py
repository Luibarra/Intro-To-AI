import time
import numpy as np

#function returns the resulting haul of a subset
def haul(subset, values, weights, cap):
    v = 0.0     #starting value
    w = 0.0     #starting weight
    n = len(subset)

    for i in range(n):
        if(subset[i] == 1):     #if this subset takes i, add up attributes
            v = v + values[i]
            w = w + weights[i]

    if w > cap:     #if over cap, reset value
        v= 0.0

    return (v, w)

#function returns a subset with an element change in order to compare
def adjSubset(subset, rnd):
    n = len(subset)
    next = np.copy(subset)      #copy the subset
    i = rnd.randint(n)      #pick a spot in the subset

    if next[i] == 0:    #if the item is taken or not, switch it 
        next[i] = 1
    elif next[i] == 1:
        next[i] = 0

    return next     #return the new subset to compare

#function returns best subset considered represented in 0s and 1s
def temper(n, rnd, values, weights, cap, itercap, maxheat, alpha):
    stime = time.time() 
    heat = maxheat      #heat starts at max
    subset = np.ones(n, dtype=np.int64)     #starting subset is taking all elements
    (v, w) = haul(subset, values, weights, cap)     #starting haul value to compare to adjacent
    heatcheck = (int)(itercap / 10)     #heat will be checked every tenth interval for a breakdown

    print('\n-Heat Over Time-')

    #loop through given iterations
    i = 0
    while i < itercap:
        adjsubset = adjSubset(subset, rnd)      #create an adjacent subset
        (adjv, _) = haul(adjsubset, values, weights, cap)       #find resulting haul of adjsubset

        #if it has been over 5 minutes, break
        if (time.time() - stime) >= 300:
            break

        #compare quality of subsets
        if adjv > v:    #if new subset returns higher value, replace
            subset = adjsubset
            v = adjv
        else:
            acceptance = np.exp((adjv - v) / heat)      #create acceptance range, chance shrinks as temp lowers
            p = rnd.random()    
            if p < acceptance:      #if random p is within range, replace anyways
                subset = adjsubset
                v = adjv 
        
        if i % heatcheck == 0:  #if at tenth interval, output heat 
            print('%.2f' %(heat))

        if heat < 0.00001:      #level heat to 0 when low enough
            heat = 0.00001
        else:
            heat = heat * alpha     #deacrease heat by alpha value
        
        i = i + 1

    return subset

#item label, weight, value
data = []

#input
filename = input('What file would you like to test? ')
print()
print('Testing Knapsack problem using Simulated Annealing...')
print('Testing using', filename, 'dataset...\n') #comma places a space, plus concatonates(only on str).

#------------- file directory ----------------
with open('testcases/'+filename) as textFile:
    for line in textFile:
        x = [item.strip() for item in line.split(',')]
        x = [int(i) if i.isdigit() else i for i in x]   #change str integers to int
        data.append(x)

#save capacity and length of list 
cap = data[0][1]
n = data[0][0]

#create attribute lists
values = []
weights = []
for x in data[1:]:      #move attributes into seperate arrays
    values.append(x[2])
    weights.append(x[1])

#
cont = 'y'
while cont != 'n':
    #Tempering Variables
    itercap = int(input('# of Intervals: '))
    maxheat = int(input('Starting Heat: '))
    alpha = float(input('Heat Cooling Alpha: '))

    rnd = np.random.RandomState(20)      #set random state variable

    start = time.time()
    best = temper(n, rnd, values, weights, cap, itercap, maxheat, alpha)
    runtime = (time.time() - start)*1000

    numitems = 0
    for x in best:
        if x == 1:
            numitems = numitems + 1

    (v, w) = haul(best, values, weights, cap)

    #output results
    print('\nNumber of Items Stolen:', numitems)
    print('Highest Value Haul:', v)
    print('Knapsack Weight:', w)
    print('Runtime:', runtime, '\n')

    cont = input('continue(y/n)? ')






