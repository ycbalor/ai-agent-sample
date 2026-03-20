from typing import Optional, Dict
import psycopg2
from psycopg2 import pool

# Initialize a connection pool
connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10, user='your_user', password='your_password', host='localhost', port='5432', database='your_database')

def get_user(username: str) -> Optional[Dict]:
    """
    Retrieve a user record from the database by username.

    :param username: The username of the user to retrieve.
    :return: A dictionary containing the user record, or None if not found.
    """
    conn = None
    try:
        # Get a connection from the pool
        conn = connection_pool.getconn()
        with conn.cursor() as cursor:
            # Use parameterized query to prevent SQL injection
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            if result:
                # Assuming the result is a tuple, convert it to a dictionary
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, result))
            return None
    finally:
        # Ensure the connection is returned to the pool
        if conn:
            connection_pool.putconn(conn)
