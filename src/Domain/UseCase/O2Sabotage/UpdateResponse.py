from Domain.UseCase.BaseUrgentSabotage.UpdateResponse import UpdateResponse as UrgentUpdateResponse


class UpdateResponse(UrgentUpdateResponse):

    def __init__(self) -> None:
        super().__init__()
        self.code1: str = ''
        self.code2: str = ''
        self.completed_codes: int = 0
        self.required_codes: int = 0
