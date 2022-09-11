"""Testing Avro fields."""


def test_simple_schema():
    """Test a simple schema."""
    import avroschema.fields as fields
    from avroschema.schema import AvroSchema

    class MySchema(AvroSchema):
        username = fields.String()

        age = fields.Integer()

        balance = fields.Long()

        affinity = fields.Float()

        power = fields.Double()

        enabled = fields.Boolean()

        encoded = fields.Bytes()

        class Meta:
            name = "my_record"
            doc = "Test schema"

    schema = MySchema().schema

    assert schema == {
        "doc": "Test schema",
        "fields": [
            {"name": "username", "type": "string"},
            {"name": "age", "type": "int"},
            {"name": "balance", "type": "long"},
            {"name": "affinity", "type": "float"},
            {"name": "power", "type": "double"},
            {"name": "enabled", "type": "boolean"},
            {"name": "encoded", "type": "bytes"},
        ],
        "name": "my_record",
        "type": "record",
    }


def test_nested():
    """Test a nested field."""
    import avroschema.fields as fields
    from avroschema.schema import AvroSchema

    class ChildSchema(AvroSchema):
        username = fields.String()

        class Meta:
            name = "child_record"
            doc = "Test child schema"

    class ParentSchema(AvroSchema):
        organisation = fields.String()

        owner = fields.Nested(ChildSchema())

        class Meta:
            name = "parent_record"
            doc = "Test parent schema"

    schema = ParentSchema().schema

    assert schema == {
        "doc": "Test parent schema",
        "fields": [
            {"name": "organisation", "type": "string"},
            {
                "name": "owner",
                "type": {
                    "doc": "Test child schema",
                    "fields": [{"name": "username", "type": "string"}],
                    "name": "child_record",
                    "type": "record",
                },
            },
        ],
        "name": "parent_record",
        "type": "record",
    }


def test_enum():
    """Test an enum field."""
    import avroschema.fields as fields
    from avroschema.schema import AvroSchema

    class MySchema(AvroSchema):
        types = fields.Enum("type_enum", ["Hot", "Cold", "Freezing"])

        class Meta:
            name = "my_record"
            doc = "Test schema"

    schema = MySchema().schema

    assert schema == {
        "doc": "Test schema",
        "fields": [
            {
                "name": "types",
                "type": {
                    "name": "type_enum",
                    "symbols": ["Hot", "Cold", "Freezing"],
                    "type": "enum",
                },
            }
        ],
        "name": "my_record",
        "type": "record",
    }


def test_list():
    """Test a list field."""
    import avroschema.fields as fields
    from avroschema.schema import AvroSchema

    class MySchema(AvroSchema):
        entries = fields.List(item_type=fields.String())

        class Meta:
            name = "my_record"
            doc = "Test schema"

    schema = MySchema().schema

    assert schema == {
        "doc": "Test schema",
        "fields": [
            {
                "name": "entries",
                "type": {"default": None, "type": "array", "values": "string"},
            }
        ],
        "name": "my_record",
        "type": "record",
    }


def test_dict():
    """Test a dict field."""
    import avroschema.fields as fields
    from avroschema.schema import AvroSchema

    class MySchema(AvroSchema):
        entries = fields.Dict(item_type=fields.String())

        class Meta:
            name = "my_record"
            doc = "Test schema"

    schema = MySchema().schema

    assert schema == {
        "doc": "Test schema",
        "fields": [
            {
                "name": "entries",
                "type": {"default": None, "type": "map", "values": "string"},
            }
        ],
        "name": "my_record",
        "type": "record",
    }


def test_fixed():
    """Test a fixed field."""
    import avroschema.fields as fields
    from avroschema.schema import AvroSchema

    class MySchema(AvroSchema):
        bindata = fields.Fixed(name="binary_data", size=16)

        class Meta:
            name = "my_record"
            doc = "Test schema"

    schema = MySchema().schema

    assert schema == {
        "doc": "Test schema",
        "fields": [
            {
                "name": "bindata",
                "type": {"name": "binary_data", "size": 16, "type": "fixed"},
            }
        ],
        "name": "my_record",
        "type": "record",
    }


def test_union_null():
    """Test union and null fields."""
    import avroschema.fields as fields
    from avroschema.schema import AvroSchema

    class MySchema(AvroSchema):
        test = fields.Union(fields.Null(), fields.String())

        class Meta:
            name = "my_record"
            doc = "Test schema"

    schema = MySchema().schema

    assert schema == {
        "doc": "Test schema",
        "fields": [{"name": "test", "type": ["null", "string"]}],
        "name": "my_record",
        "type": "record",
    }


def test_complex_union():
    """Test complex unionfields."""
    import avroschema.fields as fields
    from avroschema.schema import AvroSchema

    class ChildSchema(AvroSchema):
        username = fields.String()

        class Meta:
            name = "child_record"
            doc = "Test child schema"

    class MySchema(AvroSchema):
        test = fields.Union(
            fields.Null(), fields.String(), fields.Nested(ChildSchema())
        )

        class Meta:
            name = "my_record"
            doc = "Test schema"

    schema = MySchema().schema

    assert schema == {
        "doc": "Test schema",
        "fields": [
            {
                "name": "test",
                "type": [
                    "null",
                    "string",
                    {
                        "doc": "Test child schema",
                        "fields": [{"name": "username", "type": "string"}],
                        "name": "child_record",
                        "type": "record",
                    },
                ],
            }
        ],
        "name": "my_record",
        "type": "record",
    }
