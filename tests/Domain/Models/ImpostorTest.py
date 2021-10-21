import unittest
from datetime import datetime

from Domain.Models.Impostor import Impostor

from Domain.Models.Player import Player


class ImpostorTest(unittest.TestCase):

    def testKill_whenImpostorKillsPlayer_returnDeadPlayerKilledAtSomeTime(self):
        #arrange
        impostor = Impostor(1, 'mark', 'blue')
        victim = Player(2, 'finn', 'red')

        #act
        impostor.kill(victim)
        actual_victim_is_alive = victim.is_alive()
        actual_kill_time = impostor.get_last_kill_time()

        #assert
        self.assertFalse(actual_victim_is_alive)
        self.assertTrue(actual_kill_time > datetime.min)


if __name__ == '__main__':
    unittest.main()