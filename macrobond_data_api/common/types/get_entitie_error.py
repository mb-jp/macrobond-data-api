from typing import Dict, List, Optional, Tuple, Iterable, cast, Union

__pdoc__ = {
    "EntitieErrorInfo.__init__": False,
    "GetEntitiesError.__init__": False,
}


class EntitieErrorInfo:

    name: str
    error_message: str

    def __init__(self, name: str, error_message: str):
        self.name = name
        """name"""

        self.error_message = error_message
        """error_message"""

    def __repr__(self):
        return f"name: {self.name} error_message: {self.error_message}"


class GetEntitiesError(Exception):

    entities: List[EntitieErrorInfo]
    message: str

    def __init__(
        self,
        entities: Union[List[EntitieErrorInfo], str, Dict[str, str]],
        error_message: str = None,
    ):
        def get_entities() -> List[EntitieErrorInfo]:
            if isinstance(entities, list):
                return entities
            if isinstance(entities, dict):
                return list(map(EntitieErrorInfo, entities.keys(), entities.values()))
            return [EntitieErrorInfo(entities, cast(str, error_message))]

        self.entities = get_entities()
        """entities"""

        self.message = "failed to retrieve:\n" + (
            "\n".join(
                map(
                    lambda x: "\t" + x.name + " error_message: " + x.error_message,
                    self.entities,
                )
            )
        )
        """message"""

        super().__init__(self.message)

    @classmethod
    def raise_if(
        cls,
        raise_error: bool,
        entities_or_name: Union[Iterable[Tuple[str, Optional[str]]], str],
        error_message: str = None,
    ) -> None:
        if not raise_error:
            return

        if isinstance(entities_or_name, str):
            if error_message:
                name = entities_or_name
                raise GetEntitiesError(name, error_message)
        else:
            entities = entities_or_name
            entities_list = cast(
                List[Tuple[str, str]],
                list(filter(lambda x: x[1] is not None, entities)),
            )
            if entities_list:
                raise GetEntitiesError(
                    list(map(lambda x: EntitieErrorInfo(x[0], x[1]), entities_list))
                )