CS 467
These files are created for use in phase #1 of project #3, writing a reinforcement learning agent for Tic-Tac-Toe

Included:
>> single-game.py : run this to play one game and show the outcome. Assumes agent implementations have functions for __init__, getMove and endGame
>> training.py    : run this to play N games and show the win/loss totals for each player (without showing individual game outcomes). Assumes agent implementations have functions for __init__, getMove, endGame and stopPlaying (to indicate that training is done and updated knowledge should be written to the knowledge base file)
>> randomplayer.py : sample agent implementation, plays randomly
>> human.py        : allows a human player to select moves through console input
>> agent.py        : stub implementation of agent. You should implement here a Q-learning agent, capable of playing either first or second in a game of Tic-Tac-Toe. Your agent will be tested with a framework comparable to single-game.py but you are encouraged to use training.py as a framework for training your RL agent.