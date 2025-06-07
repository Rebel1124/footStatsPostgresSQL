import requests
import pandas as pd
import json
import datetime
from datetime import timedelta

# URL Params
params = {
    "key": "2d175fcc2f3c25f0a2a6f27e9ff2c662ca850cdc2fdac707296be94f83ddd837"
}

# 2023-2024 Season league stats
leagueID=9660


# Today
today = datetime.datetime.now().date()

#Get Leagues
def get_league_list():
    url = "https://api.football-data-api.com/league-list"
    paramsLeague = {
        "key": "2d175fcc2f3c25f0a2a6f27e9ff2c662ca850cdc2fdac707296be94f83ddd837",
        "chosen_leagues_only": "true"
    }
    try:
        response = requests.get(url, params=paramsLeague)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error retrieving data: {e}")
        return None
    

# Retrieve league data
league_data = get_league_list()

# Extract and convert 'data' to DataFrame
if league_data and 'data' in league_data:
    df = pd.DataFrame(league_data['data'])
    
    # Save to CSV
    df.to_excel('league_list.xlsx', index=False)
    
    print("Data saved to league_list.xlsx")
    print(df.head())

    
#Get Countries
def get_country_list():
    url = "https://api.football-data-api.com/country-list"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error retrieving data: {e}")
        return None
    
# Retrieve country data
country_data = get_country_list()

# Extract and convert 'data' to DataFrame
if country_data and 'data' in country_data:
    df = pd.DataFrame(country_data['data'])
    
    # Save to CSV
    df.to_excel('country_list.xlsx', index=False)
    
    print("Data saved to country_list.xlsx")
    print(df.head())
    

#Get todays matches
def get_upcoming_matches(days=0):

    date = today + timedelta(days)
    dateString = date.strftime('%Y-%m-%d')

    paramsDate = {
    "key": "2d175fcc2f3c25f0a2a6f27e9ff2c662ca850cdc2fdac707296be94f83ddd837",
    "date": dateString
    }

    url = "https://api.football-data-api.com/todays-matches"
    try:
        response = requests.get(url, params=paramsDate)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error retrieving data: {e}")
        return None

# Retrieve today's matches
todays_data = get_upcoming_matches(0)

# Extract and convert 'data' to DataFrame
if todays_data and 'data' in todays_data:
    df = pd.DataFrame(todays_data['data'])
    
    # Save to CSV
    df.to_excel('upcoming_matches.xlsx', index=False)
    
    print("Data saved to upcoming_matches.xlsx")
    print(df.head())


#Get Season Stats
def get_season_stats(leagueID):
    url = "https://api.football-data-api.com/league-season"
    paramsLeague = {
        "key": "2d175fcc2f3c25f0a2a6f27e9ff2c662ca850cdc2fdac707296be94f83ddd837",
        "season_id": str(leagueID)
    }
    try:
        response = requests.get(url, params=paramsLeague)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error retrieving data: {e}")
        return None
    

# Retrieve season stats
season_data = get_season_stats(leagueID=12325)

# Extract and convert 'data' to DataFrame
if season_data and 'data' in season_data:

    try:
        # Use json_normalize for flexible parsing
        data = season_data['data']
        
        # Attempt different parsing strategies
        if isinstance(data, dict):
            # If data is a single dict, convert to list
            df = pd.json_normalize([data])
        elif isinstance(data, list):
            df = pd.json_normalize(data)
        else:
            raise ValueError("Unexpected data type")
        
        # Save to Excel
        df.to_excel('season_data.xlsx', index=False)
        
        print("Data saved to season_data.xlsx")
        print(df.head())
        print(f"DataFrame shape: {df.shape}")
    
    except Exception as e:
        print(f"Error parsing data: {e}")
        # Save raw data for inspection
        with open('raw_season_data.json', 'w') as f:
            json.dump(season_data, f, indent=2)
        print("Raw data saved to raw_season_data.json for inspection")
    