"""This module is used to get the chart representation of a stock"""

import yfinance as yf
import datetime as dt
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html


def _get_df(stock_symbol, days):
    """Returns a data-frame object containing the relevant details of the stock"""

    end = dt.datetime.today()
    start = end - dt.timedelta(days=days)

    df = yf.download(stock_symbol, start=start, end=end)

    # Indicates whether the stock went up or down each day.
    df["Status"] = ['Increase' if c > o
                    else ('Decrease' if c < o
                          else 'Equal')
                    for c, o in zip(df.Close, df.Open)]

    # The middle between the start and the end of each day.
    df["Middle"] = (df.Open + df.Close) / 2
    # The difference between the start and the end of each day.
    df["Height"] = abs(df.Close - df.Open)
    return df


def _get_plot(df, stock):
    """Returns a plot based on the data-frame of the stock using the Bokeh library"""

    hours_12 = 12*60*60*1000

    # Setting up the graph figure object.
    plot = figure(x_axis_type='datetime', width=1000, height=300, sizing_mode='scale_width')
    plot.title.text = stock
    plot.grid.grid_line_alpha = 1

    # A line representing the entire range of the stock each day.
    plot.segment(df.index, df.High, df.index, df.Low, color="Black")

    # A rectangular representing the increase\decrease of the stock
    # between the start and the end of each day.
    plot.rect(df.index[df.Status == "Increase"], df.Middle[df.Status == "Increase"],
              hours_12, df.Height[df.Status == "Increase"], fill_color="#CCFFFF", line_color="black")

    plot.rect(df.index[df.Status == "Decrease"], df.Middle[df.Status == "Decrease"],
              hours_12, df.Height[df.Status == "Decrease"], fill_color="#FF3333", line_color="black")
    return plot


def chart(stock, stock_symbol, days):
    df = _get_df(stock_symbol, days)
    plot = _get_plot(df, stock)
    html = file_html(plot, CDN, "my plot")
    return html
