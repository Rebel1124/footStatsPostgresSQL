from typing import Annotated, Literal

from pydantic import BeforeValidator

from .base import StrictBaseModel


@BeforeValidator
def validate_percent(percent):
    if not isinstance(percent, str):
        return percent
    digits, symbol = percent[:-1], percent[-1]
    if symbol != "%":
        raise ValueError(f"'{percent}' must have '%'")
    float(digits)


@BeforeValidator
def validate_speed(speed):
    if not isinstance(speed, str):
        return speed
    digits, notation = speed.split()
    if notation != "m/s":
        raise ValueError(f"'{speed}' must have 'm/s' instead")
    return float(digits)


StrPercent = Annotated[str, validate_percent]
StrSpeed = Annotated[str, validate_speed]


class _Temperature(StrictBaseModel):
    temp: float | None = None
    unit: Literal["fahrenheit", "celcius", None] = None


class _Coordinates(StrictBaseModel):
    lat: float
    lon: float


class _Wind(StrictBaseModel):
    degree: int | None = None
    speed: Annotated[str | None, validate_speed] = None


class Weather(StrictBaseModel):
    coordinates: _Coordinates | None = None
    temperature: _Temperature | None = None
    humidity: Annotated[str | None, validate_percent]
    wind: _Wind
    type: str
    temperature_celcius: _Temperature
    clouds: Annotated[str | None, validate_percent]
    code: str | None  # Literal[
    #     "rain",
    #     "clear",
    #     "clouds",
    #     "fog",
    #     "mist",
    #     "snow",
    #     "drizzle",
    #     "thunderstorm",
    #     "haze",
    # ]
    pressure: int
