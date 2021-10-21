from abc import ABC, abstractmethod

from Domain.Models.Game import Game


class BaseValidator(ABC):

    def __init__(self) -> None:
        self.error_message: str = ''

    @abstractmethod
    def validate(self, game: Game) -> bool:
        pass
