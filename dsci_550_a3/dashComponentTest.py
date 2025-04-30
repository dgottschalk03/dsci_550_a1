from dash import Dash, dcc, html, Input, Output, callback

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

# Use the following function when accessing the value of 'my-range-slider'
# in callbacks to transform the output value to logarithmic



airports = [
    {"label": "Heliport", "value": "heliport"},
    {"label": "Seaplane Base", "value": "seaplane_base"}, 
    {"label": "Balloonport", "value": "balloonport"},
    {"label": "Small Airport", "value": "small_airport"}, 
    {"label": "Medium Airport", "value": "medium_airport"},
    {"label": "Large Airport", "value": "large_airport"},
]

app.layout = html.Div([
    # title
    html.Div([
    html.H4("Year Slider", style = {'textAlign' : 'center', 'marginBottom': '10px'}),
    
    # year slider
    html.Label("Airport Type:"),
    dcc.Checklist(
        id='airport-checklist',
        options=airports,
        value = [],
        inputStyle={"margin-right": "5px", "margin-left": "10px"},
        style={'display': 'flex', 'flexDirection': 'row'}
    )
    ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    html.Div(id='output-container-range-slider-non-linear', style={'marginTop': 20})
])

@callback(
    Output('output-container-range-slider-non-linear', 'children'),
    Input('airport-checklist', 'value'))
def update_output(value):

    return 'Value: {}]'.format(
        str(value),

    )

if __name__ == '__main__':
    app.run(debug=True)
