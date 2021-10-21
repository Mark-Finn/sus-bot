import unittest

from Domain.Models.Vote import Vote
from Domain.Models.Player import Player

from Domain.Models.Meeting import Meeting


class MeetingTest(unittest.TestCase):

    def testGetEjectedPlayer_whenNoVotes_returnSkip(self):
        #arrange
        meeting = Meeting(Player(1, 'mark', 'red'))

        #act
        actual = meeting.get_ejected_player_id()

        #assert
        self.assertFalse(actual)
        self.assertEqual(meeting.no_ejection_reason.lower(), 'no votes')

    def testGetEjectedPlayer_whenVotesTied_returnSkip(self):
        #arrange
        mark = Player(1, 'mark', 'blue')
        finn = Player(2, 'finn', 'red')
        bob = Player(3, 'bob', 'white')
        meeting = Meeting(mark)

        #act
        meeting.add_vote(Vote(mark, bob))
        meeting.add_vote(Vote(finn, mark))
        actual = meeting.get_ejected_player_id()

        #assert
        self.assertFalse(actual)
        self.assertEqual(meeting.no_ejection_reason.lower(), 'tie')


    def testGetEjectedPlayer_whenVoteToSkipWins_returnSkip(self):
        # arrange
        mark = Player(1, 'mark', 'blue')
        finn = Player(2, 'finn', 'red')
        bob = Player(3, 'bob', 'white')
        meeting = Meeting(mark)

        # act
        mark = Player(1, 'mark', 'blue')
        finn = Player(2, 'finn', 'red')
        bob = Player(3, 'bob', 'white')
        meeting.add_vote(Vote(mark, bob))
        meeting.add_vote(Vote(finn))
        meeting.add_vote(Vote(bob))
        actual = meeting.get_ejected_player_id()

        # assert
        self.assertFalse(actual)
        self.assertEqual(meeting.no_ejection_reason.lower(), 'skipped')

    def testGetEjectedPlayer_whenBobGetsTheMostVotes_returnBobsId(self):
        # arrange
        mark = Player(1, 'mark', 'blue')
        finn = Player(2, 'finn', 'red')
        bob = Player(3, 'bob', 'white')
        meeting = Meeting(mark)

        # act
        meeting.add_vote(Vote(mark, bob))
        meeting.add_vote(Vote(finn, bob))
        meeting.add_vote(Vote(bob, mark))
        actual = meeting.get_ejected_player_id()

        # assert
        expected = 3
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()