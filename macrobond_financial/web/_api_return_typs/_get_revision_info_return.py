# -*- coding: utf-8 -*-

from typing import List, Sequence, TYPE_CHECKING

from macrobond_financial.common.typs import GetEntitiesError

from macrobond_financial.common._get_pandas import _get_pandas

from macrobond_financial.common.api_return_typs import (
    GetRevisionInfoReturn,
    RevisionInfo,
)

from ._str_to_datetime import _optional_str_to_datetime_z, _str_to_datetime_z

if TYPE_CHECKING:  # pragma: no cover
    from ..web_typs import SeriesWithRevisionsInfoResponse

    from ..session import Session
    from macrobond_financial.common.api_return_typs import (
        RevisionInfoDict,
    )
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore


class _GetRevisionInfoReturn(GetRevisionInfoReturn):
    def __init__(
        self,
        session: "Session",
        series_names: Sequence[str],
        raise_error: bool,
    ) -> None:
        super().__init__()
        self.__session = session
        self.__series_names = series_names
        self.__raise_error = raise_error

    def get_revision_info(self) -> List["SeriesWithRevisionsInfoResponse"]:
        response = self.__session.series.get_revision_info(*self.__series_names)

        GetEntitiesError.raise_if(
            self.__raise_error,
            map(lambda x, y: (x, y.get("errorText")), self.__series_names, response),
        )

        return response

    def object(self) -> List[RevisionInfo]:
        def to_obj(name: str, serie: "SeriesWithRevisionsInfoResponse"):
            error_text = serie.get("errorText")
            if error_text:
                return RevisionInfo(
                    name,
                    error_text,
                    False,
                    False,
                    None,
                    None,
                    tuple(),
                )

            time_stamp_of_first_revision = _optional_str_to_datetime_z(
                serie.get("timeStampOfFirstRevision")
            )

            time_stamp_of_last_revision = _optional_str_to_datetime_z(
                serie.get("timeStampOfLastRevision")
            )

            vintage_time_stamps = tuple(
                map(
                    _str_to_datetime_z,
                    serie["vintageTimeStamps"],
                )
            )

            return RevisionInfo(
                name,
                "",
                serie["storesRevisions"],
                serie["hasRevisions"],
                time_stamp_of_first_revision,
                time_stamp_of_last_revision,
                vintage_time_stamps,
            )

        return list(map(to_obj, self.__series_names, self.get_revision_info()))

    def dict(self) -> List["RevisionInfoDict"]:
        def to_dict(
            name: str, serie: "SeriesWithRevisionsInfoResponse"
        ) -> "RevisionInfoDict":
            error_text = serie.get("errorText")
            if error_text:
                return {
                    "name": name,
                    "error_message": error_text,
                }

            time_stamp_of_first_revision = _optional_str_to_datetime_z(
                serie.get("timeStampOfFirstRevision")
            )

            time_stamp_of_last_revision = _optional_str_to_datetime_z(
                serie.get("timeStampOfLastRevision")
            )

            vintage_time_stamps = tuple(
                map(
                    _str_to_datetime_z,
                    serie["vintageTimeStamps"],
                )
            )

            return {
                "name": name,
                "stores_revisions": serie["storesRevisions"],
                "has_revisions": serie["hasRevisions"],
                "time_stamp_of_first_revision": time_stamp_of_first_revision,
                "time_stamp_of_last_revision": time_stamp_of_last_revision,
                "vintage_time_stamps": vintage_time_stamps,
            }

        return list(map(to_dict, self.__series_names, self.get_revision_info()))

    def data_frame(self, *args, **kwargs) -> "DataFrame":
        pandas = _get_pandas()
        args = args[1:]
        kwargs["data"] = self.dict()
        return pandas.DataFrame(*args, **kwargs)
