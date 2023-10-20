import streamlit as st
import random
from db_util import c, conn
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


st.title("Rock-Paper-Scissors Tournament")

hello_world, _ = execute_code("print('Hello World!')")
st.write(hello_world)

c.execute("SELECT * FROM students")
student_records = c.fetchall()
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
            player1 = list(winner)
            player2 = list(student_records[i])

            # Execute the student code to get their choice
            player1_choice, _ = execute_code(player1[1])  # player1[1] is code
            player2_choice, _ = execute_code(player2[1])  # player2[1] is code
            
            player_1_student_id = player1[0]  # player1[0] is student_id
            player_2_student_id = player2[0]  # player2[0] is student_id

            st.write(f"{player_1_student_id}: {player1_choice}")
            st.write(f"{player_2_student_id}: {player2_choice}")

            result = rps(player1_choice, player2_choice)

            # Update the scores
            
            if result == 1 or result == 0:    
                player1[2] = player1[2] + 1  # player1[2] is score
                winner = player1
            elif result == 2:
                player2[2] = player2[2] + 1  # player2[2] is score
                winner = player2
                
            st.write(f"Winner: {winner[0]}, Score: {winner[2]}")
            c.execute("UPDATE students SET score = ? WHERE student_id = ?", (winner[2], winner[0]))
            conn.commit()
                
        st.header("Tournament Standings")
        c.execute("SELECT * FROM students ORDER BY score DESC")
        student_records = c.fetchall()
        for record in student_records:
            st.write(f"{record[0]}: {record[2]}")

