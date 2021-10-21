import unittest

from Domain.Models.PlayerSet import PlayerSet

from Domain.Models.Player import Player
from Dtos.Task import Task


class PlayerSetTest(unittest.TestCase):

    def testAssignRoles_whenOneImpostor_returnsOneImpostor(self):
        # arrange
        player_set = PlayerSet()
        player_set.update(Player(1, 'mark', 'red'))
        player_set.update(Player(2, 'finn', 'blue'))

        # act
        player_set.assign_roles(impostors_count=1)
        actual_impostor_count = player_set.impostor_count()

        # assert
        expected_impostor_count = 1
        self.assertAlmostEqual(expected_impostor_count, actual_impostor_count)

    def testAssignTasks_whenOneCommonOneLongTwoShortTaskSetting_returnsAllPlayersWithFourTasks(self):
        # arrange
        player_set = PlayerSet()
        player_set.update(Player(1, 'mark', 'red'))
        player_set.update(Player(2, 'finn', 'blue'))

        # act
        player_set.assign_tasks(self.__get_fake_tasks(), common_count=1, long_count=1, short_count=2)

        # assert
        expected_number_tasks = 4
        for player in player_set.fetch_all():
            self.assertEqual(expected_number_tasks, len(player.task_checklist.get_uncompleted_tasks()))

    def testAssignTasks_whenOneCommonTask_returnsAllPlayersGetTheSameCommonTask(self):
        #arrange
        player_set = PlayerSet()
        player_set.update(Player(1, 'mark', 'red'))
        player_set.update(Player(2, 'finn', 'blue'))

        #act
        player_set.assign_tasks(self.__get_fake_tasks(), common_count=1, long_count=1, short_count=2)
        mark = player_set.fetch(1)
        actual_common_tasks = list({'admin swipe', 'wires'}.intersection(set(mark.task_checklist.get_uncompleted_tasks())))

        #assert
        expected_number_of_common_tasks = 1
        self.assertEqual(expected_number_of_common_tasks, len(actual_common_tasks))
        for player in player_set.fetch_all():
            self.assertTrue(actual_common_tasks[0] in player.task_checklist.get_uncompleted_tasks())

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
