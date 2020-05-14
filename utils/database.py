from .database_connection import DatabaseConnection


with DatabaseConnection('data.db') as connection:
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS posts(id integer primary key, title text, content text)')


def all_posts():
    with DatabaseConnection('data.db') as connection:
        cursor = connection.cursor()
        posts_lst = cursor.execute('SELECT * FROM posts').fetchall()
        if not posts_lst:
            return {}
        posts = {id: {'title': title, 'content': content} for (id, title, content) in posts_lst}
        return posts


def create_post(title, content):
    with DatabaseConnection('data.db') as connection:
        cursor = connection.cursor()
        last_id = cursor.execute("SELECT * FROM posts ORDER BY id DESC LIMIT 1").fetchone()
        if not last_id:
            id = 0
        else:
            id = last_id[0]+1
        cursor.execute('INSERT INTO posts VALUES(?,?,?)', (id, title, content))

