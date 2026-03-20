import hashlib
import bcrypt
from typing import Optional

# Assuming get_connection is defined elsewhere in the module
# from database_module import get_connection

class DatabaseConnectionPool:
    def __init__(self):
        self.pool = []  # Simplified connection pool

    def get_connection(self):
        if self.pool:
            return self.pool.pop()
        else:
            # Create a new connection if pool is empty
            return self.create_new_connection()

    def release_connection(self, conn):
        self.pool.append(conn)

    def create_new_connection(self):
        # Placeholder for actual connection creation logic
        return "new_connection"

# Create a global connection pool instance
connection_pool = DatabaseConnectionPool()


def create_user(username: str, password: str, email: str) -> Optional[str]:
    """
    Creates a new user in the database with the given username, password, and email.

    Parameters:
    - username (str): The username of the new user.
    - password (str): The password of the new user.
    - email (str): The email of the new user.

    Returns:
    - Optional[str]: Returns None if successful, or an error message if failed.
    """
    conn = connection_pool.get_connection()
    try:
        cursor = conn.cursor()
        # Use bcrypt for hashing passwords with a salt
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, hashed_password, email)
        )
        conn.commit()
    except Exception as e:
        return str(e)
    finally:
        connection_pool.release_connection(conn)
    return None