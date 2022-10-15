
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Lamia Salhi
    Course: IFT6758
    Python Version: 3.8
    
    This file is the entry point for our dash app.
'''

import dash
from dash import dcc
import dash_html_components as html
#import dash_core_components as dcc
from dash.dependencies import Input, Output

import pandas as pd

import preprocess
import template

import plotly.graph_objects as go 
from plot import advance_plot

app = dash.Dash(__name__)
app.title = 'Test Visualization question 6'

seasons=[20162017,20172018, 20182019, 20192020,20202021]
children_main=[]
for season in seasons : 
    plot = advance_plot(f"../../../datasets/data_to_plot_per_{str(season)}.csv","../../../figures/nhl_rink.png",season=season,sigma=2)
    fig = plot.get_figure()
    children_main.append( dcc.Graph(
                id=f'shotmap_{season}',
                className='graph',
                figure=fig,
                config=dict(
                    scrollZoom=False,
                    showTips=False,
                    showAxisDragHandles=False,
                    doubleClick=False,
                    displayModeBar=False
                ),
            ))

app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1('Shot maps of hockey match'),
        html.H2('From 2016/2017 to 2020/2021 seasons')
    ]),
    html.Main(className='viz-container', children=children_main)
])

#app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter
