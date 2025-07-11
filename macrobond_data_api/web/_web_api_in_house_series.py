from datetime import datetime, tzinfo
from typing import TYPE_CHECKING, Optional, Sequence, Union, Any, List, Dict

from macrobond_data_api.common.enums import SeriesWeekdays, SeriesFrequency

if TYPE_CHECKING:  # pragma: no cover
    from .web_api import WebApi


__pdoc__ = {
    "WebApi.__init__": False,
}


def _set_metadata(metadata: Dict[str, Any], name: str, val: Any) -> None:
    if name in metadata:
        if metadata[name] != val:
            raise ValueError(f"{name} in metadata does not match {name}")
    else:
        metadata[name] = val


def set_tzinfo_and_isoformat(date: datetime, local_time_zone: tzinfo) -> str:
    if date.tzinfo is None:
        date = date.replace(tzinfo=local_time_zone)
    return date.isoformat()


def upload_series(
    self: "WebApi",
    name: str,
    description: str,
    region: str,
    category: str,
    frequency: SeriesFrequency,
    values: Sequence[Optional[float]],
    start_date_or_dates: Union[datetime, Sequence[datetime]],
    day_mask: SeriesWeekdays = SeriesWeekdays.MONDAY_TO_FRIDAY,
    metadata: Optional[Dict[str, Any]] = None,
    forecast_flags: Optional[Sequence[bool]] = None,
) -> None:
    if not isinstance(values, list):
        values = list(values)

    if forecast_flags is not None and not isinstance(forecast_flags, list):
        forecast_flags = list(forecast_flags)

    if metadata is None:
        metadata = {}
    else:
        metadata = {k: v.isoformat() if isinstance(v, datetime) else v for k, v in metadata.items()}

    _set_metadata(metadata, "PrimName", name)
    _set_metadata(metadata, "Description", description)
    _set_metadata(metadata, "Region", region)
    _set_metadata(metadata, "IHCategory", category)
    _set_metadata(metadata, "Frequency", frequency.name.lower())
    _set_metadata(metadata, "DayMask", day_mask.value)

    dates: Optional[List[str]] = None

    if isinstance(start_date_or_dates, datetime):
        if start_date_or_dates.tzinfo is None:
            raise ValueError("start_date_or_dates must have a timezone")
        _set_metadata(metadata, "StartDate", start_date_or_dates.isoformat())
    else:
        local_time_zone = datetime.now().astimezone().tzinfo
        if local_time_zone is None:
            raise ValueError("cat not determine local timezone")
        dates = [set_tzinfo_and_isoformat(x, local_time_zone) for x in start_date_or_dates]

    self.session.in_house_series.upload_series(
        {"forecastFlags": forecast_flags, "metadata": metadata, "values": values, "dates": dates}
    )


def delete_serie(self: "WebApi", series_name: str) -> None:
    self.session.in_house_series.delete_series(series_name)
