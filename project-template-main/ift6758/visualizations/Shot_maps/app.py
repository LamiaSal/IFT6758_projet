
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Lamia Salhi
    Course: IFT6758
    Python Version: 3.8
    
    This file is the entry point for our dash app.
'''

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import pandas as pd

import preprocess
import template

import plotly.graph_objects as go 
from plot import advance_plot

app = dash.Dash(__name__)
app.title = 'Test Visualization question 6'

season=20162017
plot_1 = advance_plot(f"../../../datasets/data_to_plot_per_{str(season)}-bis.csv","../../../figures/nhl_rink.png",season=season,sigma=3)
fig = plot_1.get_figure()


app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1('Shot maps of hockey match'),
        html.H2('From 2016/2017 to 2020/2021 seasons')
    ]),
    html.Main(className='viz-container', children=[
        dcc.Graph(
            id='shotmap',
            className='graph',
            figure=fig,
            config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False
            )
        ),
    ])
])

#app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter
