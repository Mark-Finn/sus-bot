from Dtos.Task import Task
from Gateway.BaseJson.Decoder import Decoder as BaseDecoder


class Decoder(BaseDecoder):

    def _get_class(self):
        return Task