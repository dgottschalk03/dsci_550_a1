## Imports ##

# System Path #
import os, sys, inspect

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
from dash import dcc, html, Input, Output, ctx

# Helper Functions #
from dsci_550_a3.dg_viz import hp_interactive_globe
from dsci_550_a3.dg_query import filter_hp_df, get_legend_items
from dsci_550_a3.dg_dataLoader import load_all_data

hpimg_directory = '../data/generated_images'

## Load Data and Define Holidays
(
    hp_df,
    route_df,
    airport_df,
    flight_intersections,
    airport_intersections
) = load_all_data(hpimg_directory)

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
                id='State',
                options=[{'label': s.replace('_', ' '), 'value': s} for s in sorted(get_legend_items(hp_df, 'State'))],
                multi = True,
                placeholder="Select a State"
            ),

            html.Label("Select Event Type:"),
            dcc.Dropdown(
                id='Event_Type',
                options=[{'label': s.replace('_', ' '), 'value': s} for s in sorted(get_legend_items(hp_df, 'Event_Type'))],
                multi = True,
                placeholder="Select Event Type"
            ),

            html.Label("Select Apparition Type:"),
            dcc.Dropdown(
                id='Apparition_Type',
                options=[{'label': s.replace('_', ' '), 'value': s} for s in sorted(get_legend_items(hp_df, 'Apparition_Type'))],
                multi = True,
                placeholder="Select Apparition Type"
            ),
            html.Label("Color Locations by: "),
            dcc.Dropdown(
                id='legend-toggle',
                options=[{'label': 'Event Type', 'value': 'Event_Type'},
                         {'label': 'Apparition Type', 'value': 'Apparition_Type'},
                         {'label': 'Time of Day', 'value': 'Time_of_Day'},
                         {'label': 'Audio Evidence', 'value': 'Audio_Evidence'},
                         {'label': 'Visual Evidence', 'value': 'Visual_Evidence'},
                         {'label': 'High Traffic Flight', 'value': 'Flight_HighTraffic'},
                         {'label': 'Airport Proximity', 'value': 'Aerodrome_Proximity'}
                ],
                value='Event_Type',
                clearable = False,
                style={'width': '50%'}
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
    Input('State', 'value'),
    Input('Event_Type', 'value'),
    Input('Apparition_Type', 'value'),
    Input('haunting-date-range', 'start_date'),
    # Input('year-range-slider', 'value'),
    # Input('specific-date-picker', 'date'),
    Input('holiday-dropdown', 'value'),
    Input('legend-toggle', 'value'),
)
def update_figure(state, event_type, apparition_type, haunt_date_range, holiday, legend_arg):
    
    # extract triggered arguments from callback
    triggered_inputs = {k.split('.')[0]: v for k, v in ctx.inputs.items()}
    # additional arguments displayed on hover
    additional_args = [arg for arg, v in triggered_inputs.items() if arg != 'legend-toggle' and v is not None]

    
    # define coloring
    legend_arg = {legend_arg: get_legend_items(hp_df, legend_arg)}

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

    return hp_interactive_globe(filtered_hp_df, filtered_route_df, filtered_airport_df, coloring = legend_arg, additional_tags = additional_args)



if __name__ == '__main__':
    app.run(debug=True)