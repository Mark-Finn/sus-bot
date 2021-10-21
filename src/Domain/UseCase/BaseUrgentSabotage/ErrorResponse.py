class ErrorResponse:

    def __init__(self) -> None:
        self.success: bool = False
        self.error_message: str = ''
