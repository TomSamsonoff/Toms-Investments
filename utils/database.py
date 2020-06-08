"""This module is used to interact with the database"""

from .database_connection import DatabaseConnection


# Creating the table if it doesn't exist.
with DatabaseConnection('posts.db') as connection:
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS posts(id INTEGER PRIMARY KEY, title TEXT, content TEXT)')


def all_posts():
    """returns all the posts as a dictionary."""

    with DatabaseConnection('posts.db') as connection:
        cursor = connection.cursor()
        posts_lst = cursor.execute('SELECT * FROM posts').fetchall()
        if not posts_lst:
            return {}
        posts = {id: {'title': title, 'content': content} for (id, title, content) in posts_lst}
        return posts


def create_post(title, content):
    with DatabaseConnection('posts.db') as connection:
        cursor = connection.cursor()
        cursor.execute('INSERT INTO posts(title, content) VALUES (?,?)', (title, content))


def delete_post(post_id):
    with DatabaseConnection('posts.db') as connection:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM posts WHERE id=?', [str(post_id)])

