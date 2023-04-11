import time 
from itertools import combinations

#item label, weight, value
data = []

#input
filename = input('What file would you like to test? ')
print()
print('Testing Knapsack problem Exhaustive Search and Pruning Method...')
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

#----- Exhaustive Search ----------------------------------
print('Exhaustive Search...')
start = time.time()     #start time of search 
high = 0
weight = 0  
numitems = 0
broke = False

#ex search loop through subsets 
for i in range(n+1)[1:]:    #loop through subsets in group sizes of 1 to n
    for j in combinations(data[1:], i):     #loop through each subset
        #Debug: Timer Cap
        if ((time.time() - start) >= 1200):     #if time has gone past 20 minutes, break
            broke = True
            break

        v = 0   #attribute variables
        w = 0
        for x in j:     #find attributes of chosen items in this subset
            v = v + x[2]        #add up total value and weight 
            w = w + x[1]

        if (w <= cap) and (v > high):       #if this subset fits and is more valuable, update highest variables
            high = v
            weight = w
            numitems = len(j)       #save number of items in best

    #Debug: Timer Cap
    if (broke):     #if we broke twenty minutes, fully stop
        broke = False
        break

end = time.time()   #end time of search 
elapse = (end - start)*1000    #time elapsed 

#output ex search Results 
print('Number of Items Stolen:', numitems)
print('Highest Value Haul:', high)
print('Knapsack Weight:', weight)
print('Runtime:', elapse, '\n')

#----- Pruning Search -------------------------------------
print('Pruning Method...')
start = time.time()     #start time of search 
high = 0
weight = 0

#pruning method loop through subsets
for i in range(n+1)[1:]:      
    for j in combinations(data[1:], i):
        #Debug: Timer Cap
        if ((time.time() - start) >= 1200):     
            broke = True
            break

        v = 0
        w = 0
        if j[0][1] <= cap:       #if the weight of the first in the subset fits, continue
            for x in j: 
                v = v + x[2] 
                w = w + x[1]
                if w > cap:     #if gone over cap while adding, break
                    break

        if (w <= cap) and (v > high):      
            high = v
            weight = w
            numitems = len(j)

    #Debug: Timer Cap
    if (broke):    
        broke = False
        break

end = time.time()   #end time of search 
elapse = (end - start)*1000    #time elapsed 

#output results 
print('Number of Items Stolen:', numitems)
print('Highest Value Haul:', str(high))
print('Knapsack Weight:', str(weight))
print('Runtime:', elapse, '\n')

#Debug: print list
# for x in data:
#     for y in x:
#         print(y, end = " ")
#     print()