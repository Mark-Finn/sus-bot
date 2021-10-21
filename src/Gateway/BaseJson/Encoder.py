import json


class Encoder(json.JSONEncoder):

    def default(self, obj):
        if not isinstance(obj, list):
            return self._encode_object(obj)
        return self._list_to_dict(list(map(self._encode_object, obj)))

    def _encode_object(self, obj):
        return obj.__dict__ if hasattr(obj, '__dict__') else str(obj)

    def _list_to_dict(self, list):
        return dict(zip(self._get_keys(list), list))

    def _get_keys(self, lst):
        return range(0, len(lst))