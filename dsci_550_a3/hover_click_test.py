import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import numpy as np

# Dummy data
lat = [34, 36, 40]
lon = [-118, -119, -120]
hover_texts = ["Haunting A", "Haunting B", "Haunting C"]

# Using placeholder images for now
image_urls = [
    "https://via.placeholder.com/120x80.png?text=Ghost+1",
    "https://via.placeholder.com/120x80.png?text=Ghost+2",
    "https://via.placeholder.com/120x80.png?text=Ghost+3"
]

# Encode into <img> tags (small for hover)
hover_images = [f"<img src='{url}' width='120' height='80'>" for url in image_urls]

# Create figure
fig = go.Figure(go.Scattergeo(
    lat=lat,
    lon=lon,
    mode='markers',
    hoverinfo='skip',
    customdata=np.stack([hover_texts, hover_images, image_urls], axis=-1),
    hovertemplate="%{customdata[0]}<br><br>%{customdata[1]}<extra></extra>"
))

# Dash app
app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id='geo-plot', figure=fig),
    html.Div(id='clicked-image-container')
])

# Callback: handle click
@app.callback(
    Output('clicked-image-container', 'children'),
    Input('geo-plot', 'clickData')
)
def display_clicked_image(clickData):
    if clickData is None:
        return html.Div("Click a point to see the full image.")
    
    customdata = clickData['points'][0]['customdata']
    hover_text = customdata[0]
    full_image_url = customdata[2]  # Use the full image URL now
    
    return html.Div([
        html.H4(f"Details for {hover_text}"),
        html.Img(src=full_image_url, style={'width': '400px', 'height': '300px'})
    ], style={'textAlign': 'center'})

if __name__ == '__main__':
    app.run(debug=True)