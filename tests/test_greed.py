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
        card = greed.Card(greed.CardType.ACTION, 'Test Card', 1, [cost])
        tableau.play_card(card)
        self.assertEqual(tableau.cash, 5000)

    def test_tableau_play_card_requires_needs_when_played(self):
        icons = greed.Icons(1, 1, 1)
        tableau_1 = greed.Tableau(10000)
        def plus_1000(tableau):
            tableau.cash += 10000
        cost = greed.Cost(5000)
        card_1 = greed.Card(greed.CardType.ACTION, 'Test Card 1', 1, [cost], needs=icons, when_played=plus_1000)
        tableau_1.play_card(card_1)
        tableau_2 = greed.Tableau(10000)
        card_2 = greed.Card(greed.CardType.ACTION, 'Test Card 2', 1, [cost], when_played=plus_1000)
        tableau_2.play_card(card_2)
        self.assertEqual(tableau_1.cash, 5000)
        self.assertEqual(tableau_2.cash, 15000)

    def test_game_start_round_increments_round_counter(self):
        player_1 = greed.Player('Player 1')
        player_2 = greed.Player('Player 2')
        game = greed.Game((player_1, player_2))
        game.start_round()
        self.assertEqual(game.round, 2)

    def test_tableau_play_card_extends_thugs(self):
        tableau = greed.Tableau(10000)
        cost = greed.Cost(5000)
        card = greed.Card(greed.CardType.THUG, 'Test Card', 1, [cost])
        tableau.play_card(card)
        self.assertEqual(len(tableau.thugs), 1)

    def test_tableau_play_card_extends_holdings(self):
        tableau = greed.Tableau(10000)
        cost = greed.Cost(5000)
        card = greed.Card(greed.CardType.HOLDING, 'Test Card', 1, [cost])
        tableau.play_card(card)
        self.assertEqual(len(tableau.holdings), 1)

    def test_tableau_pay_cost_removes_thugs_and_holdings(self):
        tableau = greed.Tableau(15000)
        cost_1 = greed.Cost(5000)
        cost_2 = greed.Cost(5000, 1, 1)
        card_1 = greed.Card(greed.CardType.THUG, 'Test Card 1', 1, [cost_1])
        card_2 = greed.Card(greed.CardType.HOLDING, 'Test Card 2', 2, [cost_1])
        card_3 = greed.Card(greed.CardType.ACTION, 'Test Card 3', 3, [cost_2])
        tableau.play_card(card_1)
        tableau.play_card(card_2)
        tableau.play_card(card_3)
        self.assertEqual(len(tableau.thugs), 0)
        self.assertEqual(len(tableau.holdings), 0)


if __name__ == '__main__':
    unittest.main()
