import streamlit as st
import sqlite3
import random
import requests
from PIL import Image

PISTON_URL = "https://emkc.org/api/v2/piston/execute" 
PASS_CODE = "1234" 

# Initialize SQLite database
conn = sqlite3.connect('student_database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS students
             (student_id text, code text, score integer)''')

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



# Function to execute code using Piston API
def execute_code(code):
    # Prepare the payload for the Piston API
    payload = {
        "language": "py3",
        "version": "3.10.0",
        "files": [
            {
                "name": "my_cool_code.py",  # You can change the filename if needed
                "content": code  # Pass the code as content
            }
        ],
        "compile_timeout": 10000,
        "run_timeout": 3000,
        "compile_memory_limit": -1,
        "run_memory_limit": -1,
    }

    # Make a POST request to the Piston API
    piston_api_url = "https://emkc.org/api/v2/piston/execute"  # Replace with the actual API URL
    response = requests.post(piston_api_url, json=payload)
        
    if response.status_code == 200:
        data = response.json()
        stdout_output = data.get("run", {}).get("stdout", "").strip()
        stderr_output = data.get("run", {}).get("stderr", "").strip()

        if stderr_output:
            return None, stderr_output  # If there's stderr output, return it as error
        else:
            return stdout_output, None  # If no stderr output, return stdout output and None as error
    else:
        return None, None


page = st.sidebar.selectbox("Select a page:", ("Home", "Upload Student Code", "Start Tournament", "Reset Database"))

if page == "Upload Student Code":
    st.title("Upload Student Code")
    st.write("Please enter your student ID and Python code with the rps() function below.")

    student_id = st.text_input("Student ID:")
    student_code = st.text_area("Write program that prints out 'rock', 'scissors', or 'paper'")

    if st.button("Upload Code"):
        if student_id and student_code:
            test_output, error = execute_code(student_code)
            if error:
                st.error(f"Code execution failed: {error}")
            elif test_output is not None:
                st.success(f"Code execution successful: {test_output}")
                c.execute('SELECT * FROM students WHERE student_id=?', (student_id,))
                row = c.fetchone()
                if row is None:
                    c.execute("INSERT INTO students VALUES (?, ?, 0)", (student_id, student_code))
                    conn.commit()
                    st.success("Code uploaded successfully!")
                else:
                    c.execute("UPDATE students SET code = ? WHERE student_id = ?", (student_code, student_id))
                    conn.commit()
                    st.success("Code updated successfully!")
            else:
                st.error("Code execution failed. Please check your code.")

elif page == "Start Tournament":
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

# Rest of your code...

elif page == "Reset Database":
    st.title("Reset Database")
    st.write("Please enter the passcode to reset the database.")

    passcode = st.text_input("Passcode:", type="password")

    if st.button("Delete All Records"):
        if passcode == PASS_CODE:
            c.execute("DELETE FROM students")
            conn.commit()
            st.success("Database reset successfully!")
        else:
            st.error("Incorrect passcode, please try again.")