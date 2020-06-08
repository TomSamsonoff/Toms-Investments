"""This is where the flask web app pages are implemented."""

import io
from flask import Flask, render_template, request, redirect, url_for, send_file
from utils import database
from stocks.stocks_chart import chart
from real_estate.real_estate import RealEstate
from map.real_estate_map import RealEstateMap


app = Flask(__name__)


def get_stocks():
    with open('utils/stocks_symbols', 'r') as file:
        stocks = [row.split('$')[0].strip().rsplit(' ', 1) for row in file.readlines()]
    return dict(stocks)


def get_states():
    with open('utils/usa_states', 'r') as file:
        states = [row.strip().split(', ') for row in file.readlines()]
        return dict(states)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/post/<int:post_id>')
def post(post_id):
    """Renders the 'post.html' page along with all the posts.
    If the post id doesn't exist, renders the '404.html' error.
    """
    all_posts = database.all_posts()
    cur_post = all_posts.get(post_id)
    if not cur_post:
        return render_template('404.html', message=f'post number {post_id} was not found')
    return render_template('post.html', cur_post=cur_post, posts=database.all_posts(), post_id=post_id)


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    """Renders the 'blog.html' page along with all the posts.
    If the form was submitted, adds the new post to the database.
    """
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        database.create_post(title, content)
        return render_template('blog.html', posts=database.all_posts())
    return render_template('blog.html', posts=database.all_posts())


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Deletes the chosen post from the database."""

    database.delete_post(post_id)
    return redirect(url_for('blog'))


@app.route('/stocks', methods=['GET', 'POST'])
def stocks_graph():
    """Displays a graph representing the stock history based on the user's choice of
    stock and time-frame.
    """
    stocks = get_stocks()  # Getting a dict of all companies and their stock symbol.

    if request.method == "POST":
        days = int(request.form.get('days'))
        stock = request.form.get('stock')
        stock_symbol = stocks[stock]

        html = chart(stock, stock_symbol, days)
        return render_template('stocks.html', stocks=stocks.keys(), html=html)
    return render_template('stocks.html', stocks=stocks.keys())


@app.route('/real_estate', methods=['GET', 'POST'])
def real_estate():
    """Displays the top 20 properties in a table and in a map, based on the user's choice
    of US state using RealEstate class and RealEstateMap class.
    """

    global state
    all_states = get_states()  # Getting a dict of all US state and their abbreviations.

    if request.method == "POST":
        state = request.form.get('state')
        state_abbr = all_states[state]

        # Getting the top 20 properties of the chosen US state as a data-frame object.
        re = RealEstate(state_abbr)
        top_properties_df = re.top_properties

        count = re.listings_count  # Total number of listings
        table = top_properties_df.drop(['Link'], axis=1)
        web_map = RealEstateMap(top_properties_df)
        return render_template('real_estate.html', table=table.to_html(), webmap=web_map.get_html,
                               states=all_states.keys(), btn=render_template('download.html', count=count))
    return render_template('real_estate.html', states=all_states.keys())


@app.route('/download_file')
def download():
    """Downloading a CSV file of all the properties in the chosen US state."""

    all_states = get_states()
    state_abbr = all_states[state]

    # Getting all properties of the chosen US state as a data-frame object.
    re = RealEstate(state_abbr)
    all_properties_df = re.all_properties

    # Send_file only gets a saved file or a byte-like object
    # so instead of saving the file I'm extracting a byte-like object
    # out of the data-frame.
    props_b = str.encode(all_properties_df.to_csv(index=False))
    return send_file(io.BytesIO(props_b), attachment_filename=f'All {state} properties.csv',
                     as_attachment=True, cache_timeout=-1)


if __name__ == '__main__':
    app.run(debug=True)
