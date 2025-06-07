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
teamID=676883

# Match ID
matchID = 7638434

# Today
today = datetime.datetime.now().date()


#Get Team Data
def get_team(teamID):
    url = "https://api.football-data-api.com/team"
    paramsLeague = {
        "key": "2d175fcc2f3c25f0a2a6f27e9ff2c662ca850cdc2fdac707296be94f83ddd837",
        "team_id": str(teamID),
        'include': 'stats'
    }
    try:
        response = requests.get(url, params=paramsLeague)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error retrieving data: {e}")
        return None
    

# Retrieve team data
team_data = get_team(teamID)

# Extract and convert 'data' to DataFrame
if team_data and 'data' in team_data:

    try:
        # Use json_normalize for flexible parsing
        data = team_data['data']
        
        # Attempt different parsing strategies
        if isinstance(data, dict):
            # If data is a single dict, convert to list
            df = pd.json_normalize([data])
        elif isinstance(data, list):
            df = pd.json_normalize(data)
        else:
            raise ValueError("Unexpected data type")
        
        # Save to Excel
        df.to_excel('teamData.xlsx', index=False)
        
        print("Data saved to teamData.xlsx")
        print(df.head())
        print(f"DataFrame shape: {df.shape}")
    
    except Exception as e:
        print(f"Error parsing data: {e}")
        # Save raw data for inspection
        with open('raw_team_data.json', 'w') as f:
            json.dump(team_data, f, indent=2)
        print("Raw data saved to raw_team_data.json for inspection")



#Get Team LastX Data
def get_teamLastx(teamID):
    url = "https://api.football-data-api.com/lastx"
    paramsLeague = {
        "key": "2d175fcc2f3c25f0a2a6f27e9ff2c662ca850cdc2fdac707296be94f83ddd837",
        "team_id": str(teamID),
    }
    try:
        response = requests.get(url, params=paramsLeague)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error retrieving data: {e}")
        return None
    

# Retrieve team lastx
lastx_data = get_teamLastx(teamID)

# Extract and convert 'data' to DataFrame
if lastx_data and 'data' in lastx_data:

    try:
        # Use json_normalize for flexible parsing
        data = lastx_data['data']
        
        # Attempt different parsing strategies
        if isinstance(data, dict):
            # If data is a single dict, convert to list
            df = pd.json_normalize([data])
        elif isinstance(data, list):
            df = pd.json_normalize(data)
        else:
            raise ValueError("Unexpected data type")
        
        # Save to Excel
        df.to_excel('teamLastx.xlsx', index=False)
        
        print("Data saved to teamLastx.xlsx")
        print(df.head())
        print(f"DataFrame shape: {df.shape}")
    
    except Exception as e:
        print(f"Error parsing data: {e}")
        # Save raw data for inspection
        with open('raw_teamLastx_data.json', 'w') as f:
            json.dump(lastx_data, f, indent=2)
        print("Raw data saved to raw_teamLastx_data.json for inspection")



#Get Team Match Details
def get_matchDetails(matchID):
    url = "https://api.football-data-api.com/match"
    paramsLeague = {
        "key": "2d175fcc2f3c25f0a2a6f27e9ff2c662ca850cdc2fdac707296be94f83ddd837",
        "match_id": str(matchID),
    }
    try:
        response = requests.get(url, params=paramsLeague)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error retrieving data: {e}")
        return None
    

# Retrieve match details
match_details = get_matchDetails(matchID)

# Extract and convert 'data' to DataFrame
if match_details and 'data' in match_details:

    try:
        # Use json_normalize for flexible parsing
        data = match_details['data']
        
        # Attempt different parsing strategies
        if isinstance(data, dict):
            # If data is a single dict, convert to list
            df = pd.json_normalize([data])
        elif isinstance(data, list):
            df = pd.json_normalize(data)
        else:
            raise ValueError("Unexpected data type")
        
        # Save to Excel
        df.to_excel('matchDetails.xlsx', index=False)
        
        print("Data saved to matchDetails.xlsx")
        print(df.head())
        print(f"DataFrame shape: {df.shape}")
    
    except Exception as e:
        print(f"Error parsing data: {e}")
        # Save raw data for inspection
        with open('raw_matchDetails.json', 'w') as f:
            json.dump(match_details, f, indent=2)
        print("Raw data saved to raw_matchDetails.json for inspection")