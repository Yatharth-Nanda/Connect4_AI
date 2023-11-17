# Connect4_AI
    # Connect Four Game with Minimax AI Player
    
## Run the game  by executing Playgame 


This Python script implements the Connect Four game with an AI player using the minimax algorithm. Below are key points about the script:

## 1. Game Implementation:
   - The Connect Four game is represented by the `FourConnect` class.
   - Players take turns making moves on a 6x7 grid.

## 2. Minimax AI Player:
   - The AI player is implemented in the `GameTreePlayer` class using the minimax algorithm.
   - Three evaluation functions are provided for assessing the game state.
   - Move ordering strategies (static move ordering) are employed for optimization.

## 3. Evaluation Functions:
   - Three evaluation functions are available, with the primary one (`evaluate_state`) calculating scores based on consecutive coins in rows, columns, and diagonals.
   - The provided evaluation function for Connect Four is a heuristic that assesses the game state by identifying
      consecutive sequences of 1s, 2s, 3s, and 4s in both horizontal, vertical, and diagonal directions. Each
      sequence length is weighted, with 1s multiplied by 1, 2s by 1000, 3s by 5000, and 4s (indicating a win) by
      1000000. The final score for the state is determined by subtracting the score with respect to Player 1 from
      the score with respect to Player 2.
      Importantly, the function incorporates a strategic consideration for winning states. If the state represents a
      win for player 2 (at least one consecutive sequence of 4), the function penalizes states with a higher
      number of pieces. It subtracts the count of single coins, double coins, triple coins, and quadruple coins
      with respective weights.
