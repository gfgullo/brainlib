from brainlib.matches.Time import Time
import unittest
import time


class TestTimeClass(unittest.TestCase):

    def tearDown(self) -> None:
        pass

    @classmethod
    def setUpClass(cls) -> None:
        cls.t = Time()

    def test_normal_time(self):
        self.assertEqual(self.t.now, int(time.time()))

    def test_day(self):
        self.assertEqual(self.t.day, 3600*24)

    def test_minute(self):

        self.assertEqual(self.t.minute, 60)

    def test_second(self):
        self.assertEqual(self.t.second, 1)

    def test_hour(self):
        self.assertEqual(self.t.hour, 3600)

    def test_setting_time(self):
        t = Time(0)
        self.assertEqual(t.now, 0)
        t.set__time(10)
        self.assertEqual(t.now, 10)


if __name__ == "__main__":
    unittest.main()
