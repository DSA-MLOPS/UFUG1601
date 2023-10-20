import streamlit as st
import random
from db_util import db_execute_query, db_select_query
from code_util import execute_code

PASS_CODE = "1234" 

# Function to simulate the rock-paper-scissors game
def rps(player1, player2):
    choices = ['rock', 'paper', 'scissors']

    if player1 and type(player1) == str:
        player1 = player1.strip().lower()
    
    if player2 and type(player2) == str:
        player2 = player2.strip().lower()
    
    if player1 == player2:
        return 0
    
    if player1 not in choices:
        return 2
    
    if player2 not in choices:
        return 1
    
    elif (player1 == 'rock' and player2 == 'scissors') or \
         (player1 == 'paper' and player2 == 'rock') or \
         (player1 == 'scissors' and player2 == 'paper'):
        return 1
    else:
        return 2

def board_to_code(board):
    code = "board = "
    for i in range(3):
        for j in range(3):
            code += str(board[i][j])
    return code

# check whether the board has winner
def check_winner(board):
    # row
    for row in board:
        if row.count(1) == 3:
            return 1
        elif row.count(2) == 3:
            return 2
    # column
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == 1:
            return 1
        elif board[0][col] == board[1][col] == board[2][col] == 2:
            return 2
    # diag
    if board[0][0] == board[1][1] == board[2][2] == 1:
        return 1
    if board[0][0] == board[1][1] == board[2][2] == 2:
        return 2
    if board[0][2] == board[1][1] == board[2][0] == 1:
        return 1
    if board[0][2] == board[1][1] == board[2][0] == 2:
        return 2

    return -1

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
            st.markdown("### Round {}".format(i))
            board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            player1 = list(winner)
            player2 = list(student_records[i])

            while(True):
                # Execute the student code to get their choice
                # bord state to python code
                stub_code = "board = " + str(board) + "\n"
                main_code = """x, y = next_move(board) print(x, y)"""               
                player1_choice, _ = execute_code(stub_code + player1[1] + main_code)  # player1[1] is code
                play1_x, play1_y = player1_choice.split()
                play1_x = int(play1_x)
                play1_y = int(play1_y)
                # if they are 0, loss the game
                if board[play1_x][play1_y]!=0: break
                board[play1_x][play1_y] = 1
                
                player2_choice, _ = execute_code(stub_code + player2[1] + main_code)  # player2[1] is code
                play2_x, play2_y = player2_choice.split()
                play2_x = int(play2_x)
                play2_y = int(play2_y)
                # if they are 0, loss the game
                if board[play2_x][play2_y]!=0: break
                board[play2_x][play2_y] = 2
                
                player_1_student_id = player1[0]  # player1[0] is student_id
                player_2_student_id = player2[0]  # player2[0] is student_id

                st.write(f"{player_1_student_id}: {player1_choice}")
                st.write(f"{player_2_student_id}: {player2_choice}")
                
                # Judge the result: if there is a winner, break
                if check_winner(board) < 0: break
                if check_winner(board) == 1: 
                    winner = player1
                    winner[2] += 1
                    break
                if check_winner(board) == 2: 
                    winner = player2
                    winner[2] += 1
                    break

            # Update the database
            st.write(f"Winner: {winner[0]}, Score: {winner[2]}")
            db_execute_query("UPDATE students SET score = ? WHERE student_id = ?", (winner[2], winner[0]))
                
        st.header("Tournament Standings")
        student_records = db_select_query("SELECT * FROM students ORDER BY score DESC")
        for record in student_records:
            st.write(f"{record[0]}: {record[2]}")

