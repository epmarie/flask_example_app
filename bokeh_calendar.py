# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 11:59:12 2018

@author: caoa
"""
import random
from itertools import cycle
from math import pi
import pandas as pd
from bokeh.models import ColumnDataSource, HoverTool, LogColorMapper, ColorBar
from bokeh.plotting import figure
import bokeh.palettes as palettes

#%% Data
weeks = [str(x) for x in range(1,15)]
days = list(reversed('MTWRFSU'))
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
data = pd.DataFrame([[random.randint(1,100) for x in range(len(weeks))] for x in range(len(days))],
                      index=days, columns=weeks)
df = pd.DataFrame(data.stack(), columns=['value']).reset_index()
df.columns = ['day','week','pct1']
df['pct2'] = df.apply(lambda x: int(x['week']) / x['pct1'], axis=1 ) 
cm = cycle(months)
df['month'] = [next(cm) for x in range(df.shape[0])]
df['x'] = df['week']
df['y'] = df['day']
df['xy'] = df['pct1']
source = ColumnDataSource(data=df)
colors = list(reversed(palettes.brewer['RdPu'][8]))
mapper = LogColorMapper(palette=colors, low=df['xy'].min(), high=df['xy'].max())
xdict = {'week':weeks, 'month':months}

#%% Calendar Heatmap
def create_calendar():
    TOOLS = "save"
    
    p = figure(title="Weekday Heatmap",
               x_range=weeks, y_range=days,
               x_axis_location="above", plot_width=600, plot_height=300,
               tools=TOOLS, toolbar_location='right')
    
    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "12pt"
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = pi/4 * 0
    p.xaxis.axis_label_text_align = 'center'
    p.min_border = 10
    p.min_border_left = 50
    
    p.rect('x','y', width=1, height=1, source=source, line_color=None,
           fill_color={'field':'xy', 'transform': mapper},
    )    
    
    # HoverTool
    hover = HoverTool(tooltips = [
        ('x', '@x'),
        ('y', '@y'),
        ('xy', '@xy'),
    ])
    p.add_tools(hover)
        
    # ColorBar
    color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="12pt",
                         location=(0,0)
    )
    p.add_layout(color_bar, 'right')
    
    return p
