import unittest

from Domain.Models.Player import Player


class PlayerTest(unittest.TestCase):

    def testIsAlive_whenPlayerDidNotDie_returnsAlive(self):
        #arrange
        player = Player(1, 'mark', 'blue')

        #act
        actual = player.is_alive()

        #assert
        self.assertTrue(actual)

    def testIsAlive_whenPlayerDidDie_returnsDeadWithCauseOfDeath(self):
        # arrange
        player = Player(1, 'mark', 'blue')

        # act
        player.die('unit test')
        actual = player.is_alive()

        # assert
        expected_cause_of_death = 'unit test'
        self.assertFalse(actual)
        self.assertEqual(expected_cause_of_death, player.cause_of_death)


if __name__ == '__main__':
    unittest.main()