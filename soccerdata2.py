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
leagueID=59


# Today
today = datetime.datetime.now().date()


#Get League Matches
def get_league_matches(leagueID, games=500):
    url = "https://api.football-data-api.com/league-matches"
    paramsLeague = {
        "key": "2d175fcc2f3c25f0a2a6f27e9ff2c662ca850cdc2fdac707296be94f83ddd837",
        "season_id": str(leagueID),
        "max_per_page": str(games)
    }
    try:
        response = requests.get(url, params=paramsLeague)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error retrieving data: {e}")
        return None
    

# Retrieve league matches
leagueMatches_data = get_league_matches(leagueID=9814)

# Extract and convert 'data' to DataFrame
if leagueMatches_data and 'data' in leagueMatches_data:

    try:
        # Use json_normalize for flexible parsing
        data = leagueMatches_data['data']
        
        # Attempt different parsing strategies
        if isinstance(data, dict):
            # If data is a single dict, convert to list
            df = pd.json_normalize([data])
        elif isinstance(data, list):
            df = pd.json_normalize(data)
        else:
            raise ValueError("Unexpected data type")
        
        # Save to Excel
        df.to_excel('league_matches.xlsx', index=False)
        
        print("Data saved to league_matches.xlsx")
        print(df.head())
        print(f"DataFrame shape: {df.shape}")
    
    except Exception as e:
        print(f"Error parsing data: {e}")
        # Save raw data for inspection
        with open('raw_match_data.json', 'w') as f:
            json.dump(leagueMatches_data, f, indent=2)
        print("Raw data saved to raw_match_data.json for inspection")




#Get League Teams
def get_league_teams(leagueID):
    url = "https://api.football-data-api.com/league-teams"
    paramsLeague = {
        "key": "2d175fcc2f3c25f0a2a6f27e9ff2c662ca850cdc2fdac707296be94f83ddd837",
        "season_id": str(leagueID),
        'include': 'stats'
    }
    try:
        response = requests.get(url, params=paramsLeague)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error retrieving data: {e}")
        return None
    

# Retrieve league teams
leagueTeams_data = get_league_teams(leagueID=13284)

# Extract and convert 'data' to DataFrame
if leagueTeams_data and 'data' in leagueTeams_data:

    try:
        # Use json_normalize for flexible parsing
        data = leagueTeams_data['data']
        
        # Attempt different parsing strategies
        if isinstance(data, dict):
            # If data is a single dict, convert to list
            df = pd.json_normalize([data])
        elif isinstance(data, list):
            df = pd.json_normalize(data)
        else:
            raise ValueError("Unexpected data type")
        
        # Save to Excel
        df.to_excel('league_teams.xlsx', index=False)
        
        print("Data saved to league_teams.xlsx")
        print(df.head())
        print(f"DataFrame shape: {df.shape}")
    
    except Exception as e:
        print(f"Error parsing data: {e}")
        # Save raw data for inspection
        with open('raw_team_data.json', 'w') as f:
            json.dump(leagueTeams_data, f, indent=2)
        print("Raw data saved to raw_team_data.json for inspection")



#Get League Players
def get_league_players(leagueID, pageNum=1):
    url = "https://api.football-data-api.com/league-players"
    paramsLeague = {
        "key": "2d175fcc2f3c25f0a2a6f27e9ff2c662ca850cdc2fdac707296be94f83ddd837",
        "season_id": str(leagueID),
        "include":'stats',
        "page": str(pageNum)
    }
    try:
        response = requests.get(url, params=paramsLeague)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error retrieving data: {e}")
        return None
    

# Retrieve league players
leaguePlayers_data = get_league_players(leagueID=9660, pageNum=1)

# Extract and convert 'data' to DataFrame
if leaguePlayers_data and 'data' in leaguePlayers_data:

    try:
        # Use json_normalize for flexible parsing
        data = leaguePlayers_data['data']
        
        # Attempt different parsing strategies
        if isinstance(data, dict):
            # If data is a single dict, convert to list
            df = pd.json_normalize([data])
        elif isinstance(data, list):
            df = pd.json_normalize(data)
        else:
            raise ValueError("Unexpected data type")
        
        # Save to Excel
        df.to_excel('league_players4.xlsx', index=False)
        
        print("Data saved to league_players4.xlsx")
        print(df.head())
        print(f"DataFrame shape: {df.shape}")
    
    except Exception as e:
        print(f"Error parsing data: {e}")
        # Save raw data for inspection
        with open('raw_player_data.json', 'w') as f:
            json.dump(leaguePlayers_data, f, indent=2)
        print("Raw data saved to raw_player_data.json for inspection")



#Get League Referees
def get_league_referees(leagueID):
    url = "https://api.football-data-api.com/league-referees"
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
    

# Retrieve league referees
leagueReferees_data = get_league_referees(leagueID=5225)

# Extract and convert 'data' to DataFrame
if leagueReferees_data and 'data' in leagueReferees_data:

    try:
        # Use json_normalize for flexible parsing
        data = leagueReferees_data['data']
        
        # Attempt different parsing strategies
        if isinstance(data, dict):
            # If data is a single dict, convert to list
            df = pd.json_normalize([data])
        elif isinstance(data, list):
            df = pd.json_normalize(data)
        else:
            raise ValueError("Unexpected data type")
        
        # Save to Excel
        df.to_excel('league_referees.xlsx', index=False)
        
        print("Data saved to league_referees.xlsx")
        print(df.head())
        print(f"DataFrame shape: {df.shape}")
    
    except Exception as e:
        print(f"Error parsing data: {e}")
        # Save raw data for inspection
        with open('raw_referee_data.json', 'w') as f:
            json.dump(leagueReferees_data, f, indent=2)
        print("Raw data saved to raw_referee_data.json for inspection")