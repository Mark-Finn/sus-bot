import json
import os
from abc import ABC, abstractmethod
from Gateway.BaseJson.Encoder import Encoder


class BaseJsonGateway(ABC):

    def fetch(self):
        return self.__fetch(self._get_decoder())

    def save(self, data):
        return self.__save(data, self._get_encoder())

    @abstractmethod
    def _filename(self):
        pass

    @abstractmethod
    def _get_decoder(self):
        pass

    def _get_encoder(self):
        return Encoder

    def __get_file(self):
        return f'{os.getcwd()}\data\{self._filename()}.json'

    def __fetch(self, decoder=None):
        with open(self.__get_file(), 'r') as file:
            return json.load(file, cls=decoder)

    def __save(self, data, encoder=None):
        with open(self.__get_file(), 'w') as file:
            json.dump(data, file, cls=encoder, indent=4)