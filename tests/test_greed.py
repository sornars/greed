import unittest
import greed

class TestGreed(unittest.TestCase):

    def test_icons_le(self):
        i1 = greed.Icons(0, 0, 0, 0, 0, 0)
        i2 = greed.Icons(1, 1, 1, 1, 1, 1)
        self.assertTrue(i1 < i2)

    def test_tableau_play_card_subtracts_cost(self):
        t = greed.Tableau(10000)
        c = greed.Card("Test Card", 1, 5000)
        t.play_card(c)
        self.assertEquals(t.cash, 5000)


if __name__ == '__main__':
    unittest.main()
