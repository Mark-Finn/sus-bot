import inspect
import json
from abc import ABC, abstractmethod


class Decoder(json.JSONDecoder, ABC):
    def __init__(self, *args, **kwargs) -> None:
        json.JSONDecoder.__init__(self, object_hook=self._object_hook, *args, **kwargs)

    def _object_hook(self, obj):
        if not obj:
            return obj

        constructor_args = inspect.getargspec(self._get_class().__init__)[0]
        if isinstance(obj, dict) and set(obj.keys()) <= set(constructor_args):
            return self._get_class()(**obj)

        if isinstance(obj, list):
            return map(self.object_hook, obj)

        return obj

    @abstractmethod
    def _get_class(self):
        pass