import json
import dataclasses
from typing import Dict, List, Any


class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)


def deserialize_dataclass(DataClass, json_string: str) -> Any:
    """ Convert the JSON object represented by the string into the dataclass specified. """
    json_obj = json.loads(json_string)
    dc_data = {field.name: field.type(json_obj[field.name])
                    for field in dataclasses.fields(DataClass)}
    return DataClass(**dc_data)


def deserialize_dataclass_from_dict(DataClass, obj: dict) -> Any:
    dc_data = {field.name: field.type(obj[field.name]) if obj.get(field.name) else ""
                    for field in dataclasses.fields(DataClass)}
    return DataClass(**dc_data)
