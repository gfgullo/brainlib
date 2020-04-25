import unittest
from brainlib.matches.Round import Round
from brainlib.matches.Time import Time


class TestRound(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.t = Time(0)
        cls.round = Round({}, time_object=cls.t)

    def test_resolved(self):
        self.round.time_end = 0
        self.round.deadline = self.t.day
        self.round.max_deadline = self.t.day
        self.assertEqual(self.round.resolved(), False)

        self.round.time_end = 1
        self.assertEqual(self.round.resolved(), True)

    def test_time_remaining(self):
        self.round.time_start = 0
        self.round.deadline = self.t.day
        self.assertEqual(self.t.day, self.round.time_remaining())




if __name__ == "__main__":
    unittest.main()