import sqlite3
from typing import List, Dict, Any

# Assuming get_connection is a function that returns a database connection
# For the purpose of this example, we'll define a mock get_connection function.
def get_connection():
    return sqlite3.connect(':memory:')


def get_users_with_posts(user_ids: List[int]) -> List[Dict[str, Any]]:
    """
    Retrieves users and their associated posts from the database.

    Parameters:
    user_ids (List[int]): A list of user IDs to fetch data for.

    Returns:
    List[Dict[str, Any]]: A list of dictionaries, each containing a user and their posts.
    """
    users_with_posts = []
    with get_connection() as conn:
        cursor = conn.cursor()
        # Fetch all users in one query
        cursor.execute("SELECT * FROM users WHERE id IN ({})".format(
            ','.join('?' for _ in user_ids)), user_ids)
        users = cursor.fetchall()

        # Fetch all posts for the given user_ids in one query
        cursor.execute("SELECT * FROM posts WHERE user_id IN ({})".format(
            ','.join('?' for _ in user_ids)), user_ids)
        posts = cursor.fetchall()

        # Group posts by user_id
        posts_by_user = {}
        for post in posts:
            user_id = post['user_id']
            if user_id not in posts_by_user:
                posts_by_user[user_id] = []
            posts_by_user[user_id].append(post)

        # Combine users with their posts
        for user in users:
            user_id = user['id']
            user_posts = posts_by_user.get(user_id, [])
            users_with_posts.append({"user": user, "posts": user_posts})

    return users_with_posts
