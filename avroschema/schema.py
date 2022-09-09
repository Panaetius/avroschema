from functools import cached_property


class AvroMeta(type):
    def __new__(cls, clsname, bases, attrs):
        if "Meta" not in attrs:
            raise TypeError(f"'class Meta' missing on schema '{clsname}'")
        meta = attrs.pop("Meta")

        if not hasattr(meta, "name"):
            raise TypeError(f"Schema '{clsname}' is missing 'name' property")

        attrs["__avro_name"] = meta.name
        attrs["__avro_namespace"] = getattr(meta, "namespace", None)
        attrs["__avro_doc"] = getattr(meta, "doc", None)
        return type.__new__(cls, clsname, bases, attrs)


class AvroSchema(object, metaclass=AvroMeta):
    @cached_property
    def schema(self):
        pass
