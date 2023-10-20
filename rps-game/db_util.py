import sqlite3

DATABASE_NAME = 'student_database.db'

def db_execute_query(query, params=None, database_name=DATABASE_NAME):
    """
    Execute a query with parameters.

    :param query: SQL query to execute.
    :param params: Optional tuple of parameters to replace within the query.
    """
    conn = None
    try:
        # Open connection
        conn = sqlite3.connect(database_name)
        c = conn.cursor()

        # Execute query with parameters and commit changes
        if params:
            c.execute(query, params)
        else:
            c.execute(query)
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close connection
        if conn:
            conn.close()

def db_select_query(query, database_name=DATABASE_NAME):
    """
    Execute a selection query, such as a SELECT statement.

    :param query: SQL query to execute.
    :return: Fetched results.
    """
    rows = []
    conn = None
    try:
        # Open connection
        conn = sqlite3.connect(database_name)
        c = conn.cursor()

        # Execute query and fetch results
        c.execute(query)
        rows = c.fetchall()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close connection
        if conn:
            conn.close()
    return rows

# Sample usage of the db_util functions
if __name__ == '__main__':
    execute_query('''CREATE TABLE IF NOT EXISTS students
                (student_id text, code text, score integer)''')

    # Insert a student record
    execute_query('''INSERT INTO students (student_id, code, score) VALUES
                ('123', 'XYZ', 90)''')

    # Select records
    rows = select_query("SELECT * FROM students")
    for row in rows:
        print(row)
