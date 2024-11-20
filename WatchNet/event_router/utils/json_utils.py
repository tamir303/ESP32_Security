import json
from datetime import datetime


class __CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, set):
            return list(obj)
        else:
            return str(obj)


def serialize_json(data):
    return json.dumps(data, cls=__CustomJSONEncoder).encode('utf-8')


def deserialize_json(data):
    return json.loads(data.decode('utf-8'))
