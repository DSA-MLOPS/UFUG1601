## Welcome to Tic-Tac-Toe Game
This app is made with [Streamlit](https://streamlit.io/). 
You can access our Tic-Tac-Toe Tournament platform at [https://tictactoe-john.streamlit.app](https://tictactoe-john.streamlit.app/home).

### Step 1: Upload Code

Implement the `def next_move(board)` function which represents how to generate the next best position to win the game in Python and upload it to our platform. For example,
```python
### we will pass board (3x3 list)
# 0: nothing
# 1: X (letter X)
# 2: Y (letter Y)
#
# You need to return x, y

def next_move(board):
    import random
    while True:
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        if board[x][y] == 0:
            return x, y
    return 0, 0
```
### Step 2: Play Game

**Tournament Results** 

Round 1: John vs Winner
======> Start Playing <======

--------------- Step 1 ---------------

John: (2, 0)
```python
##  0   1   2
  +---+---+---+
0 |   |   |   |
  +---+---+---+
1 |   |   |   |
  +---+---+---+
2 | X |   |   |
  +---+---+---+
```

Winner: (0, 0)
```python
##  0   1   2
  +---+---+---+
0 | O |   |   |
  +---+---+---+
1 |   |   |   |
  +---+---+---+
2 | X |   |   |
  +---+---+---+
--------------- Step 2 ---------------
```

John: (2, 1)
```python
##  0   1   2
  +---+---+---+
0 | O |   |   |
  +---+---+---+
1 |   |   |   |
  +---+---+---+
2 | X | X |   |
  +---+---+---+
```

Winner: (2, 2)
```python
##  0   1   2
  +---+---+---+
0 | O |   |   |
  +---+---+---+
1 |   |   |   |
  +---+---+---+
2 | X | X | O |
  +---+---+---+
```
--------------- Step 3 ---------------

John: (1, 0)
```python
##  0   1   2
  +---+---+---+
0 | O |   |   |
  +---+---+---+
1 | X |   |   |
  +---+---+---+
2 | X | X | O |
  +---+---+---+
```

Winner: (1, 1)
```python
##  0   1   2
  +---+---+---+
0 | O |   |   |
  +---+---+---+
1 | X | O |   |
  +---+---+---+
2 | X | X | O |
  +---+---+---+
```
The winner is Winner and continues to the next round!

**Tournament Standings** 
```python
Sung: 24
John: 12
```

### Step 3: Reset Database
After playing for a long time, if you want to clear the database, you can click this button.

