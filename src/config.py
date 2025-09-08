import os
from enum import StrEnum, auto

from dotenv import load_dotenv

load_dotenv()

FOOTYSTATS_API_KEY = os.environ["FOOTYSTATS_API_KEY"]
DB_URL = os.environ["DB_URL"]


class League(StrEnum):
    GERMANY_BUNDESLIGA = auto()
    EUROPE_UEFA_CHAMPIONS_LEAGUE = auto()
    ENGLAND_PREMIER_LEAGUE = auto()
    ENGLAND_CHAMPIONSHIP = auto()
    SPAIN_LA_LIGA = auto()
    FRANCE_LIGUE_1 = auto()
    ITALY_SERIE_A = auto()
    SOUTH_AFRICA_PREMIER_SOCCER_LEAGUE = auto()
    EUROPE_UEFA_EUROPA_LEAGUE = auto()
    SOUTH_AFRICA_NATIONAL_FIRST_DIVISION = auto()


FOOTY_STATS_LEAGUE_NAMES: dict[League, str] = {
    League.GERMANY_BUNDESLIGA: "Germany Bundesliga",
    League.EUROPE_UEFA_CHAMPIONS_LEAGUE: "Europe UEFA Champions League",
    League.ENGLAND_PREMIER_LEAGUE: "England Premier League",
    League.ENGLAND_CHAMPIONSHIP: "England Championship",
    League.SPAIN_LA_LIGA: "Spain La Liga",
    League.FRANCE_LIGUE_1: "France Ligue 1",
    League.ITALY_SERIE_A: "Italy Serie A",
    League.SOUTH_AFRICA_PREMIER_SOCCER_LEAGUE: "South Africa Premier Soccer League",
    League.EUROPE_UEFA_EUROPA_LEAGUE: "Europe UEFA Europa League",
    League.SOUTH_AFRICA_NATIONAL_FIRST_DIVISION: "South Africa National First Division",
}

LEAGUES_NAMES = FOOTY_STATS_LEAGUE_NAMES.values()


BET_10_LEAGUE_IDS: dict[League, str] = {
    League.GERMANY_BUNDESLIGA: "b42dc668-1af7-3821-b6e8-80ca062a9e72",
    League.EUROPE_UEFA_CHAMPIONS_LEAGUE: "ce550e8e-33c9-3304-bfe4-68b219880435",
    League.ENGLAND_PREMIER_LEAGUE: "7e9ec672-139c-3622-975b-b94cac2aac00",
    League.ENGLAND_CHAMPIONSHIP: "56e39c5b-7291-328f-98a7-f63673ab708c",
    League.SPAIN_LA_LIGA: "f009a65c-c455-316d-8229-f637a9fe6daf",
    League.FRANCE_LIGUE_1: "464e8c09-cf26-3505-9cac-908bee0fc873",
    League.ITALY_SERIE_A: "6cc3c199-bbbf-3cd4-932d-3477ba302b69",
    League.SOUTH_AFRICA_PREMIER_SOCCER_LEAGUE: "46a22184-d2b4-3663-b2d0-e3938c1ed9e5",
    League.EUROPE_UEFA_EUROPA_LEAGUE: "80007881-9a0e-3809-b287-7d7216f01a7f",
    League.SOUTH_AFRICA_NATIONAL_FIRST_DIVISION: "1f5da8be-413c-3f54-9ac4-e32d209ea411",
}

HOOLYWOOD_BET_URLS: dict[League, str] = {
    League.GERMANY_BUNDESLIGA: "https://www.hollywoodbets.net/betting/1/soccer/all/65/germany/3092441/bundesliga?filter=match-betting",
    League.EUROPE_UEFA_CHAMPIONS_LEAGUE: "https://www.hollywoodbets.net/betting/1/soccer/all/617/uefa-champions-league/3617652/uefa-champions-league?filter=match-betting",
    League.ENGLAND_PREMIER_LEAGUE: "https://www.hollywoodbets.net/betting/1/soccer/all/248/england/3092452/premier-league?filter=match-betting",
    League.ENGLAND_CHAMPIONSHIP: "https://www.hollywoodbets.net/betting/1/soccer/all/248/england/3092456/championship?filter=match-betting",
    League.SPAIN_LA_LIGA: "https://www.hollywoodbets.net/betting/1/soccer/all/161/spain/3092463/spain-primera-division?filter=match-betting",
    League.FRANCE_LIGUE_1: "https://www.hollywoodbets.net/betting/1/soccer/all/61/france/3092422/ligue-1?filter=match-betting",
    League.ITALY_SERIE_A: "https://www.hollywoodbets.net/betting/1/soccer/all/83/italy/3092562/serie-a?filter=match-betting",
    League.SOUTH_AFRICA_PREMIER_SOCCER_LEAGUE: "https://www.hollywoodbets.net/betting/1/soccer/all/2/south-africa/3092583/sa-psl?filter=match-betting",
    League.EUROPE_UEFA_EUROPA_LEAGUE: "https://www.hollywoodbets.net/betting/1/soccer/all/618/uefa-europa-league/3619705/uefa-europa-league?filter=match-betting",
    League.SOUTH_AFRICA_NATIONAL_FIRST_DIVISION: "https://www.hollywoodbets.net/betting/1/soccer/all/2/south-africa/3092935/sa-mfc?filter=match-betting",
}

BET_WAY_URLS: dict[League, str] = {
    League.GERMANY_BUNDESLIGA: "https://new.betway.co.za/sport/soccer?sortOrder=League&selectedLeagues=germany_bundesliga",
    League.EUROPE_UEFA_CHAMPIONS_LEAGUE: "https://new.betway.co.za/sport/soccer?sortOrder=League&selectedLeagues=international-clubs_uefa-champions-league",
    League.ENGLAND_PREMIER_LEAGUE: "https://new.betway.co.za/sport/soccer?sortOrder=League&selectedLeagues=england_premier-league",
    League.ENGLAND_CHAMPIONSHIP: "https://new.betway.co.za/sport/soccer?sortOrder=League&selectedLeagues=england_championship",
    League.SPAIN_LA_LIGA: "https://new.betway.co.za/sport/soccer?sortOrder=League&selectedLeagues=spain_la-liga",
    League.FRANCE_LIGUE_1: "https://new.betway.co.za/sport/soccer?sortOrder=League&selectedLeagues=france_ligue-1",
    League.ITALY_SERIE_A: "https://new.betway.co.za/sport/soccer?sortOrder=League&selectedLeagues=italy_serie-a",
    League.SOUTH_AFRICA_PREMIER_SOCCER_LEAGUE: "https://new.betway.co.za/sport/soccer?sortOrder=League&selectedLeagues=south-africa_premiership",
    League.EUROPE_UEFA_EUROPA_LEAGUE: "https://new.betway.co.za/sport/soccer?sortOrder=League&selectedLeagues=international-clubs_uefa-europa-league",
    League.SOUTH_AFRICA_NATIONAL_FIRST_DIVISION: "https://new.betway.co.za/sport/soccer?sortOrder=League&selectedLeagues=south-africa_championship",
}

SUPER_SPORT_BET_URLS: dict[League, str] = {
    League.GERMANY_BUNDESLIGA: "https://supersportbet.com/sportsbook/soccer/german-bundesliga-209/",
    League.EUROPE_UEFA_CHAMPIONS_LEAGUE: "https://supersportbet.com/sportsbook/soccer/champions-league-286/",
    League.ENGLAND_PREMIER_LEAGUE: "https://supersportbet.com/sportsbook/soccer/premier-league-175/",
    League.ENGLAND_CHAMPIONSHIP: "https://supersportbet.com/sportsbook/soccer/england-championship-182/",
    League.SPAIN_LA_LIGA: "https://supersportbet.com/sportsbook/soccer/spain-la-liga-186/",
    League.FRANCE_LIGUE_1: "https://supersportbet.com/sportsbook/soccer/france-ligue-1-159/",
    League.ITALY_SERIE_A: "https://supersportbet.com/sportsbook/soccer/italy-serie-a-205/",
    League.SOUTH_AFRICA_PREMIER_SOCCER_LEAGUE: "https://supersportbet.com/sportsbook/soccer/south-africa-premiership-11147/",
    League.EUROPE_UEFA_EUROPA_LEAGUE: "https://supersportbet.com/sportsbook/soccer/uefa-europa-league-352/",
    League.SOUTH_AFRICA_NATIONAL_FIRST_DIVISION: None,
}
SPORTING_BET_URLS: dict[League, str] = {
    League.GERMANY_BUNDESLIGA: "https://www.sportingbet.co.za/en/sports/football-4/betting/germany-17/bundesliga-102842",
    League.EUROPE_UEFA_CHAMPIONS_LEAGUE: "https://www.sportingbet.co.za/en/sports/football-4/betting/europe-7/uefa-champions-league-102855",
    League.ENGLAND_PREMIER_LEAGUE: "https://www.sportingbet.co.za/en/sports/football-4/betting/england-14/premier-league-102841",
    League.ENGLAND_CHAMPIONSHIP: "https://www.sportingbet.co.za/en/sports/football-4/betting/england-14/championship-102839",
    League.SPAIN_LA_LIGA: "https://www.sportingbet.co.za/en/sports/football-4/betting/spain-28/laliga-102829",
    League.FRANCE_LIGUE_1: "https://www.sportingbet.co.za/en/sports/football-4/betting/france-16/ligue-1-102843",
    League.ITALY_SERIE_A: "https://www.sportingbet.co.za/en/sports/football-4/betting/italy-20/serie-a-102846",
    League.SOUTH_AFRICA_PREMIER_SOCCER_LEAGUE: "https://www.sportingbet.co.za/en/sports/football-4/betting/south-africa-197/premier-soccer-league-100015",
    League.EUROPE_UEFA_EUROPA_LEAGUE: "https://www.sportingbet.co.za/en/sports/football-4/betting/europe-7/uefa-europa-league-102856",
    League.SOUTH_AFRICA_NATIONAL_FIRST_DIVISION: "https://www.sportingbet.co.za/en/sports/football-4/betting/south-africa-197/championship-101414",
}

SUPA_BETS_LEAGUE_IDS: dict[League, int] = {
    League.GERMANY_BUNDESLIGA: 990865,
    League.EUROPE_UEFA_CHAMPIONS_LEAGUE: 990677,
    League.ENGLAND_PREMIER_LEAGUE: 990625,
    League.ENGLAND_CHAMPIONSHIP: 990674,
    League.SPAIN_LA_LIGA: 990618,
    League.FRANCE_LIGUE_1: 990645,
    League.ITALY_SERIE_A: 990826,
    League.SOUTH_AFRICA_PREMIER_SOCCER_LEAGUE: 1005011,
    League.EUROPE_UEFA_EUROPA_LEAGUE: 990760,
    League.SOUTH_AFRICA_NATIONAL_FIRST_DIVISION: 991050,
}
