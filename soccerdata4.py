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

# Team ID
teamID=149

# Match ID
matchID = 7638434


# Player ID
playerID = 184012

# Referee ID
refereeID = 294

# Today
today = datetime.datetime.now().date()


#Get League Table
def get_league_table(leagueID):
    url = "https://api.football-data-api.com/league-tables"
    paramsLeague = {
        "key": "2d175fcc2f3c25f0a2a6f27e9ff2c662ca850cdc2fdac707296be94f83ddd837",
        "season_id": str(leagueID),
    }
    try:
        response = requests.get(url, params=paramsLeague)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error retrieving data: {e}")
        return None
    

# Retrieve league table stats
leagueTable_data = get_league_table(leagueID=9660)

# Extract and convert 'data' to DataFrame
if leagueTable_data and 'data' in leagueTable_data:

    try:
        # Use json_normalize for flexible parsing
        data = leagueTable_data['data']
        
        # Attempt different parsing strategies
        if isinstance(data, dict):
            # If data is a single dict, convert to list
            df = pd.json_normalize([data])
        elif isinstance(data, list):
            df = pd.json_normalize(data)
        else:
            raise ValueError("Unexpected data type")
        
        # Save to Excel
        df.to_excel('league_table.xlsx', index=False)
        
        print("Data saved to league_table.xlsx")
        print(df.head())
        print(f"DataFrame shape: {df.shape}")
    
    except Exception as e:
        print(f"Error parsing data: {e}")
        # Save raw data for inspection
        with open('raw_leagueTable_data.json', 'w') as f:
            json.dump(leagueTable_data, f, indent=2)
        print("Raw data saved to raw_leagueTable_data.json for inspection")



#Get Player Stats
def get_player_stats(playerID):
    url = "https://api.football-data-api.com/player-stats"
    paramsLeague = {
        "key": "2d175fcc2f3c25f0a2a6f27e9ff2c662ca850cdc2fdac707296be94f83ddd837",
        "player_id": str(playerID),
    }
    try:
        response = requests.get(url, params=paramsLeague)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error retrieving data: {e}")
        return None
    

# Retrieve Player stats
player_data = get_player_stats(playerID)

# Extract and convert 'data' to DataFrame
if player_data and 'data' in player_data:

    try:
        # Use json_normalize for flexible parsing
        data = player_data['data']
        
        # Attempt different parsing strategies
        if isinstance(data, dict):
            # If data is a single dict, convert to list
            df = pd.json_normalize([data])
        elif isinstance(data, list):
            df = pd.json_normalize(data)
        else:
            raise ValueError("Unexpected data type")
        
        # Save to Excel
        df.to_excel('player_stats.xlsx', index=False)
        
        print("Data saved to player_stats.xlsx")
        print(df.head())
        print(f"DataFrame shape: {df.shape}")
    
    except Exception as e:
        print(f"Error parsing data: {e}")
        # Save raw data for inspection
        with open('raw_playerStats_data.json', 'w') as f:
            json.dump(player_data, f, indent=2)
        print("Raw data saved to raw_playerStats_data.json for inspection")



#Get Referee Stats
def get_referee_stats(refereeID):
    url = "https://api.football-data-api.com/referee"
    paramsLeague = {
        "key": "2d175fcc2f3c25f0a2a6f27e9ff2c662ca850cdc2fdac707296be94f83ddd837",
        "referee_id": str(refereeID),
    }
    try:
        response = requests.get(url, params=paramsLeague)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error retrieving data: {e}")
        return None
    

# Retrieve referee stats
referee_data = get_referee_stats(refereeID)

# Extract and convert 'data' to DataFrame
if referee_data and 'data' in referee_data:

    try:
        # Use json_normalize for flexible parsing
        data = referee_data['data']
        
        # Attempt different parsing strategies
        if isinstance(data, dict):
            # If data is a single dict, convert to list
            df = pd.json_normalize([data])
        elif isinstance(data, list):
            df = pd.json_normalize(data)
        else:
            raise ValueError("Unexpected data type")
        
        # Save to Excel
        df.to_excel('referee_stats.xlsx', index=False)
        
        print("Data saved to referee_stats.xlsx")
        print(df.head())
        print(f"DataFrame shape: {df.shape}")
    
    except Exception as e:
        print(f"Error parsing data: {e}")
        # Save raw data for inspection
        with open('raw_refereeStats_data.json', 'w') as f:
            json.dump(referee_data, f, indent=2)
        print("Raw data saved to raw_refereeStats_data.json for inspection")