# -*- coding: utf-8 -*-

from typing import Union, overload, List, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:  # pragma: no cover

    from pandas import DataFrame, _typing as pandas_typing  # type: ignore

    from ..typs import (
        Series,
        SeriesColumns,
        SeriesTypedDict,
    )


class GetSeriesReturn(ABC):
    @abstractmethod
    def list_of_objects(self) -> List["Series"]:
        ...

    @abstractmethod
    def list_of_dicts(self) -> List["SeriesTypedDict"]:
        ...

    @overload
    def data_frame(self) -> "DataFrame":
        ...

    @overload
    def data_frame(
        self,
        index: "pandas_typing.Axes" = None,
        columns: Union["SeriesColumns", "pandas_typing.Axes"] = None,
        dtype: "pandas_typing.Dtype" = None,
        copy: bool = False,
    ) -> "DataFrame":
        ...

    @abstractmethod
    def data_frame(self, *args, **kwargs) -> "DataFrame":
        ...
