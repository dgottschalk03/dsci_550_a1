from itertools import chain
from datetime import date

# Unique Legend Items
def get_legend_items(df_hp, legend_key):
    s = set().union(*df_hp[legend_key].dropna().str.split(' | ').tolist())
    try:
        s.remove('|')  # remove delimiter if it was caught
    except:
        pass
    return  list(s)

# Date Range Filter
def parse_date(s): 
    return date(*map(int, s.split('-'))) 

def in_date_range(date_list, start_date, end_date):
    return any(start_date <= date <= end_date for date in date_list)

# Main Query Function
def filter_hp_df(
    hp_df,
    route_df,
    airport_df,
    flight_intersections,
    airport_intersections,
    state=None, event_type=None, apparition_type=None, haunt_date_range=None, holiday = None):
    
    filtered_hp_df = hp_df.copy()
    
    if state:
        filtered_hp_df = filtered_hp_df[filtered_hp_df['State'] == state]
    if event_type:
        filtered_hp_df = filtered_hp_df[filtered_hp_df['Event_Type'].str.contains(event_type, na=False)]
    if apparition_type:
        filtered_hp_df = filtered_hp_df[filtered_hp_df['Apparition_Type'].str.contains(apparition_type, na=False)]
    if haunt_date_range:
        start_date, end_date = map(parse_date, haunt_date_range)
        filtered_hp_df = filtered_hp_df[(filtered_hp_df['Haunted_Places_Date'].apply(lambda x: in_date_range(x, start_date, end_date)))]
    if holiday:
        holiday = parse_date(holiday)
        filtered_hp_df = filtered_hp_df[filtered_hp_df['Haunted_Places_Date'].apply(lambda x: in_date_range(x, holiday, holiday))]

    haunted_ids = filtered_hp_df['Haunted_Places_Id'].astype(str).tolist()

    filtered_flight_intersections = {k: v['Routes'] for k, v in flight_intersections.items() if k in haunted_ids}
    filtered_airport_intersections = {k: v['Airports'] for k, v in airport_intersections.items() if k in haunted_ids}

    relevant_routes = set()
    relevant_iata_codes = set()
    relevant_airports = set()

    for _, v in filtered_flight_intersections.items():
        relevant_routes.update(route['Route_ID'] for route in v)
        relevant_iata_codes.update(
            chain(
            (route['Dest_Airport'] for route in v),
            (route['Source_Airport'] for route in v)
            )
        )
        
    for _, v in filtered_airport_intersections.items():
        relevant_airports.update(airport['Airport_ID'] for airport in v)

    filtered_route_df = route_df.loc[list(relevant_routes)]
    filtered_airport_df = airport_df[airport_df['Id'].isin(relevant_airports) | airport_df['Iata_Code'].isin(relevant_iata_codes)]

    return filtered_hp_df, filtered_route_df, filtered_airport_df