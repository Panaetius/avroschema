"""Avro Schema classes."""

from functools import cached_property
from io import BytesIO
from typing import IO, Any, Dict, List, Optional, Tuple, Union

import fastavro
import fastavro.types

from avroschema.fields import _Field
from avroschema.utils import validate_name


def _parse_fields(target: Dict, source: Dict) -> List[Tuple[str, str]]:
    """Parse fields from class dicts."""
    errors = []
    for field_name, field_value in source.items():
        if not issubclass(type(field_value), _Field):
            continue
        validation_errors = field_value.validate()
        if validation_errors:
            errors.append((field_name, validation_errors))
        target[field_name] = field_value

    return errors


class AvroMeta(type):
    """Metaclass to create avro schemas."""

    __avro_name__: str
    __avro_namespace__: str
    __avro_doc__: str
    __avro_fields__: Dict[str, _Field]

    def __new__(cls, clsname, bases, attrs):
        """Create new type."""
        if not bases:
            return type.__new__(cls, clsname, bases, attrs)

        if "Meta" not in attrs:
            raise TypeError(f"'class Meta' missing on schema '{clsname}'")
        meta = attrs.pop("Meta")

        if not hasattr(meta, "name"):
            raise TypeError(f"Schema '{clsname}' is missing 'name' property")

        if not validate_name(meta.name):
            raise AttributeError(
                f"Schema name '{meta.name}' on schema '{clsname}' is invalid. "
                "Names must follow the pattern '[A-Za-z_][A-Za-z0-9_]*'"
            )

        attrs["__avro_name__"] = meta.name
        attrs["__avro_namespace__"] = getattr(meta, "namespace", None)
        attrs["__avro_doc__"] = getattr(meta, "doc", None)
        attrs["__avro_fields__"] = dict()

        errors = []

        classes = list(bases)
        for base in classes[:0:-1]:
            errors.extend(_parse_fields(attrs["__avro_fields__"], base.__dict__))

        errors.extend(_parse_fields(attrs["__avro_fields__"], attrs))

        if errors:
            msg = f"Schema '{clsname}' contains invalid fields:\n"
            for name, messages in errors:
                msg += f"\t{name}:\n"
                for error in errors:
                    msg += f"\t\t{error}\n"
            raise AttributeError(msg)

        return type.__new__(cls, clsname, bases, attrs)


class AvroSchema(metaclass=AvroMeta):
    """Base class for Avro schemas."""

    @cached_property
    def schema(self) -> Dict[str, Any]:
        """Avro schema as dictionary."""
        result = {
            "name": self.__avro_name__,
            "doc": self.__avro_doc__,
            "type": "record",
            "fields": list(),
        }

        if self.__avro_namespace__:
            result["namespace"] = self.__avro_namespace__

        for field_name, field_value in self.__avro_fields__.items():
            result["fields"].append({"name": field_name, "type": field_value.schema})

        return result

    @cached_property
    def parsed_schema(self) -> fastavro.types.Schema:
        """Parsed fastavro schema."""
        return fastavro.parse_schema(self.schema)

    def read(self, record: BytesIO) -> List[fastavro.types.AvroMessage]:
        """Read bytes to records."""
        return list(fastavro.reader(fo=record, reader_schema=self.parsed_schema))

    def write(
        self,
        records: Union[List[Dict[str, Any]], Dict[str, Any]],
        stream: Optional[IO] = None,
    ) -> IO:
        """Write records to stream."""
        if not stream:
            stream = BytesIO()

        fastavro.writer(stream, self.parsed_schema, records)
        stream.seek(0)

        return stream
