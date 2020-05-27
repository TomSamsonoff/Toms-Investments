def stocks_graph():
    import yfinance as yf
    import datetime as dt
    from bokeh.plotting import figure, show, output_file
    from bokeh.resources import CDN
    from bokeh.embed import file_html

    end = dt.datetime.today()
    start = end - dt.timedelta(days=30)

    df = yf.download('A', start=start, end=end)

    df["Status"] = ['Increase' if c > o else ('Decrease' if c < o else 'Equal') for c, o in zip(df.Close, df.Open)]
    df["Middle"] = (df.Open + df.Close) / 2
    df["Height"] = abs(df.Close - df.Open)

    p = figure(x_axis_type='datetime', width=1000, height=300, sizing_mode='scale_width')
    p.title.text = "Google Stocks"
    p.grid.grid_line_alpha = 1

    hours_12 = 12 * 60 * 60 * 1000

    p.segment(df.index, df.High, df.index, df.Low, color="Black")

    p.rect(df.index[df.Status == "Increase"], df.Middle[df.Status == "Increase"],
           hours_12, df.Height[df.Status == "Increase"], fill_color="#CCFFFF", line_color="black")

    p.rect(df.index[df.Status == "Decrease"], df.Middle[df.Status == "Decrease"],
           hours_12, df.Height[df.Status == "Decrease"], fill_color="#FF3333", line_color="black")

    html = file_html(p, CDN, "my plot")
    return html
