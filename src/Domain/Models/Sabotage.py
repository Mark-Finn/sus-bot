from datetime import datetime


class Sabotage:

    def __init__(self) -> None:
        self.is_resolved: bool = False
        self.start_time: datetime = datetime.now()
        self.end_time: datetime = datetime.min

    def resolve(self):
        self.is_resolved = True
        self.end_time = datetime.now()