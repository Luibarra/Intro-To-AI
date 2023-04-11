The file directory in each program is labeled by the comment: 

"------------- file directory ----------------"

It is currently looking for a folder "testcases/", that string can be changed. 
Each program requires the filename entered as input. 

knapsack.py - Greedy Methods
	Libraries Used:
		-import time-
	The program prints out each method results and times. 
	The chosen list can be printed by uncommenting code blocks labeled under "Debug:"
	
exhaustivekp.py - Exhaustive and Pruning
	Libraries Used:
		-import time-
		-from itertools import combinations-
	The program returns exhaustive first then pruning results.
	20 minute timer code is labeled under "Debug: "

optimizekp.py - Personal Optimization (Annealing)
	Libraries Used:
		-import time-
		-import numpy as np-
	This program takes inputs for:
		# of Iterations
		Starting Temp
		Alpha Variable
	Recommended Starting Input:
		1000
		10000
		.98
		