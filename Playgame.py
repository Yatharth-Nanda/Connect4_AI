# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 11:39:10 2023

@author: yatha
"""
from FourConnect import * # See the FourConnect.py file
import csv
import math
import copy
import numpy as np
import time

class GameTreePlayer:
    
    def __init__(self):
        self.number_of_calls=0 # to store total number of minimax calls 
        
        pass
    '''
    the commented out functions are also evaluation function based on different heuristics 
    their functioning has been detailed in the report 
    the main evaluation function is below , that calls the score function and then uses the difference for evaluation
    
    
    dynamic move ordering has been commented out ( approach 3 ), the reasoning for same is in report 
    static move ordering has been used (approach 2 )
    '''
    
    
    '''EVALUATION FUNCTION 1 '''
    # def evaluate_state(self,state):
    #     #implementing heuristic that  counts coins in the central portion of board are more valuable than the ones towards edges 
          
    #     state_value=0
    #     for r in range(6):
    #         for c in range(7):
    #             #finding distance from the edges of the grid 
    #             #h=min(abs(r-(-1)),abs(r-6))
    #             v=min(abs(c-(-1)),abs(c-7))
               
    #             scaling_factor=r*v
    #             player=state[r][c]
    #             if player==1:
    #                 state_value-=scaling_factor
    #             elif player ==2:
    #                 state_value+=scaling_factor
               
    #     return state_value
    
    '''EVALUATION FUNCTION 2'''
    # def evaluate_state(self,state):
    #   #implementing the heuristic for counting coins irrespective of the position in board 
    #       state_value=0
    #       val1=self.score(state,2)
    #       val2=self.score(state,1)
    #       if(val1>=900000):
    #             return val1
    #       elif(val2>=900000):
    #             return -val2
          
    #       for r in range(6):
    #           for c in range(7):
                
    #             player=state[r][c]
    #             if player==1:
    #                 state_value-=1
    #             elif player ==2:
    #                 state_value+=1
    #             else:
    #                 state_value+=0.1
    #       return state_value
                 
         

    def transform (self,x): # to transform the count vector into number of 1s , number of 2s and so on 
        for i in range(1,len(x)):
            x[i]=x[i]/i;
        return x
    
    def _CountHorizontal(self,player,state): # count horizontal sets of 2s,3s,4s and return them in a vector 
        g = state
        coin_count=np.zeros(5)
        for i in range(6):
            for j in range(7): 
                
                if(g[i][j]==player):# that position itself should have a coin of player 1 
                    cMin=cMax=j                     
                    while True:
                        cMin = cMin-1  # left of the current coin position 
                        if cMin<0 or g[i][cMin]!=player: # if out of bounds or not player 
                            cMin = cMin+1
                            break
                    while True:
                        cMax = cMax+1 # right of the current coin position 
                        if cMax>6 or g[i][cMax]!=player:
                            cMax = cMax-1 # to keep within bound / till last similar coin
                            break
                        
                        # if cmin and cmax are pointing to the last coins at the end of a chain for a single player , then is it deciding if the player can win..
                        # in the sense that if he places the coin here then to the right and left of it there will be at least 3 coins , making it a total of 4 or more coins with it placed rightly 
                    
                    
                    coin_count[min(cMax-cMin+1,4)]+=1
        return coin_count                
        
    def _CountVertical(self,player,state):# count vertical sets of 1s , 2s,3s,4s and return them in a vector 
        g = state
        coin_count=np.zeros(5)
        for i in range(6):
            for j in range(7): 
                       
                if(g[i][j]==player):# that position itself should have a coin of player 1 
                    rMin=rMax=i
                    while True:
                        rMin = rMin-1
                        if rMin<0 or g[rMin][j]!=player:
                            rMin = rMin+1
                            break
                    while True:
                        rMax = rMax+1
                        if rMax>5 or g[rMax][j]!=player:
                            rMax = rMax-1
                            break
                
                    coin_count[min(rMax-rMin +1,4)]+=1
        return coin_count                
    def _CountDiag(self,player,diag,state):# count horizontal sets of 1s,2s,3s,4s and return them in a vector 
        g = state
        coin_count=np.zeros(5)
        
        for i in range(6):
            for j in range(7): 
                
                
                if(g[i][j]==player):# that position itself should have a coin of player 1 
                    rMin=rMax=i
                    cMin=cMax=j
                    while True:
                        cMin = cMin -1 # moving left and downward means increasing row and column , when diag=1
                        rMax = rMax + diag
                        if cMin<0 or rMax<0 or rMax>5 or g[rMax][cMin]!=player:
                            cMin = cMin +1
                            rMax = rMax - diag
                            break
                    while True:
                        cMax = cMax+1
                        rMin = rMin-diag
                        if cMax>6 or rMin<0 or rMin>5 or g[rMin][cMax]!=player:
                            cMax = cMax-1
                            rMin = rMin+diag
                            break
                   
                    coin_count[min(cMax-cMin +1,4)]+=1
        return coin_count        
    
    '''EVALUATION FUNCTION 3 '''
    
    def evaluate_state(self,state):
          return self.score(state,2)-self.score(state,1) # subtract score of player2 from player1 
    
    
    
    def score(self,state,player):
        t1= GameTreePlayer()
        a1=t1.transform(t1._CountHorizontal(player,state))
        a2=(t1.transform(t1._CountVertical(player,state)))
        a3=(t1.transform(t1._CountDiag(player,1,state)))
        a4=(t1.transform(t1._CountDiag(player,-1,state)))
        final_count=np.add(np.add(a1,a2),np.add(a3,a4))
        #I have written the function to count groups of consecutive 2s ,3s and 4s and then hit and trialed with weights to fine tune the final score and test for better winning results 
        #if it is a win state , i.e at least 1 consecutive 4 , then the lesser coins on the state the better it is for us ,to ensure a faster win
        #this is to tie break against win  that are reached after more moves  and push to reach the win faster
        if(final_count[4]>=1):
            value=value=-1*final_count[1]-final_count[2]*1000-final_count[3]*5000+final_count[4]*1000000
        #is not a win state , then the more coins , the better for us as we have more potential chances 
        else:
            value=1*final_count[1]+final_count[2]*1000+final_count[3]*5000+final_count[4]*1000000
        
        return value
    
    def is_terminal(self, board):
        #return  sum(row.count(0) for row in board) == 0
        # state is terminal if there are no more moves or if one of the players has won
        return abs(self.score(board,2)) >= 900000 or self.score(board,1) >= 900000 or sum(row.count(0) for row in board) == 0 
    
    def find_next_state(self,curr_state,action,player):
    
        cRow = -1 # if action invalid return -1 
        c=action
        for r in range(5,-1,-1):  # iterates upwards in a col and break at first zero
            if curr_state[r][c]==0:
                cRow=r
                break
        if(cRow==-1):
            return None
        else :            
            new_state=copy.deepcopy(curr_state)
            new_state[cRow][action]=player 
            return new_state
    

    def action_value(self, state, action): # make a new state right after the current one and return its evaluation
        next_state = self.find_next_state(state,action,2)
        if next_state is  None:
            return 0
        else:
            return self.evaluate_state(next_state)
    
    
    def minimax(self,state,depth,player,alpha,beta):
        self.number_of_calls+=1
        if depth==0 or self.is_terminal(state):
            return self.evaluate_state(state),0
        
        
        '''dynamic move ordering'''
        #ordered_actions=list(range(7))        
        #ordered_actions.sort(key=lambda action:self.action_value(state, action), reverse=True)
        '''static move ordering '''
        ordered_actions = [3,4,2,1,5,6,0] # centrally prioritised actions as coins in centre are more likely to lead to better states 

        best_action = -1
        if player==1:
            min_value = math.inf
            for action in ordered_actions:
                next_state = self.find_next_state(state,action,player)
                if (next_state is not None):
                    next_state_score,_ = self.minimax(next_state,depth-1,2,alpha,beta)
                    if next_state_score < min_value: # if a better state score is found we replace it 
                        min_value = next_state_score
                        best_action = action
                    beta = min(min_value,beta)
                    if beta <= alpha:
                        break
            return min_value , best_action

        if player==2:
            max_value = -math.inf
            for action  in ordered_actions:
                next_state = self.find_next_state(state,action,player)
                if (next_state is not None):
                    next_state_score,_ = self.minimax(next_state,depth-1,1,alpha,beta)
                    if next_state_score > max_value:
                        max_value = next_state_score
                        best_action = action
                    alpha = max( max_value,alpha)
                    if beta <= alpha:
                        break

            return max_value, best_action
    
    def FindBestAction(self,currentState):
        """
        Modify this function to search the GameTree instead of getting input from the keyboard.
        The currentState of the game is passed to the function.
        currentState[0][0] refers to the top-left corner position.
        currentState[5][6] refers to the bottom-right corner position.
        Action refers to the column in which you decide to put your coin. The actions (and columns) are numbered from left to right.
        Action 0 is refers to the left-most column and action 6 refers to the right-most column.
        """
        alpha = -math.inf
        beta = math.inf
        #adjusting paramters for a 5 move look ahead for player 2 
        _,bestAction = self.minimax(currentState,5,2,alpha,beta)
        return bestAction


def LoadTestcaseStateFromCSVfile():
    testcaseState=list()

    with open('testcase.csv', 'r') as read_obj: 
       	csvReader = csv.reader(read_obj)
        for csvRow in csvReader:
            row = [int(r) for r in csvRow]
            testcaseState.append(row)
        return testcaseState


def PlayGameHuman():
    fourConnect = FourConnect()
    fourConnect.PrintGameState()
    gameTree = GameTreePlayer()
    
    move=0
    while move<42: #At most 42 moves are possible
        if move%2 == 0: #Myopic player always moves first
            fourConnect.HumanPlayerAction()
        else:
            currentState = fourConnect.GetCurrentState()
            gameTreeAction = gameTree.FindBestAction(currentState)
            fourConnect.GameTreePlayerAction(gameTreeAction)
        fourConnect.PrintGameState()
        move += 1
        if fourConnect.winner!=None:
            break
    
    """
    You can add your code here to count the number of wins average number of moves etc.
    You can modify the PlayGame() function to play multiple games if required.
    """
    if fourConnect.winner==None:
        print("Game is drawn.")
    else:
        print("Winner : Player {0}\n".format(fourConnect.winner))
    print("Moves : {0}".format(move))
def PlayGame():

    num_plays = 50
    wins=np.zeros(3) # to store wins , wins [0] is draw  , wins[1] is player 1 wins , wins[2] is player 2 wins 
    total_moves=0
    number_of_minimaxcalls=0
    for i in range(num_plays):
        fourConnect = FourConnect()
        fourConnect.PrintGameState()
        gameTree = GameTreePlayer()
        
        move=0
        while move<42: #At most 42 moves are possible
            if move%2 == 0: #Myopic player always moves first
                fourConnect.MyopicPlayerAction()
            else:
                currentState = fourConnect.GetCurrentState()
                gameTreeAction = gameTree.FindBestAction(currentState)
                fourConnect.GameTreePlayerAction(gameTreeAction)
            #fourConnect.PrintGameState()
            move += 1
            if fourConnect.winner!=None:
                break
        
        number_of_minimaxcalls+=gameTree.number_of_calls
        
        if fourConnect.winner==2:
            wins[2]+=1
            total_moves+=move
        elif fourConnect.winner==1:
            wins[1]+=1
        else:
            wins[0]+=1
    
        
            
    print("Average number of moves="+str(total_moves/wins[2]))    
    print(wins)
    print("Player 2 wins: {0}\n".format(wins[2]))
    print("Player 1 wins: {0}\n".format(wins[1]))
    print("Draws: {0}\n".format(wins[0]))
    print("Number of calls="+str(number_of_minimaxcalls/50))
    

def RunTestCase():
    """
    This procedure reads the state in testcase.csv file and start the game.
    Player 2 moves first. Player 2 must win in 5 moves to pass the testcase; Otherwise, the program fails to pass the testcase.
    """
    
    fourConnect = FourConnect()
    gameTree = GameTreePlayer()
    testcaseState = LoadTestcaseStateFromCSVfile()
    fourConnect.SetCurrentState(testcaseState)
    fourConnect.PrintGameState()

    move=0
    while move<5: #Player 2 must win in 5 moves
        if move%2 == 1: 
            fourConnect.MyopicPlayerAction()
        else:
            currentState = fourConnect.GetCurrentState()
            gameTreeAction = gameTree.FindBestAction(currentState)
            fourConnect.GameTreePlayerAction(gameTreeAction)
        fourConnect.PrintGameState()
        move += 1
        if fourConnect.winner!=None:
            break
    
    print("Roll no : 2021AAPS1291G") #Put your roll number here
    
    if fourConnect.winner==2:
        print("Player 2 has won. Testcase passed.")
    else:
        print("Player 2 could not win in 5 moves. Testcase failed.")
    print("Moves : {0}".format(move))
    

def main():
    # start_time = time.time()
    #PlayGame()
    # end_time = time.time()

    # Calculate the elapsed time
    # elapsed_time = end_time - start_time
    
    # Print the elapsed time
    # print(f"Elapsed Time: {elapsed_time} seconds")
    PlayGameHuman()   
    #RunTestCase()


if __name__=='__main__':
    main()
