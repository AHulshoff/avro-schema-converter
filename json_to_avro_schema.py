import json
from avro.schema import parse


class Converter():

    def __init__(self, name: str, json_str: str):
        schema = json.dumps(self._read_data(json.loads(json_str), name), indent=4)
        self.avro_schema = parse(schema)
        self.avro_schema_str = schema


    def _type_rename(self, type_name):
        match type_name:
            case "str": return "string"
            case _: return type_name


    def _read_data(self, data, name):
        schema: dict = { "type": "record", "name": name, "fields": [] }
        for k in data:
            if isinstance(data[k], dict):
                schema["fields"] = schema["fields"] + [{ "name": k, "type": self._read_data(data[k], f"{name}.{k}") }]
            elif isinstance(data[k], list) and isinstance(data[k][0], dict):
                schema["fields"] = schema["fields"] + [({ "name": k, "type": { "type": "array", "items": self._read_data(data[k][0], f"{name}.{k}") } })]
            else:
                schema["fields"] = schema["fields"] + [({ "name": k, "type": self._type_rename(type(data[k]).__name__) })]
        return schema
