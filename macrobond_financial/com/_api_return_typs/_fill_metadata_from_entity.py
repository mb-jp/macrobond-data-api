# -*- coding: utf-8 -*-

from typing import Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover

    from ..com_typs import Entity as ComEntity


def _fill_metadata_from_entity(com_entity: "ComEntity") -> Dict[str, Any]:
    ret = {}
    metadata = com_entity.Metadata

    for names_and_description in metadata.ListNames():
        name = names_and_description[0]
        values = metadata.GetValues(name)
        ret[name] = values[0] if len(values) == 1 else list(values)

    if "FullDescription" not in ret:
        ret["FullDescription"] = com_entity.Title

    return ret


def _copy_metadata_from_com_entity_cict(
    source: "ComEntity", destination: Dict[str, Any]
) -> Dict[str, Any]:

    metadata = source.Metadata

    for names_and_description in metadata.ListNames():
        name = names_and_description[0]
        values = metadata.GetValues(name)

        destination["MetaData." + name] = (
            values[0] if len(values) == 1 else list(values)
        )

    if "MetaData.FullDescription" not in destination:
        destination["MetaData.FullDescription"] = source.Title

    return destination