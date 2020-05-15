from flask import Flask, render_template, request, redirect, url_for
from utils import database


app = Flask(__name__)

# posts = {
#     0: {
#         'title': 'First post',
#         'content': 'First post content'
#     }
# }


@app.route('/')
def home():
    return render_template('home.html', posts=database.all_posts())


@app.route('/post/<int:post_id>')
def post(post_id):
    # post = database.all_posts().get(post_id)
    cur_post = database.all_posts().get(post_id)
    if not cur_post:
        # return render_template('404.html', message=f'post number {post_id} was not found')
        return render_template('404.html', message=f'post number {post_id} was not found', posts=database.all_posts())
    # return render_template('post.html', post=post)
    return render_template('post.html', cur_post=cur_post, posts=database.all_posts(), post_id=post_id)


@app.route('/post/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        database.create_post(title, content)
        # post_id = len(posts)
        # posts[post_id] = {'title': title, 'content': content}
        # return redirect(url_for('post', post_id=post_id))
        return redirect(url_for('home'))
    return render_template('create.html', posts=database.all_posts())


@app.route('/delete/<int:post_id>')
def delete(post_id):
    database.delete_post(post_id)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
