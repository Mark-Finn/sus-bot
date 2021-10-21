from typing import Optional, List


class FinalResponse:

    def __init__(self) -> None:
        self.anonymous_voting: bool = False
        self.recipient_votes_map: dict = {}
        self.recipient_vote_count_list: List[tuple] = []
        self.ejected_player: Optional[str] = None
        self.no_ejection_reason: str = ''
        self.was_impostor: Optional[bool] = None
        self.remaining_impostors: Optional[int] = None
        self.is_game_over: bool = False
        self.is_com_sabotage: bool = False
        self.rotation_options: List[int] = []
        self.is_electrical_sabotage: bool = False
        self.switch_states: List[bool] = []