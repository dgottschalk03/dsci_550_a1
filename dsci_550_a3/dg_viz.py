## Imports ##

# System Path #
import os
import sys 

# Misc Data Handling #
import pandas as pd
from datetime import date 

# Flight Trajectory Functions #
from dsci_550_a1.flightFunctions import *

# Plotly #
import plotly.graph_objects as go
import plotly.express as px
import textwrap



## Main Visualization Function ##
def hp_interactive_globe(hp_df, route_df, airport_df, legend_arg):

    # Initialize trace lists
    all_traces = []

    legend_key = list(legend_arg.keys())[0]
    legend_values = [v for v in legend_arg[legend_key]]

    # Color Palette
    plot_colors = [
    'rgb(102,179,92)',
    'rgb(14,106,71)',
    'rgb(188,20,102)',
    'rgb(121,210,214)',
    'rgb(74,202,87)',
    'rgb(116,99,103)',
    'rgb(151,130,149)',
    'rgb(52,1,87)',
    'rgb(235,157,37)',
    'rgb(129,191,187)',
    'rgb(20,160,203)',
    'rgb(57,21,252)',
    'rgb(235,88,48)',
    'rgb(218,58,254)',
    'rgb(169,255,219)',
    'rgb(187,207,14)',
    'rgb(189,189,174)']


    ## Haunted Places Trace 
    
    # Iterate through legend values
    for i, val in enumerate(legend_values):
        
        # Filter Dataset
        hp_df_filtered = hp_df.loc[hp_df[f'{legend_key}'].str.contains(val, na=False)].copy()
        hp_df_filtered['Formatted_Description'] = hp_df_filtered['Description'].apply(
        lambda x: "<br>".join(textwrap.wrap(x, width=50))
    )
        # Add Trace
        trace = (go.Scattergeo(
            locationmode = 'USA-states',
            lon = hp_df_filtered['Longitude'],
            lat = hp_df_filtered['Latitude'],
            hoverinfo = 'text',
            text = hp_df_filtered.apply(lambda row: 
                                        f"<b>Haunting Type</b>: {row[f'{legend_key}']}<br>"
                                        f"<b>index</b>:{row['Haunted_Places_Id']} | <b>Location</b>: {row['Location']}<br>"
                                        f"<b>Number of Intersecting Flights</b>: {row['Flight_Intersection_Count']} | <b>Number of Nearby Airports</b>: {row['Aerodrome_Count']}<br>"
                                        f"<b>Description</b>: {row['Formatted_Description']}", 
                                        axis=1),
            mode = 'markers',
            showlegend = True, 
            marker = dict(
                size = 4,
                color = plot_colors[i],
                opacity = 0.75
                ),
                name = val, 
                visible = True
            )
        )
        all_traces.append(trace)


    ## Flight Paths Traces

    lats_plot, lons_plot = [] , []

    for row in route_df.itertuples(index = False):   

        lats, lons = zip(*row.Flight_Path)
        lats, lons = list(lats), list(lons)

        lats_plot.extend(lats + [None])
        lons_plot.extend(lons + [None])

    # Add trace
    trace = (go.Scattergeo(
        lon= lons_plot,
        lat= lats_plot,
        mode='lines',
        line=dict(width=.5, color='red'),
        opacity = 0.2, 
        hoverinfo = 'skip', 
        name = "Flights",
        visible = False
    ))
    all_traces.append(trace)


    ## Airport Traces
    airport_types = airport_df['Type'].unique().tolist()

    # Bluescale Color Palette
    airport_plot_colors = {
    'heliport' :        "rgb(100,151,177)" ,
    'seaplane_base': 	"rgb(179,205,224)",
    'balloonport' : 	"rgb(179,205,224)",
    'small_airport' :  "rgb(0,91,150)"  ,
    'medium_airport' :	"rgb(3,57,108)",
    'large_airport':   "rgb(1,31,75)"
    }

    airport_proximity_dict = {
        "large_airport" : 55560,    # 30 nautical miles
        "medium_airport" : 9260,    # 5 nautical miles
        "small_airport" : 5556,     # 3 nautical miles
        "heliport":  2778,          # 1.5 nautical miles
        "seaplane_base" : 5556,     # 3 nautical miles
        "balloonport" : 5556        # 3 nautical miles
    }

    # Plot Trace
    for airport_type in airport_types:

        # Filter by airport type
        airport_df_filtered = airport_df.loc[airport_df['Type'] == airport_type]

        # Airport Marker 
        airport_marker = (go.Scattergeo(
        locationmode = 'USA-states',
        lon = airport_df_filtered['Longitude_Deg'],
        lat = airport_df_filtered['Latitude_Deg'],
        hoverinfo = 'text',
        text = airport_df_filtered.apply(lambda row: f"IATA Code: {row['Iata_Code']}<br>Name: {row['Name']}", axis=1),
        mode = 'markers',
        marker = dict(
            size = 2,
            color = airport_plot_colors[airport_type],
            opacity = 1
            ),
            name = airport_type,
            visible = False
        ))
        all_traces.append(airport_marker)

        # Airport Radius

        lats_plot, lons_plot = [] , []

        for airport in airport_df_filtered.itertuples():
            
            lats, lons = zip(*airport.Airport_Radius)
            lats, lons = list(lats), list(lons)

            lats_plot.extend(lats + [None])
            lons_plot.extend(lons + [None])
        
        airport_radii = (go.Scattergeo(
        locationmode = 'USA-states',
        lon = lons_plot,
        lat = lats_plot,
        hoverinfo = 'skip',
        mode = 'lines',
        line = dict(
            width = 1,
            color = airport_plot_colors[airport_type],
            dash = 'dot'
            ),
            name = airport_type,
            visible = False
        ))
        all_traces.append(airport_radii)




    ## Interactive Buttons 

    hp_buttons = [
            {
                "method": "restyle",
                "args" : [{"visible" : True}, [i for i, x in enumerate(all_traces) if x.name == val]], # When toggled on, checkbox shows already visible traces + haunted place specified in box
                "args2" : [{'visible':'legendonly'},[i for i,x in enumerate(all_traces) if x.name == val]], # When toggled off, checkbox removes haunted trace
                "label": val,
                "visible" : True, 

            }
            for val in legend_values
        ]

    hp_toggleAll = {
                "method": "restyle",
                "args" : [{"visible" : True}, [i for i, x in enumerate(all_traces) if x.name in legend_values]],
                "args2" : [{'visible':'legendonly'},[i for i,x in enumerate(all_traces) if x.name in legend_values]],
                "label": "Toggle All",
                "visible" : True, 

            }
    hp_buttons.append(hp_toggleAll) 


    ## Add Interactive Buttons for airports 

    airport_buttons = [
            {
                "method": "restyle",
                "args" : [{"visible" : True}, [i for i, x in enumerate(all_traces) if x.name == airport_type]],
                "args2" : [{'visible':'legendonly'},[i for i,x in enumerate(all_traces) if x.name == airport_type]],
                "label": airport_type,
                "visible" : True, 
            }
            for airport_type in airport_types
        ]

    # Toggle All Airports
    airport_toggleAll = {
                "method": "restyle",
                "args" : [{"visible" : True}, [i for i, x in enumerate(all_traces) if x.name in airport_types]],
                "args2" : [{'visible':'legendonly'},[i for i,x in enumerate(all_traces) if x.name in airport_types]],
                "label": "Toggle All",
                "visible" : True, 
            }
    airport_buttons.append(airport_toggleAll) 

    # Toggle All Flights 
    flights_toggleAll = {
                "method": "restyle",
                "args" : [{"visible" : True}, [i for i, x in enumerate(all_traces) if x.name == "Flights"]],
                "args2" : [{'visible':'legendonly'},[i for i,x in enumerate(all_traces) if x.name == "Flights"]],
                "label": "Flight Paths",
                "visible" : True, 

            }
    airport_buttons.append(flights_toggleAll)



    ## Final Conf 

    updateMenusConf = [
        {
            "buttons": hp_buttons,
            "direction" : "down",
            "showactive" : False,
            "x": 0.1,
            "y": 1.15,
            "xanchor" : "left",
            "yanchor" : "top", 
            "font": {"size" : 12},
            "type": "dropdown",
            "name": "Toggle Flags"
        },
        {
            "buttons": airport_buttons,
            "direction" : "down",
            "showactive" : True,
            "x": -.05,
            "y": 1.15,
            "xanchor" : "left",
            "yanchor" : "top", 
            "font": {"size" : 12},
            "type": "dropdown",
            "name": "Flight Toggle"
        }
        ]


    ## Create Plotly figure 
    fig = go.Figure(data = all_traces)


    fig.update_layout(
        title_text = 'Interactive Flight Map',
        showlegend = True,
        clickmode='event+select',
        hovermode = 'closest',
        geo = dict(
            scope = 'north america',
            projection_type = 'azimuthal equal area',
            showland = True,
            showcountries = True,
            showsubunits = True, 
            subunitcolor = "Black",
            landcolor = 'rgb(243, 243, 243)',
            countrycolor = 'rgb(204, 204, 204)',
        ),
        updatemenus = updateMenusConf
    )

    # Return figure
    return fig





def generate_formatted_textbox(row, primary_tag, additional_tags, separator="|"):
    """
    Generate a formatted HTML string for a row based on specified fields.

    Parameters:
    - row: A pandas Series (a single row of a DataFrame).
    - fields: List of fields (column names) to include.
    - bold_fields: List of fields to bold (optional; if None, all fields will be bolded).
    - separator: String separator between lines (default: "<br>").
    - extra_formatting: Optional dictionary {field: custom_format_string}, where
                        custom_format_string can use {value} as placeholder.

    Returns:
    - A formatted HTML string.
    """
    lines = []
    lines.append(f"<b>Location</b>: {row['Location']} | <b>{primary_tag}</b>: {row.get(primary_tag, "")}")

    if additional_tags:
        additional_tag_line = ['<b>Additional Tags:</b>'] + [f"{row.get(tag, '')}" for tag in additional_tags]
        lines.append(f" {separator} ".join(additional_tag_line))

    lines.append(f"<b>Number of Intersecting Flights</b>: {row['Flight_Intersection_Count']} | <b>Number of Nearby Airports</b>: {row['Aerodrome_Count']}<br>")
    lines.append(f"<b>Description</b>: {row['Formatted_Description']}")

    return "<br>".join(lines)
## Main Visualization Function ##
def hp_interactive_globe(hp_df, route_df, airport_df, coloring, additional_tags = None):
    # Initialize trace lists
    all_traces = []

    legend_key = list(coloring.keys())[0]
    legend_values = [v for v in coloring[legend_key]]

    # Color Palette
    plot_colors = {
    'dsci550_a3-1-hsla': 'rgb(116, 84, 190)', 'dsci550_a3-2-hsla': 'rgb(125, 133, 241)', 'dsci550_a3-3-hsla': 'rgb(58, 45, 113)', 'dsci550_a3-4-hsla': 'rgb(10, 188, 4)', 'dsci550_a3-5-hsla': 'rgb(77, 114, 23)', 
    'dsci550_a3-6-hsla': 'rgb(140, 215, 64)', 'dsci550_a3-7-hsla': 'rgb(237, 7, 7)', 'dsci550_a3-8-hsla': 'rgb(113, 3, 3)', 'dsci550_a3-9-hsla': 'rgb(188, 53, 4)',  'dsci550_a3-10-hsla': 'rgb(238, 114, 6)', 
    'dsci550_a3-11-hsla': 'rgb(241, 166, 74)', 'dsci550_a3-12-hsla': 'rgb(255, 137, 254)', 'dsci550_a3-13-hsla': 'rgb(116, 235, 148)', 'dsci550_a3-14-hsla': 'rgb(4, 214, 176)', 'dsci550_a3-15-hsla': 'rgb(65, 173, 240)', 
    'dsci550_a3-16-hsla': 'rgb(2, 100, 109)', 'dsci550_a3-17-hsla': 'rgb(1, 38, 59)', 'dsci550_a3-18-hsla': 'rgb(191, 176, 88)', 'dsci550_a3-19-hsla': 'rgb(34, 3, 1)', 'dsci550_a3-20-hsla': 'rgb(12, 12, 12)'
    }
        

    ## Haunted Places Trace 
    
    # Iterate through legend values
    for i, val in enumerate(legend_values):
        
        # Filter Dataset
        hp_df_filtered = hp_df.loc[hp_df[f'{legend_key}'].str.contains(val, na=False)].copy()
        hp_df_filtered['Formatted_Description'] = hp_df_filtered['Description'].apply(
        lambda x: "<br>".join(textwrap.wrap(x, width=50))
    )
        # Add Trace
        trace = (go.Scattergeo(
            locationmode = 'USA-states',
            lon = hp_df_filtered['Longitude'],
            lat = hp_df_filtered['Latitude'],
            hoverinfo = 'skip',
            customdata = np.stack([
                                hp_df_filtered.apply(lambda row: generate_formatted_textbox(
                                                row,
                                                primary_tag=f"{legend_key}",
                                                additional_tags=additional_tags,
                                            ), 
                                        axis=1),
            # customdata = np.stack([
            #                     hp_df_filtered.apply(lambda row: 
            #                             f"<b>Location</b>: {row['Location']} | <b>{legend_key}</b>: {row[f'{legend_key}']}<br>"
            #                             f"<b>Additional Tags</b>: {row['Haunted_Places_Id']} | <b>Location</b>: {row['Location']}<br>"
            #                             f"<b>Number of Intersecting Flights</b>: {row['Flight_Intersection_Count']} | <b>Number of Nearby Airports</b>: {row['Aerodrome_Count']}<br>"
            #                             f"<b>Description</b>: {row['Formatted_Description']}", 
            #                             axis=1),
                                ], axis = 1
            ),
            hovertemplate = (
                "%{customdata[0]}<br><br>"
            ),
            mode = 'markers',
            showlegend = True, 
            marker = dict(
                size = 4,
                color = plot_colors[f"dsci550_a3-{i+1}-hsla"],
                opacity = 0.75
                ),
                name = val, 
                visible = True
            )
        )
        all_traces.append(trace)


    ## Flight Paths Traces

    lats_plot, lons_plot = [] , []

    for row in route_df.itertuples(index = False):   

        lats, lons = zip(*row.Flight_Path)
        lats, lons = list(lats), list(lons)

        lats_plot.extend(lats + [None])
        lons_plot.extend(lons + [None])

    # Add trace
    trace = (go.Scattergeo(
        lon= lons_plot,
        lat= lats_plot,
        mode='lines',
        line=dict(width=.5, color='red'),
        opacity = 0.2, 
        hoverinfo = 'skip', 
        name = "Flights",
        visible = False
    ))
    all_traces.append(trace)


    ## Airport Traces
    airport_types = airport_df['Type'].unique().tolist()

    # Bluescale Color Palette
    airport_plot_colors = {
    'heliport' :        "rgb(100,151,177)" ,
    'seaplane_base': 	"rgb(179,205,224)",
    'balloonport' : 	"rgb(179,205,224)",
    'small_airport' :  "rgb(0,91,150)"  ,
    'medium_airport' :	"rgb(3,57,108)",
    'large_airport':   "rgb(1,31,75)"
    }

    airport_proximity_dict = {
        "large_airport" : 55560,    # 30 nautical miles
        "medium_airport" : 9260,    # 5 nautical miles
        "small_airport" : 5556,     # 3 nautical miles
        "heliport":  2778,          # 1.5 nautical miles
        "seaplane_base" : 5556,     # 3 nautical miles
        "balloonport" : 5556        # 3 nautical miles
    }

    # Plot Trace
    for airport_type in airport_types:

        # Filter by airport type
        airport_df_filtered = airport_df.loc[airport_df['Type'] == airport_type]

        # Airport Marker 
        airport_marker = (go.Scattergeo(
        locationmode = 'USA-states',
        lon = airport_df_filtered['Longitude_Deg'],
        lat = airport_df_filtered['Latitude_Deg'],
        hoverinfo = 'text',
        text = airport_df_filtered.apply(lambda row: f"IATA Code: {row['Iata_Code']}<br>Name: {row['Name']}", axis=1),
        mode = 'markers',
        marker = dict(
            size = 2,
            color = airport_plot_colors[airport_type],
            opacity = 1
            ),
            name = airport_type,
            visible = False
        ))
        all_traces.append(airport_marker)

        # Airport Radius

        lats_plot, lons_plot = [] , []

        for airport in airport_df_filtered.itertuples():
            
            lats, lons = zip(*airport.Airport_Radius)
            lats, lons = list(lats), list(lons)

            lats_plot.extend(lats + [None])
            lons_plot.extend(lons + [None])
        
        airport_radii = (go.Scattergeo(
        locationmode = 'USA-states',
        lon = lons_plot,
        lat = lats_plot,
        hoverinfo = 'skip',
        mode = 'lines',
        line = dict(
            width = 1,
            color = airport_plot_colors[airport_type],
            dash = 'dot'
            ),
            name = airport_type,
            visible = False
        ))
        all_traces.append(airport_radii)




    ## Interactive Buttons 

    hp_buttons = [
            {
                "method": "restyle",
                "args" : [{"visible" : True}, [i for i, x in enumerate(all_traces) if x.name == val]], # When toggled on, checkbox shows already visible traces + haunted place specified in box
                "args2" : [{'visible':'legendonly'},[i for i,x in enumerate(all_traces) if x.name == val]], # When toggled off, checkbox removes haunted trace
                "label": val,
                "visible" : True, 

            }
            for val in legend_values
        ]

    hp_toggleAll = {
                "method": "restyle",
                "args" : [{"visible" : True}, [i for i, x in enumerate(all_traces) if x.name in legend_values]],
                "args2" : [{'visible':'legendonly'},[i for i,x in enumerate(all_traces) if x.name in legend_values]],
                "label": "Toggle All",
                "visible" : True, 

            }
    hp_buttons.append(hp_toggleAll) 


    ## Add Interactive Buttons for airports 

    airport_buttons = [
            {
                "method": "restyle",
                "args" : [{"visible" : True}, [i for i, x in enumerate(all_traces) if x.name == airport_type]],
                "args2" : [{'visible':'legendonly'},[i for i,x in enumerate(all_traces) if x.name == airport_type]],
                "label": airport_type,
                "visible" : True, 
            }
            for airport_type in airport_types
        ]

    # Toggle All Airports
    airport_toggleAll = {
                "method": "restyle",
                "args" : [{"visible" : True}, [i for i, x in enumerate(all_traces) if x.name in airport_types]],
                "args2" : [{'visible':'legendonly'},[i for i,x in enumerate(all_traces) if x.name in airport_types]],
                "label": "Toggle All",
                "visible" : True, 
            }
    airport_buttons.append(airport_toggleAll) 

    # Toggle All Flights 
    flights_toggleAll = {
                "method": "restyle",
                "args" : [{"visible" : True}, [i for i, x in enumerate(all_traces) if x.name == "Flights"]],
                "args2" : [{'visible':'legendonly'},[i for i,x in enumerate(all_traces) if x.name == "Flights"]],
                "label": "Flight Paths",
                "visible" : True, 

            }
    airport_buttons.append(flights_toggleAll)



    ## Final Conf 

    updateMenusConf = [
        {
            "buttons": hp_buttons,
            "direction" : "down",
            "showactive" : False,
            "x": 0.1,
            "y": 1.15,
            "xanchor" : "left",
            "yanchor" : "top", 
            "font": {"size" : 12},
            "type": "dropdown",
            "name": "Toggle Flags"
        },
        {
            "buttons": airport_buttons,
            "direction" : "down",
            "showactive" : True,
            "x": -.05,
            "y": 1.15,
            "xanchor" : "left",
            "yanchor" : "top", 
            "font": {"size" : 12},
            "type": "dropdown",
            "name": "Flight Toggle"
        }
        ]


    ## Create Plotly figure 
    fig = go.Figure(data = all_traces)


    fig.update_layout(
        title_text = 'Interactive Flight Map',
        showlegend = True,
        clickmode='event+select',
        hovermode = 'closest',
        geo = dict(
            scope = 'north america',
            projection_type = 'azimuthal equal area',
            showland = True,
            showcountries = True,
            showsubunits = True, 
            subunitcolor = "Black",
            landcolor = 'rgb(243, 243, 243)',
            countrycolor = 'rgb(204, 204, 204)',
        ),
        updatemenus = updateMenusConf
    )

    # Return figure
    return fig