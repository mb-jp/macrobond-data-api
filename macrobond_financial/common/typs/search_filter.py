# -*- coding: utf-8 -*-

from typing import Dict, Sequence, Union, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from pandas import DataFrame, _typing as pandas_typing  # type: ignore


class SearchFilter:
    def __init__(
        self,
        text: str = None,
        entity_types: Union[Sequence[str], str] = None,
        must_have_values: Dict[str, object] = None,
        must_not_have_values: Dict[str, object] = None,
        must_have_attributes: Union[Sequence[str], str] = None,
        must_not_have_attributes: Union[Sequence[str], str] = None,
    ) -> None:
        self.text = text

        if isinstance(entity_types, str):
            self.entity_types: Sequence[str] = [entity_types]
        else:
            self.entity_types = entity_types if entity_types else []

        self.must_have_values: Dict[str, object] = (
            must_have_values if must_have_values else {}
        )

        self.must_not_have_values: Dict[str, object] = (
            must_not_have_values if must_not_have_values else {}
        )

        if isinstance(must_have_attributes, str):
            self.must_have_attributes: Sequence[str] = [must_have_attributes]
        else:
            self.must_have_attributes = (
                must_have_attributes if must_have_attributes else []
            )

        if isinstance(must_not_have_attributes, str):
            self.must_not_have_attributes: Sequence[str] = [must_not_have_attributes]
        else:
            self.must_not_have_attributes = (
                must_not_have_attributes if must_not_have_attributes else []
            )
