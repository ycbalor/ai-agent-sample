import psycopg2
from psycopg2 import pool

# Initialize a connection pool
connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10, user='your_user', password='your_password', host='localhost', port='5432', database='your_database')

def get_user(username):
    """
    Retrieve a user's information from the database by username.

    Parameters:
    username (str): The username of the user to retrieve.

    Returns:
    tuple: A tuple containing the user's information if found, otherwise None.
    """
    conn = None
    result = None
    try:
        # Get a connection from the pool
        conn = connection_pool.getconn()
        with conn.cursor() as cursor:
            # Use parameterized query to prevent SQL injection
            query = "SELECT id, username, email FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Return the connection to the pool
        if conn:
            connection_pool.putconn(conn)
    return result