import unittest
import greed

class TestGreed(unittest.TestCase):

    def test_icons_le(self):
        icons_1 = greed.Icons(0, 0, 0, 0, 0, 0)
        icons_2 = greed.Icons(1, 1, 1, 1, 1, 1)
        icons_3 = greed.Icons(1, 1, 1)
        assert icons_1 <= icons_2
        assert not icons_2 <= icons_1
        assert not icons_3 <= icons_1

    def test_tableau_play_card_subtracts_cost(self):
        tableau = greed.Tableau(10000)
        cost = greed.Cost(5000)
        card = greed.Card(greed.CardType.ACTION, 'Test Card', 1, costs=[cost])
        tableau.play_card(card)
        assert tableau.cash == 5000

    def test_tableau_play_card_requires_needs(self):
        icons = greed.Icons(1, 1, 1)
        tableau_1 = greed.Tableau(10000)
        cost = greed.Cost(5000)
        card_1 = greed.Card(greed.CardType.ACTION, 'Test Card 1', 1, costs=[cost], needs=icons)
        tableau_1.play_card(card_1)
        assert tableau_1.cash == 10000

    def test_game_start_round_increments_round_counter(self):
        player_1 = greed.Player('Player 1')
        player_2 = greed.Player('Player 2')
        game = greed.Game((player_1, player_2))
        game.start_round()
        assert game.round == 2

    def test_tableau_play_card_extends_thugs(self):
        tableau = greed.Tableau(10000)
        cost = greed.Cost(5000)
        card = greed.Card(greed.CardType.THUG, 'Test Card', 1, costs=[cost])
        tableau.play_card(card)
        assert len(tableau.thugs) == 1

    def test_tableau_play_card_extends_holdings(self):
        tableau = greed.Tableau(10000)
        cost = greed.Cost(5000)
        card = greed.Card(greed.CardType.HOLDING, 'Test Card', 1, costs=[cost])
        tableau.play_card(card)
        assert len(tableau.holdings) == 1

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
        assert len(tableau.thugs) == 0
        assert len(tableau.holdings) == 0

    def test_gain_money_equal_to_opponent_on_left(self):
        player_1 = greed.Player('Player 1')
        player_2 = greed.Player('Player 2')
        thug_1 = greed.generate_thugs()[0]
        game = greed.Game((player_1, player_2))
        game.round = 3
        game.current_player = player_1
        thug_1.when_played(game)
        player_2.tableau.cash += 10000
        assert player_1.tableau.cash == 10000
        game.round = 4
        player_2.tableau.cash += 10000
        assert player_1.tableau.cash == 10000

    def test_gain_10000_if_0_cash(self):
        player_1 = greed.Player('Player 1')
        thug_2 = greed.generate_thugs()[1]
        game = greed.Game((player_1,))
        game.current_player = player_1
        thug_2.each_turn(game)
        assert player_1.tableau.cash == 10000
        thug_2.each_turn(game)
        assert player_1.tableau.cash == 10000

    def test_gain_10000(self):
        player_1 = greed.Player('Player 1')
        thug_4 = greed.generate_thugs()[3]
        game = greed.Game((player_1,))
        game.current_player = player_1
        thug_4.when_played(game)
        assert player_1.tableau.cash == 10000

    def test_gain_5000_per_gun(self):
        player_1 = greed.Player('Player 1')
        thug_5 = greed.generate_thugs()[4]
        card_1 = greed.Card(greed.CardType.THUG, 'Test Card 1', 2, icons=greed.Icons(guns=3))
        player_1.tableau.thugs = (card_1,)
        game = greed.Game((player_1,))
        game.current_player = player_1
        thug_5.when_played(game)
        assert player_1.tableau.cash == 20000

    def test_gain_20000(self):
        player_1 = greed.Player('Player 1')
        thug_6 = greed.generate_thugs()[5]
        game = greed.Game((player_1,))
        game.current_player = player_1
        thug_6.when_played(game)
        assert player_1.tableau.cash == 20000

    def test_lose_25000(self):
        player_1 = greed.Player('Player 1')
        thug_6 = greed.generate_thugs()[5]
        game = greed.Game((player_1,))
        game.current_player = player_1
        player_1.tableau.cash = 25000
        thug_6.end_of_game(game)
        assert player_1.tableau.cash == 0

    def test_gain_10000_per_alcohol(self):
        player_1 = greed.Player('Player 1')
        thug_7 = greed.generate_thugs()[6]
        card_1 = greed.Card(greed.CardType.HOLDING, 'Test Card 1', 2, icons=greed.Icons(alcohol=3))
        player_1.tableau.holdings = (card_1,)
        game = greed.Game((player_1,))
        game.current_player = player_1
        thug_7.when_played(game)
        assert player_1.tableau.cash == 30000

    def test_place_an_extra_marker_on_holding(self):
        player_1 = greed.Player('Player 1')
        game = greed.Game((player_1,))
        game.current_player = player_1
        thug_8 = greed.generate_thugs()[7]
        thug_8.when_played(game)
        card_1 = greed.Card(greed.CardType.HOLDING, 'Test Card 1', 3, icons=greed.Icons(alcohol=3))
        player_1.tableau.play_card(card_1)
        assert player_1.tableau.holdings[0].markers == 4
        game.discard_card(thug_8)
        card_2 = greed.Card(greed.CardType.HOLDING, 'Test Card 2', 3, icons=greed.Icons(alcohol=3))
        player_1.tableau.play_card(card_2)
        assert player_1.tableau.holdings[1].markers == 6

    def test_play_reveal_a_new_thug(self):
        player_1 = greed.Player('Player 1')
        thug_9 = greed.generate_thugs()[8]
        game = greed.Game((player_1,))
        game.current_player = player_1
        thug_9.when_played(game)
        assert len(player_1.tableau.thugs) == 1
        card_1 = greed.Card(greed.CardType.THUG, 'Test Card 1', 3, costs=greed.Cost(10000), needs=greed.Icons(3, 3, 3))
        game.draw_deck.append(card_1)
        thug_9.when_played(game)
        assert player_1.tableau.thugs[-1] is card_1

    def test_play_copy_a_thug(self):
        player_1 = greed.Player('Player 1')
        thug_4 = greed.generate_thugs()[3]
        player_1.tableau.thugs = (thug_4,)
        thug_10 = greed.generate_thugs()[9]
        game = greed.Game((player_1,))
        game.current_player = player_1
        thug_10.when_played(game)
        assert len(player_1.tableau.thugs) == 2
        assert player_1.tableau.cash == 10000

    def gain_5000_per_marker_on_holding_with_the_most(self):
        player_1 = greed.Player('Player 1')
        thug_11 = greed.generate_thugs()[10]
        card_1 = greed.Card(greed.CardType.HOLDING, 'Test Card 1', 2, icons=greed.Icons(alcohol=3))
        card_2 = greed.Card(greed.CardType.HOLDING, 'Test Card 2', 2, icons=greed.Icons(alcohol=3))
        card_1.markers = 5
        player_1.tableau.holdings = (card_1, card_2)
        game = greed.Game((player_1,))
        game.current_player = player_1
        thug_11.when_played(game)
        assert player_1.tableau.cash == 25000

    def test_gain_15000_per_thug_played(self):
        player_1 = greed.Player('Player 1')
        game = greed.Game((player_1,))
        game.current_player = player_1
        thug_12 = greed.generate_thugs()[11]
        thug_12.when_played(game)
        card_1 = greed.Card(greed.CardType.THUG, 'Test Card 1', 3)
        player_1.tableau.play_card(card_1)
        assert player_1.tableau.cash == 15000
        game.discard_card(thug_12)
        card_2 = greed.Card(greed.CardType.THUG, 'Test Card 2', 3)
        player_1.tableau.play_card(card_2)
        assert player_1.tableau.cash == 15000

    def test_gain_20000_when_lost(self):
        player_1 = greed.Player('Player 1')
        game = greed.Game((player_1,))
        game.current_player = player_1
        thug_13 = greed.generate_thugs()[12]
        game.discard_card(thug_13)
        assert player_1.tableau.cash == 20000

if __name__ == '__main__':
    unittest.main()
