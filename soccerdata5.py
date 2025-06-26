import json

import pandas as pd
import requests

# URL Params
params = {
    "key": "2d175fcc2f3c25f0a2a6f27e9ff2c662ca850cdc2fdac707296be94f83ddd837"
}


#Get btts Stats
def get_btts_stats():
    url = "https://api.football-data-api.com/stats-data-btts"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error retrieving data: {e}")
        return None
    

# Retrieve btts stats
btts_data = get_btts_stats()

# Extract and convert 'data' to DataFrame
if btts_data and 'data' in btts_data:

    try:
        # Use json_normalize for flexible parsing
        data = btts_data['data']
        
        # Attempt different parsing strategies
        if isinstance(data, dict):
            # If data is a single dict, convert to list
            df = pd.json_normalize([data])
        elif isinstance(data, list):
            df = pd.json_normalize(data)
        else:
            raise ValueError("Unexpected data type")
        
        # Save to Excel
        df.to_excel('btts_stats.xlsx', index=False)
        
        print("Data saved to btts_stats.xlsx")
        print(df.head())
        print(f"DataFrame shape: {df.shape}")
    
    except Exception as e:
        print(f"Error parsing data: {e}")
        # Save raw data for inspection
        with open('raw_bttsStats_data.json', 'w') as f:
            json.dump(btts_data, f, indent=2)
        print("Raw data saved to raw_bttsStats_data.json for inspection")



#Get over25 Stats
def get_over25_stats():
    url = "https://api.football-data-api.com/stats-data-over25"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error retrieving data: {e}")
        return None
    

# Retrieve over25 stats
over25_data = get_over25_stats()

# Extract and convert 'data' to DataFrame
if over25_data and 'data' in over25_data:

    try:
        # Use json_normalize for flexible parsing
        data = over25_data['data']
        
        # Attempt different parsing strategies
        if isinstance(data, dict):
            # If data is a single dict, convert to list
            df = pd.json_normalize([data])
        elif isinstance(data, list):
            df = pd.json_normalize(data)
        else:
            raise ValueError("Unexpected data type")
        
        # Save to Excel
        df.to_excel('over25_stats.xlsx', index=False)
        
        print("Data saved to over25_stats.xlsx")
        print(df.head())
        print(f"DataFrame shape: {df.shape}")
    
    except Exception as e:
        print(f"Error parsing data: {e}")
        # Save raw data for inspection
        with open('raw_over25Stats_data.json', 'w') as f:
            json.dump(over25_data, f, indent=2)
        print("Raw data saved to raw_over25Stats_data.json for inspection")