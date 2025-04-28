import dash
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Test Image Render"),
    html.Img(src="https://i.imgur.com/wZ4GJ2R.png", style={'width': '300px', 'height': '200px'})
])

if __name__ == "__main__":
    app.run(debug=True)




# image_links = {
#     "Electronic_Malfunction" : "https://drive.google.com/file/d/1ScXiXQC56Uq7hfOHKP4x77TwB63BKV71/view?usp=drive_link",
#     "Accident/Disaster" : "https://drive.google.com/file/d/1i0S_Gzz_WXpccP5co0afB5shs0E-jGTA/view?usp=drive_link", 
#     "Flying_Object" : "https://drive.google.com/file/d/1j1xVbOmF7duVySzJ9oWna1zuGR82Guk-/view?usp=drive_link", 
#     'Plane_Crash' : "https://drive.google.com/file/d/1POFRr7GzQwWje8oIbQOWSzZAuIMn2l5N/view?usp=drive_link",
#     'Supernatural' : "https://drive.google.com/file/d/1iBwg05D0seFPJyTtz6sHoIZvnZXlgJ3F/view?usp=drive_link",
#     "Unknown" : "https://drive.google.com/file/d/1CjFDg_a0NVCvQCLHGeX9GkZOK_I6WXwB/view?usp=drive_link", 
#     "Violence" : "https://drive.google.com/file/d/1KtiXtzaFk50QSNdBywXVbLZyf1iWzFWx/view?usp=drive_link"
# }

# for event_type in image_links.keys():
#     image_links[event_type] = build_hover_icon(convert_drive_links(image_links[event_type]))

# filtered_hp_df['Event_Type'] = filtered_hp_df['Event_Type'].apply(lambda x: x.split('|')[0].strip())
# filtered_hp_df['Image_Pointer'] = filtered_hp_df['Event_Type'].map(image_links)

# encoded_image = filtered_hp_df.loc[9]['Image_Pointer']
# encoded_image
# # display_binary_img(encoded_image)