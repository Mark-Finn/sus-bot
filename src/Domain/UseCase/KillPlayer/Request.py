class Request:

    def __init__(self, killer_id: int, victim_id: int) -> None:
        self.killer_id: int = killer_id
        self.victim_id: int = victim_id
