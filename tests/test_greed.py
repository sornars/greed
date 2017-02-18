import unittest
import greed

class TestGreed(unittest.TestCase):

    def test_icons_le(self):
        icons_1 = greed.Icons(0, 0, 0, 0, 0, 0)
        icons_2 = greed.Icons(1, 1, 1, 1, 1, 1)
        icons_3 = greed.Icons(1, 1, 1)
        self.assertTrue(icons_1 <= icons_2)
        self.assertFalse(icons_2 <= icons_1)
        self.assertFalse(icons_3 <= icons_1)

    def test_tableau_play_card_subtracts_cost(self):
        tableau = greed.Tableau(10000)
        cost = greed.Cost(5000)
        card = greed.Card("Test Card", 1, [cost])
        tableau.play_card(card)
        self.assertEqual(tableau.cash, 5000)

    def test_tableau_play_card_requires_needs_when_played(self):
        icons = greed.Icons(1, 1, 1)
        tableau_1 = greed.Tableau(10000)
        def plus_1000(tableau):
            tableau.cash += 10000
        cost = greed.Cost(5000)
        card_1 = greed.Card("Test Card", 1, [cost], needs=icons, when_played=plus_1000)
        tableau_1.play_card(card_1)
        print(card_1.needs, tableau_1.calculate_icons())
        tableau_2 = greed.Tableau(10000)
        card_2 = greed.Card("Test Card", 1, [cost], when_played=plus_1000)
        tableau_2.play_card(card_2)
        self.assertEqual(tableau_1.cash, 5000)
        self.assertEqual(tableau_2.cash, 15000)



if __name__ == '__main__':
    unittest.main()
