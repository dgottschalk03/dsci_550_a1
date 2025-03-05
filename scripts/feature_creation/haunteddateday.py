import pandas as pd
import numpy as np
import requests
from datetime import datetime
import time
import argparse
import re

def get_daylight_duration_calculation(lat, lon, date):
    
    try:
        # Convert latitude to radians
        lat_rad = np.radians(lat)
        
        # Calculate day of year
        day_of_year = date.timetuple().tm_yday
        
        # Calculate solar declination angle (in radians)
        declination = 0.4093 * np.sin(2 * np.pi * (284 + day_of_year) / 365)
        
        # Calculate daylight hours using the sunrise equation
        cos_hour_angle = -np.tan(lat_rad) * np.tan(declination)
        
        # Ensure cos_hour_angle is in the valid range [-1, 1]
        cos_hour_angle = np.clip(cos_hour_angle, -1, 1)
        
        # Calculate the hour angle
        hour_angle = np.arccos(cos_hour_angle)
        
        # Convert hour angle to hours
        daylight_hours = 2 * (hour_angle * 12 / np.pi)
        
        return daylight_hours
    except Exception as e:
        print(f"Calculation error for {lat}, {lon}, {date}: {e}")
        return None

def get_daylight_duration_hybrid(lat, lon, date, api_delay=1.0):
    
    try:
        # Format date as YYYY-MM-DD
        formatted_date = date.strftime('%Y-%m-%d')
        
        # Make API request
        url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lon}&date={formatted_date}&formatted=0"
        response = requests.get(url)
        data = response.json()
        
        # Add delay to avoid rate limiting
        time.sleep(api_delay)
        
        if data['status'] == 'OK':
            # Parse sunrise and sunset times
            sunrise = datetime.fromisoformat(data['results']['sunrise'].replace('Z', '+00:00'))
            sunset = datetime.fromisoformat(data['results']['sunset'].replace('Z', '+00:00'))
            
            # Calculate duration in hours
            daylight_seconds = (sunset - sunrise).total_seconds()
            daylight_hours = daylight_seconds / 3600
            
            return (daylight_hours, "API")
        else:
            print(f"API returned non-OK status: {data}")
            print(f"Falling back to calculation for {lat}, {lon}, {date}")
            
            # Use calculation method as fallback
            daylight_hours = get_daylight_duration_calculation(lat, lon, date)
            return (daylight_hours, "Calculation (API Error)")
    except Exception as e:
        print(f"API error for {lat}, {lon}, {date}: {e}")
        print(f"Falling back to calculation for {lat}, {lon}, {date}")
        
        # Use calculation method as fallback
        daylight_hours = get_daylight_duration_calculation(lat, lon, date)
        return (daylight_hours, "Calculation (API Exception)")

def parse_date(date_val):
    
    try:
        # If it's already a datetime
        if isinstance(date_val, pd.Timestamp) or isinstance(date_val, datetime):
            return date_val
            
        # If it's a string representation of a list with datetime objects
        if isinstance(date_val, str):
            # Try to extract datetime components using regex
            pattern = r'datetime\.datetime\((\d+),\s*(\d+),\s*(\d+)'
            match = re.search(pattern, date_val)
            
            if match:
                year, month, day = map(int, match.groups())
                # Handle future dates - API might not accept dates too far in the future
                if year > 2024:
                    # Use 2023 equivalent date (same month/day) to avoid API issues
                    year = 2023
                return datetime(year, month, day)
            
            # Try parsing as a regular date string
            try:
                date = pd.to_datetime(date_val)
                # Handle future dates
                if date.year > 2024:
                    return datetime(2023, date.month, date.day)
                return date
            except:
                pass
                
        # If it's an empty value or parsing failed
        return None
        
    except Exception as e:
        print(f"Date parsing error: {e} for value: {date_val}")
        return None

def process_dataset(input_file, output_file, api_delay=1.0):
    
    print(f"Processing dataset: {input_file}")
    print(f"Using hybrid method: API with calculation fallback (delay: {api_delay}s)")
    
    # Read the dataset
    try:
        if input_file.endswith('.tab'):
            df = pd.read_csv(input_file, sep='\t', on_bad_lines='warn')
        else:
            df = pd.read_csv(input_file, on_bad_lines='warn')
        
        print(f"Successfully loaded dataset with {len(df)} rows")
        
    except Exception as e:
        print(f"Error reading dataset: {e}")
        return None
    
    # Create empty columns for results
    df['Daylight_Duration_Hours'] = np.nan
    df['Data_Source'] = ''
    
    # Track successful calculations
    successful_count = 0
    api_count = 0
    calculation_count = 0
    
    # Process each row
    for idx, row in df.iterrows():
        try:
            # Skip if missing latitude, longitude
            if pd.isna(row['latitude']) or pd.isna(row['longitude']):
                if idx % 100 == 0:
                    print(f"Skipping row {idx}: Missing latitude or longitude")
                continue
                
            # Parse date
            date = parse_date(row['Haunted_Places_Date'])
            
            # Skip if date parsing failed
            if date is None:
                if idx % 100 == 0:
                    print(f"Skipping row {idx}: Could not parse date")
                continue
                
            # Get latitude and longitude
            lat = float(row['latitude'])
            lon = float(row['longitude'])
            
            # Get daylight duration using hybrid approach
            daylight_result = get_daylight_duration_hybrid(lat, lon, date, api_delay)
            
            if daylight_result is not None:
                daylight_hours, source = daylight_result
                
                # Update statistics
                if "API" in source:
                    api_count += 1
                else:
                    calculation_count += 1
                    
                # Update the dataframe
                if daylight_hours is not None:
                    df.at[idx, 'Daylight_Duration_Hours'] = daylight_hours
                    df.at[idx, 'Data_Source'] = source
                    successful_count += 1
            
            # Print progress
            if idx % 100 == 0 or idx < 5 or idx == len(df) - 1:
                status = f"Processed {idx+1}/{len(df)} records. "
                if daylight_result is not None and daylight_result[0] is not None:
                    status += f"Date: {date}, Daylight: {daylight_result[0]:.2f} hours, Source: {daylight_result[1]}"
                else:
                    status += f"Date: {date}, Failed to calculate daylight hours"
                print(status)
                
        except Exception as e:
            print(f"Error processing row {idx}: {e}")
            continue
        
        # Save intermediate results every 500 records
        if idx % 500 == 0 and idx > 0:
            print(f"Saving intermediate results at record {idx}...")
            df.to_csv(f"{output_file}.partial", index=False)
    
    # Save the final results
    df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")
    print(f"Successfully calculated daylight duration for {successful_count} out of {len(df)} records")
    print(f"  - API method: {api_count} records")
    print(f"  - Calculation method: {calculation_count} records")
    
    if successful_count > 0:
        print(f"Average daylight duration: {df['Daylight_Duration_Hours'].mean():.2f} hours")
        print(f"Min daylight duration: {df['Daylight_Duration_Hours'].min():.2f} hours")
        print(f"Max daylight duration: {df['Daylight_Duration_Hours'].max():.2f} hours")
    
    return df

if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description='Calculate daylight duration for haunted places dataset using hybrid approach')
    parser.add_argument('--input', '-i', type=str, required=True, help='Input file path')
    parser.add_argument('--output', '-o', type=str, default='haunted_places_with_daylight_hybrid.csv', 
                        help='Output file path')
    parser.add_argument('--delay', '-d', type=float, default=1.0, 
                        help='Delay between API calls in seconds (default: 1.0)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Process the dataset using hybrid approach
    results = process_dataset(args.input, args.output, api_delay=args.delay)