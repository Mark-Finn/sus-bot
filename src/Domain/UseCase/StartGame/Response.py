from typing import List, Tuple
from Domain.UseCase.StartGame.PlayerResponse import PlayerResponse


class Response:

    def __init__(self) -> None:
        self.success: bool = False
        self.error_message: str = ''
        self.impostor_names: List[str] = []
        self.players: List[PlayerResponse] = []
        self.crewmate_color_pairs: List[Tuple] = []
        self.impostor_color_pairs: List[Tuple] = []