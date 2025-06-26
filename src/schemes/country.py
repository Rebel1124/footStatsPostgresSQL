from .base import StrictBaseModel


class Country(StrictBaseModel):
    id: int
    iso: str
    country: str
    name_jp: str | None
    name_tr: str | None
    name_kr: str | None
    name_pt: str | None
    name_ru: str | None
    name_es: str | None
    name_nl: str | None
    name_se: str | None
    name_de: str | None
    iso_number: int | None
