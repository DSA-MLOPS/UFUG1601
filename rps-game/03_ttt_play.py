import streamlit as st
import random
from db_util import db_execute_query, db_select_query
from code_util import execute_code

PASS_CODE = "1234" 

def find_winner(board):
    for i in range(3):
        if (board[i][0] == board[i][1] == board[i][2] != 0) or (board[0][i] == board[1][i] == board[2][i] != 0):
            return True
    if (board[0][0] == board[1][1] == board[2][2] != 0) or (board[0][2] == board[1][1] == board[2][0] != 0):
        return True
    # now check for a tie
    if 0 in sum(board, []):
        return False
    return "Tie"

def print_board(board):
    """
        1   2   3
      +---+---+---+
    0 |   | X | X |
      +---+---+---+
    1 | X | O | X |
      +---+---+---+
    2 | O | O | O |
      +---+---+---+
    """
    symbol_map = {0: " ", 1: "X", 2: "O"}
    str_board = "\n##  0   1   2\n"
    for i in range(3):
        str_board += "  +---+---+---+\n"
        line = f"{i} |"
        for j in range(3):
            line += f" {symbol_map[board[i][j]]} |"
        str_board += line + "\n"
    str_board += "  +---+---+---+\n"
    print(str_board)
    return str_board

def put_a_stone(board, x, y, stone):
    if board[x][y] == 0:
        board[x][y] = stone
        return board, True
    else:
        print(f"Spot {x},{y} is already occupied. Try another spot.")
        return board, False

# set global variable to save time and memory
STONE_INDEX = [(x, y) for x in range(3) for y in range(3)] 
def random_board(board):
    random_stone_num = random.randint(0, 9) # random stone number
    if random_stone_num != 0:
         for i in range(random_stone_num):
             random_stone = random.choice(STONE_INDEX) # (x, y)
             random_mark = random.choice([1, 2]) # 1 or 2
             board[random_stone[0]][random_stone[1]] = random_mark
             # if initialized winner, roll back 
             if find_winner(board):
                 board[random_stone[0]][random_stone[1]] = 0 
    return board

st.title("TTT Tournament")

student_records = db_select_query("SELECT * FROM students")
st.write("We have {} student codes.".format(len(student_records)))

# Show participants
st.markdown("### Participants")
for record in student_records:
    st.markdown("- {}".format(record[0]))  # record[0] is student_id
    
if len(student_records) < 2:
    st.warning("Need at least two student codes to start the tournament.")
else:
    passcode = st.text_input("Passcode:", type="password")
    if st.button("Start Tournament") and passcode == PASS_CODE:
        st.header("Tournament Results")
        random.shuffle(student_records)
        winner = list(student_records[0])
        
        for i in range(1, len(student_records)):
            board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            player1 = list(winner)
            player2 = list(student_records[i])
            st.markdown("### Round {}: {} vs {}".format(i, player1[0], player2[0]))
            print("### Round {}: {} (X) vs {} (O)".format(i, player1[0], player2[0]))

            # for version 2 
            # board = random_board(board)
            # st.markdown("**Random Initialized Board:**")
            # st.text(print_board(board))

            st.markdown("**======> Start Playing <======**")
            win_flag = False
            step = 1
            while(True):
                st.markdown(f"--------------- Step {step} ---------------")
                step += 1 
                # Execute the student 1 code of next_move() function to get their choice
                play1_code = f"{player1[1]}\nboard = {board}\nprint(next_move(board))"      
                player1_choice, _ = execute_code(play1_code) 
                play1_x, play1_y = eval(player1_choice) 

                board, valid_move = put_a_stone(board, play1_x, play1_y, 1)
                if not valid_move:
                    st.write(f"{player1[0]}: {player1_choice}")
                    st.write(f"{player1[0]} made an invalid move due to spot is already occupied. \
                             {player2[0]} wins and continues to the next round!")
                    st.text(print_board(board)) 
                    winner = player2
                    winner[2] += 1
                    win_flag = True 
                    break
                st.write(f"{player1[0]}: {player1_choice}")
                st.text(print_board(board))
                
                win_flag = find_winner(board)
                if win_flag:
                    if "Tie" != win_flag:
                        result = f"The winner is {player1[0]} and continues to the next round!"
                        winner = player1
                    else:
                        result = f"They are {win_flag}!"
                    st.write(result)
                    print(result, "\n")
                    break
 
                # Execute the student 2 code of next_move() function to get their choice
                play2_code = f"{player2[1]}\nboard = {board}\nprint(next_move(board))" 
                player2_choice, _ = execute_code(play2_code) 
                play2_x, play2_y = eval(player2_choice)
                
                board, valid_move = put_a_stone(board, play2_x, play2_y, 2)
                if not valid_move:
                    st.write(f"{player2[0]}: {player2_choice}")
                    st.write(f"{player2[0]} made an invalid move due to spot is already occupied. \
                             {player1[0]} wins and continues to the next round!")
                    st.text(print_board(board)) 
                    winner = player1
                    winner[2] += 1
                    win_flag = True 
                    break  
                st.write(f"{player2[0]}: {player2_choice}")
                st.text(print_board(board))

                win_flag = find_winner(board)
                if win_flag:
                    if "Tie" != win_flag:
                        result = f"The winner is {player2[0]} and continues to the next round!"
                        winner = player2
                    else:
                        result = f"They are {win_flag}!"
                    st.write(result)
                    print(result, "\n")
                    break

            # Update the database
            if win_flag and win_flag!="Tie":
                db_execute_query("UPDATE students SET score = ? WHERE student_id = ?", (winner[2], winner[0]))  
        st.header("Tournament Standings")
        student_records = db_select_query("SELECT * FROM students ORDER BY score DESC")
        for record in student_records:
            st.write(f"{record[0]}: {record[2]}")

