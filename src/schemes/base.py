import json
from typing import Annotated, Literal
from urllib.parse import urljoin

from pydantic import BaseModel, BeforeValidator, ConfigDict


class StrictBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


add_base_domain = BeforeValidator(
    lambda path: urljoin("https://footystats.org/", path),
)

add_cdn_img_domain = BeforeValidator(
    lambda path: urljoin("https://cdn.footystats.org/img/", path)
)

from_json = BeforeValidator(json.loads)


type StrContinentCode = Literal["eu", "af", "an", "as", "na", "oc", "sa"]


def _validate_event_time(event_time: str) -> str:
    event_time = event_time.replace("'", "").strip()
    if "+" in event_time:  # 45 + 2
        nums = event_time.split("+")
        if len(nums) != 2:
            raise ValueError(f"{event_time!r} is not valid event time notation")
        if not (nums[0].isdigit() and nums[1].isdigit()):
            raise ValueError(f"{event_time!r} is not valid event time notation")
    elif event_time == "-1":
        pass
    else:  # 45
        if not event_time.isdigit():
            raise ValueError(f"{event_time!r} is not valid event time notation")
    return event_time


@BeforeValidator
def validate_event_times(raw_times) -> list[str]:
    if isinstance(raw_times, list):
        events = raw_times.copy()
    else:
        events = [str(g) for g in json.loads(raw_times)]
    return [_validate_event_time(event) for event in events]


@BeforeValidator
def validate_event_time(event_time) -> str:
    return _validate_event_time(event_time)


empty_list_to_none = BeforeValidator(lambda a: None if a == [] else a)
empty_str_to_none = BeforeValidator(lambda a: None if a == "" else a)
minus_one_to_none = BeforeValidator(lambda a: None if a == -1 else a)


def validate_season_year(year) -> str | None:
    if year == -1:
        return None
    string_year = str(year).strip().replace("/", "")
    if string_year.isdigit():
        match len(string_year):
            case 2:
                return "20" + string_year
            case 4:
                return string_year
            case 8:
                return f"{string_year[:4]}/{string_year[4:]}"
    raise ValueError(f"Year must have 4 or 8 digits. ({year!r})")


type StrSeasonYear = Annotated[str | None, BeforeValidator(validate_season_year)]
