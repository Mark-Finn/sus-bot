class Response:

    def __init__(self):
        self.success: bool = False
        self.error_message: str = ''
        self.report_options: dict = {}