from .base import StrictBaseModel, StrSeasonYear


class _Season(StrictBaseModel):
    id: int
    year: StrSeasonYear


class League(StrictBaseModel):
    name: str
    country: str
    league_name: str
    image: str
    season: list[_Season]
