from Dtos.Settings import Settings
from Gateway.BaseJson.Gateway import BaseJsonGateway
from Domain.Gateway.Settings.Decoder import Decoder


class Gateway(BaseJsonGateway):

    def save(self, data: Settings):
        super().save(data)

    def fetch(self) -> Settings:
        settings = super().fetch()
        if isinstance(settings, Settings):
            return settings
        return Settings()

    def _filename(self):
        return 'settings'

    def _get_decoder(self):
        return Decoder