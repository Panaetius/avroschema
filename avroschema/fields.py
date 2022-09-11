"""Avro fields."""

from abc import abstractmethod
from typing import TYPE_CHECKING, Any
from typing import List as ListType
from typing import Optional

from avroschema.utils import validate_name

if TYPE_CHECKING:
    from avroschema.schema import AvroSchema


class _Field:
    """Base class of all fields."""

    def __init__(self) -> None:
        pass

    @property
    @abstractmethod
    def schema(self):
        """The schema snippet for this field."""
        raise NotImplementedError

    def validate(self) -> ListType[str]:
        """Validate this field."""
        return []


class String(_Field):
    """A String field."""

    def __init__(self) -> None:
        super().__init__()

    @property
    def schema(self):
        """The schema snippet for this field."""
        return "string"


class Boolean(_Field):
    """A Boolean field."""

    def __init__(self) -> None:
        super().__init__()

    @property
    def schema(self):
        """The schema snippet for this field."""
        return "boolean"


class Integer(_Field):
    """An Integer field."""

    def __init__(self) -> None:
        super().__init__()

    @property
    def schema(self):
        """The schema snippet for this field."""
        return "int"


class Long(_Field):
    """A Long field."""

    def __init__(self) -> None:
        super().__init__()

    @property
    def schema(self):
        """The schema snippet for this field."""
        return "long"


class Float(_Field):
    """A Float field."""

    def __init__(self) -> None:
        super().__init__()

    @property
    def schema(self):
        """The schema snippet for this field."""
        return "float"


class Double(_Field):
    """A double field."""

    def __init__(self) -> None:
        super().__init__()

    @property
    def schema(self):
        """The schema snippet for this field."""
        return "double"


class Bytes(_Field):
    """A bytes field."""

    def __init__(self) -> None:
        super().__init__()

    @property
    def schema(self):
        """The schema snippet for this field."""
        return "bytes"


class Nested(_Field):
    """A field containing a nested Avro schema."""

    def __init__(self, schema: "AvroSchema") -> None:
        super().__init__()
        self.nested_schema = schema

    @property
    def schema(self):
        """The schema snippet for this field."""
        return self.nested_schema.schema


class Enum(_Field):
    """An Enum field."""

    def __init__(self, name: str, symbols: ListType[str]) -> None:
        super().__init__()
        self.name = name
        self.symbols = symbols

    def validate(self) -> ListType[str]:
        """Validate this field."""
        errors = []
        if not validate_name(self.name):
            errors.append(
                f"Name '{self.name}' is invalidate, must be '[A-Za-z_][A-Za-z0-9_]*'."
            )

        for symbol in self.symbols:
            if not validate_name(symbol):
                errors.append(
                    f"Symbol '{symbol}' is invalidate, must be '[A-Za-z_][A-Za-z0-9_]*'."
                )

        return errors

    @property
    def schema(self):
        """The schema snippet for this field."""
        return {"type": "enum", "name": self.name, "symbols": self.symbols}


class List(_Field):
    """A List (Array) field."""

    def __init__(self, item_type: _Field, default: Optional[Any] = None) -> None:
        super().__init__()
        self.item_type = item_type
        self.default = default

    @property
    def schema(self):
        """The schema snippet for this field."""
        return {
            "type": "array",
            "values": self.item_type.schema,
            "default": self.default,
        }


class Dict(_Field):
    """A Dict (Map) field."""

    def __init__(self, item_type: _Field, default: Optional[Any] = None) -> None:
        super().__init__()
        self.item_type = item_type
        self.default = default

    @property
    def schema(self):
        """The schema snippet for this field."""
        return {"type": "map", "values": self.item_type.schema, "default": self.default}


class Fixed(_Field):
    """A fixed length binary field."""

    def __init__(self, name: str, size: int) -> None:
        super().__init__()
        self.name = name
        self.size = size

    def validate(self) -> ListType[str]:
        """Validate this field."""
        errors = []

        if not validate_name(self.name):
            errors.append(
                f"Name '{self.name}' is invalidate, must be '[A-Za-z_][A-Za-z0-9_]*'."
            )

        if self.size < 1:
            errors.append(f"Size '{self.size}' is invalid, must be greater than 0.")

        return errors

    @property
    def schema(self):
        """The schema snippet for this field."""
        return {"type": "fixed", "size": self.size, "name": self.name}


class Null:
    """A null field, used for optional values."""

    def __init__(self) -> None:
        pass

    @property
    def schema(self):
        """The schema snippet for this field."""
        return "null"


class Union(_Field):
    """A combination of several fields."""

    def __init__(self, *types: _Field) -> None:
        super().__init__()

        self.types = types

    @property
    def schema(self):
        """The schema snippet for this field."""
        return [t.schema for t in self.types]
