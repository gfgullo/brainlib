import unittest
from mockfirestore import MockFirestore
from brainlib import Match


class TestOpponent(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.match = Match.Match({
            "Marco": {"username": "marco", "uid": "Marco"},
            "Nico": {"username": "nico", "uid": "Nico"},
            "users": ["Marco", "Nico"]

        }, db=MockFirestore)

    def test_opponent(self):
        user = self.match.get_opponent("Marco")
        self
        self.assertEqual(user.uid, "Nico")
        self.assertEqual(user.username, "nico")

    def test_get_user(self):
        u = self.match.get_user("Marco")
        u1 = self.match.get_user("Nico")

        self.assertEqual(u.uid, "Marco")
        self.assertEqual(u1.uid, "Nico")


if __name__ == "__main__":
    unittest.main()