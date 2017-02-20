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
        card = greed.Card(greed.CardType.ACTION, 'Test Card', 1, costs=[cost])
        tableau.play_card(card)
        self.assertEqual(tableau.cash, 5000)

    def test_tableau_play_card_requires_needs(self):
        icons = greed.Icons(1, 1, 1)
        tableau_1 = greed.Tableau(10000)
        cost = greed.Cost(5000)
        card_1 = greed.Card(greed.CardType.ACTION, 'Test Card 1', 1, costs=[cost], needs=icons)
        tableau_1.play_card(card_1)
        self.assertEqual(tableau_1.cash, 10000)

    def test_game_start_round_increments_round_counter(self):
        player_1 = greed.Player('Player 1')
        player_2 = greed.Player('Player 2')
        game = greed.Game((player_1, player_2))
        game.start_round()
        self.assertEqual(game.round, 2)

    def test_tableau_play_card_extends_thugs(self):
        tableau = greed.Tableau(10000)
        cost = greed.Cost(5000)
        card = greed.Card(greed.CardType.THUG, 'Test Card', 1, costs=[cost])
        tableau.play_card(card)
        self.assertEqual(len(tableau.thugs), 1)

    def test_tableau_play_card_extends_holdings(self):
        tableau = greed.Tableau(10000)
        cost = greed.Cost(5000)
        card = greed.Card(greed.CardType.HOLDING, 'Test Card', 1, costs=[cost])
        tableau.play_card(card)
        self.assertEqual(len(tableau.holdings), 1)

    def test_tableau_pay_cost_removes_thugs_and_holdings(self):
        tableau = greed.Tableau(15000)
        cost_1 = greed.Cost(5000)
        cost_2 = greed.Cost(5000, 1, 1)
        card_1 = greed.Card(greed.CardType.THUG, 'Test Card 1', 1, costs=[cost_1])
        card_2 = greed.Card(greed.CardType.HOLDING, 'Test Card 2', 2, costs=[cost_1])
        card_3 = greed.Card(greed.CardType.ACTION, 'Test Card 3', 3, costs=[cost_2])
        tableau.play_card(card_1)
        tableau.play_card(card_2)
        tableau.play_card(card_3)
        self.assertEqual(len(tableau.thugs), 0)
        self.assertEqual(len(tableau.holdings), 0)

    def test_tableau_play_thug_1_ability(self):
        player_1 = greed.Player('Player 1')
        player_2 = greed.Player('Player 2')
        thug_1 = greed.generate_thugs()[0]
        def plus_10000(game):
            game.current_player.tableau.cash += 10000
        card = greed.Card(greed.CardType.ACTION, 'Test Card 1', 2, when_played=plus_10000)
        game = greed.Game((player_1, player_2))
        game.round = 3
        game.draft_decks[0].cards.append(thug_1)
        game.draft_decks[1].cards.append(card)
        game.start_round()
        self.assertEqual(player_1.tableau.cash, 10000)
        game.start_round()
        self.assertEqual(player_1.tableau.cash, 10000)

    def test_tableau_play_thug_2_ability(self):
        player_1 = greed.Player('Player 1')
        player_2 = greed.Player('Player 2')
        thug_2 = greed.generate_thugs()[1]
        card = greed.Card(greed.CardType.ACTION, 'Test Card 1', 2)
        game = greed.Game((player_1, player_2))
        game.round = 3
        game.draft_decks[0].cards.append(thug_2)
        game.draft_decks[1].cards.append(card)
        game.start_round()
        self.assertEqual(player_1.tableau.cash, 10000)
        game.start_round()
        self.assertEqual(player_1.tableau.cash, 10000)
        player_1.tableau.cash = 0
        game.start_round()
        self.assertEqual(player_1.tableau.cash, 10000)

    def test_tableau_play_thug_4_ability(self):
        player_1 = greed.Player('Player 1')
        player_2 = greed.Player('Player 2')
        thug_4 = greed.generate_thugs()[3]
        card = greed.Card(greed.CardType.ACTION, 'Test Card 1', 2)
        game = greed.Game((player_1, player_2))
        game.round = 3
        game.draft_decks[0].cards.append(thug_4)
        game.draft_decks[1].cards.append(card)
        game.start_round()
        self.assertEqual(player_1.tableau.cash, 10000)

    def test_tableau_play_thug_5_ability(self):
        player_1 = greed.Player('Player 1')
        player_2 = greed.Player('Player 2')
        thug_5 = greed.generate_thugs()[4]
        card = greed.Card(greed.CardType.ACTION, 'Test Card 1', 2)
        game = greed.Game((player_1, player_2))
        game.draft_decks[0].cards.append(thug_5)
        game.draft_decks[1].cards.append(card)
        game.round = 10
        game.start_round()
        self.assertEqual(player_1.tableau.cash, 20000)
        player_1.tableau.cash = 25000
        game.start_round()
        self.assertEqual(player_1.tableau.cash, 0)


if __name__ == '__main__':
    unittest.main()
