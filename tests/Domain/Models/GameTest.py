import unittest

from Domain.Models.Game import Game
from Dtos.Settings import Settings
from Dtos.Task import Task
from Enums.GameState import GameState


class GameTest(unittest.TestCase):

    def testStart_whenGameStarts_returnsGameInProgress(self):
        # arrange
        game_model = Game(settings=Settings(), all_tasks=self.__get_fake_tasks())

        # act
        game_model.start()

        # assert
        expected_game_state = GameState.IN_PROGRESS
        self.assertEqual(expected_game_state, game_model.game_state)

    def __get_fake_tasks(self):
        return [
            Task('admin swipe', 'admin', 'swipe card', 'common'),
            Task('wires', 'everywhere', 'connect wires', 'common'),
            Task('scan', 'medbay', 'scans body', 'short'),
            Task('chart course', 'navigation', 'char course', 'short'),
            Task('clean vent', 'anywhere', 'clean vent', 'short'),
            Task('asteroids', 'weapons', 'destroy asteroids', 'long'),
            Task('simon says', 'nuclear', 'play simon says', 'long'),
        ]


if __name__ == '__main__':
    unittest.main()
