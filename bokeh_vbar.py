# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 11:57:25 2018

@author: caoa
"""
from random import randint
from itertools import cycle
from collections import defaultdict
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool, TapTool
from bokeh.models.callbacks import OpenURL
from bokeh.plotting import figure
from bokeh.io import show
import bokeh.palettes as palettes

#%% data
def get_data(n):
    colors = cycle(palettes.d3['Category20'][min(20,n)])
    data = defaultdict(list)
    for day in range(n):
        data['days'].append(str(day+1))
        data['ct'].append(randint(1,100))
        data['colors'].append(next(colors))    
    return data
    
#%% vertical bar chart
def create_bar_chart(days, w=900, h=300):
    data = get_data(days)
    xfactor = [str(x+1) for x in range(days)]
    source = ColumnDataSource(data)
     
    p = figure(title="Count per day", plot_width=w, plot_height=h, 
               x_range=xfactor, y_range=(0,100),
               toolbar_location="above", outline_line_color='black',
    )
    p.vbar(x='days', bottom=0, top='ct', source=source, width=0.8, 
           color=None, fill_color='colors')
    
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = "grey"
    p.ygrid.grid_line_alpha = 0.25
    p.yaxis.axis_label = "Count"
    p.xaxis.axis_label = "Days"
    p.xaxis.major_tick_line_color = None

    TOOLTIPS = [
        ("Day", "@days"),
        ("No.", "@ct"),
        ("color", "$color[swatch]:colors"),
    ]
    hovertool = HoverTool(tooltips=TOOLTIPS)
    p.add_tools(hovertool)
    taptool = TapTool(callback=OpenURL(url='../../scatter'))
    p.add_tools(taptool)
    
    return p

#%%
if __name__ == "__main__":
    plot = create_bar_chart(days=9)
    show(plot)