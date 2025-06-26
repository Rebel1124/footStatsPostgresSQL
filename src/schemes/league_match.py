from .match import Match


class LeagueMatch(Match):
    over05: bool
    over15: bool
    over25: bool
    over35: bool
    over45: bool
    over55: bool
    btts: bool
