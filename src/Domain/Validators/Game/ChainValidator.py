from typing import List, Optional

from Domain.Models.Game import Game
from Domain.Validators.Game.BaseValidator import BaseValidator


class ChainValidator(BaseValidator):

    def __init__(self, validators: Optional[List[BaseValidator]]=None) -> None:
        super().__init__()
        self.validators: List[BaseValidator] = validators or []

    def validate(self, game: Game) -> bool:
        for validator in self.validators:
            if not validator.validate(game):
                self.error_message = validator.error_message
                return False
        return True

    def add_validator(self, validator: BaseValidator):
        self.validators.append(validator)