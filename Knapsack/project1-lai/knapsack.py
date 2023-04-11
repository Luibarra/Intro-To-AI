import time
#--- attribute return methods ---
def getValue(array):
    if len(array) == 2:
        return 0
    return array[2]
    
def getWeight(array):
    if len(array) == 2:
        return 0
    return array[1]

def getRatio(array):
    if len(array) == 2:
        return 0
    if array[1] == 0:
        return array[2]/0.1
    return array[2]/array[1]

#method returns list sorted by method
def SortList(array, method):
    match method:
        case "value":
            #print('value')
            array.sort(key=getValue, reverse=True)
            return array
        case "weight":
            #print('weight')
            array.sort(key=getWeight)
            return array
        case "ratio":
            #print('ratio')
            array.sort(key=getRatio, reverse=True)
            return array
        case _:
            print('invalid method')

#method returns filled knapsack
def fillKP(list, weightLimit):
    kp = []
    total = 0
    i = 0
    while (total < weightLimit) and (i < len(list)):    #while we are under limit and in bounds
        if(len(list[i]) == 3):  #ignore starting row
            if (total+list[i][1]) <= weightLimit:   #if item fits with rest, add to pack
                kp.append(list[i])
                total = total + list[i][1]  #inc pack weight
        i = i+1 #inc in list
    
    return kp

#item label, weight, value
list = []

#input
filename = input('What file would you like to test? ')
print()
print('Testing Knapsack using Greedy Methods...')
print('Testing using', filename, 'dataset...') #comma places a space, plus concatonates(only on str).

#------------- file directory ----------------
with open('testcases/'+filename) as textFile:
    for line in textFile:
        x = [item.strip() for item in line.split(',')]
        x = [int(i) if i.isdigit() else i for i in x]   #change str integers to int
        list.append(x)

#set weight limit
weightLimit = list[0][1]

#--- Fill Knapsacks ---

#sort by weight method
start = time.time()     #time before function
wkp = fillKP(SortList(list, 'weight'), weightLimit)
end = time.time()       #time after function
elapseW = (end - start) * 1000  #time taken in milliseconds for this method

#sort by value method
start = time.time()     
vkp = fillKP(SortList(list, 'value'), weightLimit)
end = time.time()       
elapseV = (end - start) * 1000  #time taken in milliseconds for this method

#sort by ratio method
start = time.time()     
rkp = fillKP(SortList(list, 'ratio'), weightLimit)
end = time.time()       
elapseR = (end - start) * 1000  #time taken in milliseconds for this method

#output knapsack haul
print('Weight Limit:', str(weightLimit) + '...\n')

if len(wkp) == 0:    #edge case, nothing fits
    print('Nothing Fits!')
else:
# ----- Output Weight Results -----
    print('--- Weight Method ---') 
    # print('[name][weight][value]')     #Debug: uncomment for Haul output
    sum = 0
    w = 0
    for x in wkp:
        sum = sum + x[2]
        w = w + x[1]
        #Debug: uncomment for loop and print() for Haul output
        # for y in x:   
        #     print(y, end = " ")
        # print()
    print('Number of Items Stolen:', len(wkp))
    print('Value of items stolen:', sum)
    print('Knapsack Weight:', w)
    print('Runtime:', elapseW, '\n')

# ----- Output Value Results -----
    print('--- Value Method ---') 
    # print('[name][weight][value]')    #Debug: uncomment for Haul output 
    sum = 0
    w = 0
    for x in vkp:
        sum = sum + x[2]
        w = w + x[1]
        #Debug: uncomment for loop and print() for Haul output
        # for y in x:   
        #     print(y, end = " ")
        #print()
    print('Number of Items Stolen:', len(vkp))
    print('Value of Items Stolen:', sum)
    print('Knapsack Weight:', w)
    print('Runtime:', elapseV, '\n')

# ----- Output Ratio Results -----
    print('--- Ratio Method ---') 
    # print('[name][weight][value]')    #Debug: uncomment for Haul output 
    sum = 0
    w = 0
    for x in rkp:
        sum = sum + x[2]
        w = w + x[1]
        #Debug: uncomment for loop and print() for Haul output
        # for y in x:   
        #     print(y, end = " ")
        # print()
    print('Number of Items Stolen:', len(rkp))
    print('Value of Items Stolen:', sum)
    print('Knapsack Weight:', w)
    print('Runtime:', elapseR, '\n')

# Debug: print list
# for x in list:
#     for y in x:
#        print(y, end = " ")
#     print()
# print()