from abc import abstractmethod
from typing import TYPE_CHECKING, Any
from typing import List as ListType
from typing import Optional

if TYPE_CHECKING:
    from avroschema.schema import AvroSchema


class _Field:
    def __init__(self) -> None:
        pass

    @property
    @abstractmethod
    def schema(self):
        raise NotImplementedError


class String(_Field):
    def __init__(self) -> None:
        super().__init__()

    @property
    def schema(self):
        return "string"


class Boolean(_Field):
    def __init__(self) -> None:
        super().__init__()

    @property
    def schema(self):
        return "boolean"


class Integer(_Field):
    def __init__(self) -> None:
        super().__init__()

    @property
    def schema(self):
        return "int"


class Long(_Field):
    def __init__(self) -> None:
        super().__init__()

    @property
    def schema(self):
        return "long"


class Float(_Field):
    def __init__(self) -> None:
        super().__init__()

    @property
    def schema(self):
        return "float"


class Double(_Field):
    def __init__(self) -> None:
        super().__init__()

    @property
    def schema(self):
        return "double"


class Bytes(_Field):
    def __init__(self) -> None:
        super().__init__()

    @property
    def schema(self):
        return "bytes"


class Nested(_Field):
    def __init__(self, schema: "AvroSchema") -> None:
        super().__init__()
        self.nested_schema = schema

    @property
    def schema(self):
        return self.nested_schema.schema


class Enum(_Field):
    def __init__(self, name: str, symbols: ListType[str]) -> None:
        super().__init__()
        self.name = name
        self.symbols = symbols

    @property
    def schema(self):
        return {"type": "enum", "name": self.name, "symbols": self.symbols}


class List(_Field):
    def __init__(self, item_type: _Field, default: Optional[Any] = None) -> None:
        super().__init__()
        self.item_type = item_type
        self.default = default

    @property
    def schema(self):
        return {
            "type": "array",
            "values": self.item_type.schema,
            "default": self.default,
        }


class Dict(_Field):
    def __init__(self, item_type: _Field, default: Optional[Any] = None) -> None:
        super().__init__()
        self.item_type = item_type
        self.default = default

    @property
    def schema(self):
        return {"type": "map", "values": self.item_type.schema, "default": self.default}


class Fixed(_Field):
    def __init__(self, name: str, size: int) -> None:
        super().__init__()
        self.name = name
        self.size = size

    @property
    def schema(self):
        return {"type": "fixed", "size": self.size, "name": self.name}


class Null:
    def __init__(self) -> None:
        pass

    @property
    def schema(self):
        return "null"


class Union(_Field):
    def __init__(self, *types) -> None:
        super().__init__()

        self.types = types

    @property
    def schema(self):
        return [t.schema for t in self.types]
