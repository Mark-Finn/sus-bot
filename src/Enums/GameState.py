from enum import Enum


class GameState(Enum):
    IN_LOBBY = 'in lobby'
    IN_PROGRESS = 'in progress'
    MEETING_CALLED = 'meeting called'
    DISCUSSING = 'crewmates meeting'
    VOTING = 'crewmates voting'
    RESULTS = 'viewing results'
    GAME_END = 'game over'