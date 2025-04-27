## Imports ##

# System Path #
import os
import sys 

# Add dsci_550_a1 to base path. Lets you project functions #
parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(parent_dir)

# Misc Data Handling #
import pandas as pd
import numpy as np
import datetime
import re
import json 

# Dates #
from datetime import date 
def parse_date(s): 
    return date(*map(int, s.split('-'))) 

# Runtime #
import time
from tqdm import tqdm 

# Iterators #
import collections
import ast
import random

# Flight Trajectory Functions #
from dsci_550_a1.flightFunctions import *

# Plotly #
import plotly.graph_objects as go
import plotly.express as px

# Dash #
import dash
from dash import dcc, html, Input, Output

# Helper Functions #
from dsci_550_a3.dg_viz import hp_interactive_globe
from dsci_550_a3.dg_query import filter_hp_df, get_legend_items
from dsci_550_a3.dg_dataLoader import load_all_data


## Load Data and Define Holidays
(
    hp_df,
    route_df,
    airport_df,
    flight_intersections,
    airport_intersections
) = load_all_data()

holidays = [
    {"label": "New Year's Day", "value": "1000-1-1"},
    {"label": "Valentine's Day", "value": "1000-2-14"}, 
    {"label": "St. Patrick's Day", "value": "1000-3-17"},
    {"label": "April Fool's", "value": "1000-4-1"}, 
    {"label": "Easter", "value": "1000-4-20"},
    {"label": "Independence Day", "value": "1000-7-4"},
    {"label": "Halloween", "value": "1000-10-31"},
    {"label": "Thanksgiving", "value": "1000-11-23"},
    {"label": "Christmas Eve", "value": "1000-12-24"},
    {"label": "Christmas Day", "value": "1000-12-25"},
    {"label": "New Year's Eve", "value": "1000-12-31"},
]

## Initialize Dash app
app = dash.Dash(__name__)

## Define layout
app.layout = html.Div([
    html.H1("Haunted Flights Explorer"),

    html.Div([
        html.Div([
            html.Label("Select State:"),
            dcc.Dropdown(
                id='state-dropdown',
                options=[{'label': s, 'value': s} for s in sorted(get_legend_items(hp_df, 'State'))],
                placeholder="Select a State"
            ),

            html.Label("Select Event Type:"),
            dcc.Dropdown(
                id='event-type-dropdown',
                options=[{'label': s, 'value': s} for s in sorted(get_legend_items(hp_df, 'Event_Type'))],
                placeholder="Select Event Type"
            ),

            html.Label("Select Apparition Type:"),
            dcc.Dropdown(
                id='apparition-type-dropdown',
                options=[{'label': s, 'value': s} for s in sorted(get_legend_items(hp_df, 'Apparition_Type'))],
                placeholder="Select Apparition Type"
            ),
            html.Label("Color Locations by: "),
            dcc.Checklist(
                id='legend-toggle',
                options=[{'label': 'Event Type', 'value': 'Event_Type'}],
                value=[],
                labelStyle={'display': 'block'}
            ),   
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    
        html.Div([

            html.Label("Select Date (Year):"),
            dcc.DatePickerRange(
                id='haunting-date-range',
                min_date_allowed=datetime.date(1000, 1, 1),
                max_date_allowed=datetime.date.today(),
                initial_visible_month=datetime.date(2025, 1, 1),
                start_date_placeholder_text="Start Date",
                end_date_placeholder_text="End Date"
            ),

            html.Label("Select Holiday:"),
            dcc.Dropdown(
                id='holiday-dropdown',
                options=holidays,
                placeholder="Optional:; Select Holiday"
            )
        ], style={'width': '48%', 'display': 'inline-block', 'paddingLeft': '20px', 'verticalAlign': 'top'}),
        
    
    ]),
    
    dcc.Graph(id='geo-plot')

])



@app.callback(
    Output('geo-plot', 'figure'),
    Input('state-dropdown', 'value'),
    Input('event-type-dropdown', 'value'),
    Input('apparition-type-dropdown', 'value'),
    Input('haunting-date-range', 'start_date'),
    # Input('year-range-slider', 'value'),
    # Input('specific-date-picker', 'date'),
    Input('holiday-dropdown', 'value'),
    Input('legend-toggle', 'value'),
)
def update_figure(state, event_type, apparition_type, haunt_date_range, holiday, legend_arg):
#def update_figure(hp_df, route_df, airport_df, flight_intersections, airport_intersections,state, event_type, apparition_type, haunt_date_range, holiday, legend_arg):
    if not legend_arg:
        legend_arg = {'Event_Type': get_legend_items(hp_df, 'Event_Type')} 
    
    filtered_hp_df, filtered_route_df, filtered_airport_df = filter_hp_df(
        hp_df,
        route_df,
        airport_df,
        flight_intersections,
        airport_intersections,
        state,
        event_type,
        apparition_type,
        haunt_date_range,
        holiday,
    )


    return hp_interactive_globe(filtered_hp_df, filtered_route_df, filtered_airport_df, legend_arg)



if __name__ == '__main__':
    app.run(debug=True)