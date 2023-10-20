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
                main_code = """
x, y = next_move(board)
print(x, y)"""
                
                player1_choice, _ = execute_code(stub_code + player1[1] + main_code)  # player1[1] is code
                play1_x, play1_y = player1_choice.split()
                play1_x = int(play1_x)
                play1_y = int(play1_y)
                # if they are 0
                board[play1_x][play1_y] = 1
                
                player2_choice, _ = execute_code(stub_code + player2[1] + main_code)  # player2[1] is code
                play2_x, play2_y = player2_choice.split()
                play2_x = int(play2_x)
                play2_y = int(play2_y)
                # if they are 0
                board[play2_x][play2_y] = 2
                
                # Judge the result
                # if thee is a winner, break
                
                player_1_student_id = player1[0]  # player1[0] is student_id
                player_2_student_id = player2[0]  # player2[0] is student_id

                st.write(f"{player_1_student_id}: {player1_choice}")
                st.write(f"{player_2_student_id}: {player2_choice}")


            # Update the scores
            # findout winner and update the score
                
            st.write(f"Winner: {winner[0]}, Score: {winner[2]}")
            db_execute_query("UPDATE students SET score = ? WHERE student_id = ?", (winner[2], winner[0]))
                
        st.header("Tournament Standings")
        student_records = db_select_query("SELECT * FROM students ORDER BY score DESC")
        for record in student_records:
            st.write(f"{record[0]}: {record[2]}")

