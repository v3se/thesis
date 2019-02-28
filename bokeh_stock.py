# myapp.py

from random import random
from bokeh.palettes import RdYlBu3
from math import pi
import pandas as pd
from bokeh.plotting import figure, show, output_file, curdoc
from bokeh.models import ColumnDataSource
from bokeh.layouts import widgetbox, column
from bokeh.models.widgets import CheckboxGroup, Select


def checkbox_handler(attr, old, new):
    sma = p.select_one({'name': 'sma'})
    if not old:
        print("on")
        sma.visible = True
    else:
        print("off")
        sma.visible = False
        

def date_handler(attr, old, new):
    #get the elements
    sma = p.select_one({'name': 'sma'})
    segment = p.select_one({'name': 'segment'})
    bar1 = p.select_one({'name': 'bar1'})
    bar2 = p.select_one({'name': 'bar2'})
    print("end_date selected")
    #get the source data
    df = pd.read_csv("CSCO.csv")
    print(new)
    #convert to datetime
    df_date = pd.to_datetime(df["date"])
    #select range
    mask = (df_date > new) # & (df_date <= end_datei
    df["date"] = df_date
    df = df.loc[mask]
    #define the candlechart data
    inc = df.close > df.open
    dec = df.open > df.close
    #modify the source data
    new_src = ColumnDataSource(df)
    sourceInc=ColumnDataSource(ColumnDataSource.from_df(df.loc[inc]))
    sourceDec=ColumnDataSource(ColumnDataSource.from_df(df.loc[dec]))
    bar1.data_source.data = sourceInc.data
    bar2.data_source.data = sourceDec.data
    segment.data_source.data = new_src.data
    #calculate the mean and substitute the sma source data with it
    df["close"] = df["close"].rolling(window=20).mean()
    src_line = ColumnDataSource(df)
    sma.data_source.data = src_line.data
    
    #create_plot(df["date"], df, src, inc, dec)
    
def create_plot(df_date, df, src, inc, dec):

    sourceInc=ColumnDataSource(ColumnDataSource.from_df(df.loc[inc]))
    sourceDec=ColumnDataSource(ColumnDataSource.from_df(df.loc[dec]))

    w = 12*60*60*1000

    TOOLTIPS = [
        ("Open", "@open"),
        ("Close", "@close"),
        ("High", "@high"),
        ("Low", "@low")
    ]

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"
    global p
    p = figure(x_axis_type="datetime", tools=TOOLS, tooltips=TOOLTIPS, plot_width=1000, title = "CSCO Stock")
    p.xaxis.major_label_orientation = pi/4
    p.grid.grid_line_alpha=0.5
    p.segment(source = src, x0='date', y0='high', x1='date', y1='low', color="black", name='segment')
    p.vbar(source = sourceInc, x='date', bottom='open', width=w, top='close', fill_color="#D5E1DD", line_color="black", name ='bar1')
    p.vbar(source = sourceDec, x='date', top='open', width=w, bottom='close', fill_color="#F2583E", line_color="black", name='bar2')
    df["close"] = df["close"].rolling(window=20).mean()
    src_line = ColumnDataSource(df)
    p.line(source = src_line, x='date', y='close', name='sma')
    curdoc().add_root(column(checkbox_group, end_date, p))

checkbox_group = CheckboxGroup(
        labels=["Simple Moving Average (20)"], active=[0, 1])
checkbox_group.on_change("active", checkbox_handler)


df = pd.read_csv("CSCO.csv")
date_list_asc = df["date"].tolist()
date_desc = df["date"].iloc[::-1]
date_list_desc = date_desc.tolist()

df["date"] = pd.to_datetime(df["date"])
global df_date
df_date = pd.to_datetime(df["date"])

inc = df.close > df.open
dec = df.open > df.close
src = ColumnDataSource(df)
#start_date = Select(title="Start date:", value="foo", options=date_list_asc)
end_date = Select(title="End date:", value="foo", options=date_list_desc)
end_date.on_change("value", date_handler)


create_plot(df_date, df, src, inc, dec)
