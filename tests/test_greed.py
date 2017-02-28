from unittest.mock import patch

import pytest

import greed

def test_deck_create_draw_deck_returns_80_cards():
    assert len(greed.deck.create_draw_deck()) == 80

@patch('builtins.input', return_value='0')
def test_game_start_round_increments_round(mock_input):
    player_1 = greed.Tableau('Test Player 1')
    player_2 = greed.Tableau('Test Player 1')
    game = greed.Game((player_1, player_2))
    game.start_round()
    assert game.current_round == 1

@patch('builtins.input', return_value='0')
def test_tableau_draft_card_adds_card_to_hand(mock_input):
    player_1 = greed.Tableau('Test Player 1')
    draft_deck = list(range(12))
    player_1.draft_card(draft_deck)
    assert len(player_1.hand) == 1

@patch('builtins.input', return_value='0')
def test_tableau_select_option_removes_card(mock_input):
    player_1 = greed.Tableau('Test Player 1')
    draft_deck = list(range(12))
    player_1.select_option(draft_deck)
    assert len(draft_deck) == 11

@patch('builtins.input', side_effect=['a', '0'])
def test_tableau_select_option_asks_for_correct_input(mock_input):
    player_1 = greed.Tableau('Test Player 1')
    draft_deck = list(range(12))
    player_1.select_option(draft_deck)
    assert len(draft_deck) == 11

def test_icons_le():
    icons_1 = greed.card.Icons(0, 0, 0, 0, 0, 0, 0, 0)
    icons_2 = greed.card.Icons(1, 1, 1, 1, 1, 1, 1, 1)
    icons_3 = greed.card.Icons(1, 1, 1)
    assert icons_1 <= icons_2
    assert not icons_2 <= icons_1
    assert not icons_3 <= icons_1

def test_icons_add():
    icons_1 = greed.card.Icons(0, 1, 0, 1, 0, 1, 0, 1)
    icons_2 = greed.card.Icons(1, 1, 1, 1, 1, 1, 1, 1)
    icons_3 = icons_1 + icons_2
    assert icons_3.guns == 1
    assert icons_3.cars == 2
    assert icons_3.keys == 1
    assert icons_3.alcohol == 2
    assert icons_3.hearts == 1
    assert icons_3.wrenches == 2
    assert icons_3.thugs == 1
    assert icons_3.holdings == 2

def test_card_invalid_card_type_raises_valueerror():
    with pytest.raises(ValueError):
        greed.Card(1, 2, 'Test Card')

def test_harveybrainsratcliffe_when_played():
    hbr = greed.deck.HarveyBrainsRatcliffe()
    player_1 = greed.Tableau('Test Player 1')
    player_2 = greed.Tableau('Test Player 2')
    game = greed.Game((player_1, player_2))
    hbr.when_played(game, player_1)
    player_2.cash += 10000
    assert player_1.cash == 10000
    game.current_round += 1
    player_2.cash += 10000
    assert player_1.cash == 10000
    game.current_round -= 1
    hbr.when_played(game, player_1)
    player_2.cash += 10000
    assert player_1.cash == 30000

@patch('builtins.input', return_value='0')
def test_tableau_pay_cost_subtracts_cost(mock_input):
    player_1 = greed.Tableau('Test Player 1', 10000)
    game = greed.Game((player_1,))
    cost = greed.card.Cost(5000)
    player_1.pay_cost(game, [cost])
    assert player_1.cash == 5000

def test_tableau_check_needs_returns_true_or_false():
    icons = greed.card.Icons(1, 1, 1, 1, 1, 1)
    player_1 = greed.Tableau('Test Player 1', 5000)
    assert player_1.check_needs(icons) is False
    card_1 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1', icons=greed.card.Icons(1, 1, 1))
    player_1.thugs.append(card_1)
    assert player_1.check_needs(icons) is False
    card_2 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1', icons=greed.card.Icons(0, 0, 0, 1, 1, 1))
    player_1.holdings.append(card_2)
    assert player_1.check_needs(icons) is True

@patch('builtins.input', return_value='0')
def test_tableau_play_card_extends_thugs(mock_input):
    player_1 = greed.Tableau('Test Player 1')
    game = greed.Game((player_1,))
    card = greed.Card(greed.card.CardType.THUG, 'Test Card', 1)
    player_1.play_card(game, card)
    assert len(player_1.thugs) == 1

@patch('builtins.input', return_value='0')
def test_tableau_play_card_extends_holdings(mock_input):
    player_1 = greed.Tableau('Test Player 1')
    game = greed.Game((player_1,))
    card = greed.Card(greed.card.CardType.HOLDING, 'Test Card', 1)
    player_1.play_card(game, card)
    assert len(player_1.holdings) == 1

@patch('builtins.input', return_value='0')
def test_tableau_pay_cost_removes_thugs(mock_input):
    player_1 = greed.Tableau('Test Player 1')
    game = greed.Game((player_1,))
    card = greed.Card(greed.card.CardType.THUG, 'Test Card', 1)
    player_1.thugs.append(card)
    cost = greed.card.Cost(thugs=1)
    player_1.pay_cost(game, [cost])
    assert len(player_1.thugs) == 0

@patch('builtins.input', return_value='0')
def test_tableau_pay_cost_removes_holdings(mock_input):
    player_1 = greed.Tableau('Test Player 1')
    game = greed.Game((player_1,))
    card = greed.Card(greed.card.CardType.HOLDING, 'Test Card', 1)
    player_1.holdings.append(card)
    cost = greed.card.Cost(holdings=1)
    player_1.pay_cost(game, [cost])
    assert len(player_1.holdings) == 0

@patch('builtins.input', return_value='0')
def test_tableau_play_card_discards_costs(mock_input):
    player_1 = greed.Tableau('Test Player 1')
    game = greed.Game((player_1,))
    card_1 = greed.Card(greed.card.CardType.HOLDING, 'Test Card', 1)
    player_1.holdings.append(card_1)
    cost = greed.card.Cost(holdings=1)
    card_2 = greed.Card(greed.card.CardType.HOLDING, 'Test Card', 1, costs=[cost])
    player_1.play_card(game, card_2)
    assert len(game.discard_deck) == 1

def test_game_end_round_rotates_draft_decks():
    player_1 = greed.Tableau('Test Player 1')
    player_2 = greed.Tableau('Test Player 2')
    game = greed.Game((player_1, player_2))
    game.draft_decks = [1, 2]
    game.end_round()
    assert game.draft_decks == [2,1]

@patch('builtins.input', return_value='0')
def test_tableau_play_card_discards_card_if_needs_or_cost_not_met(mock_input):
    player_1 = greed.Tableau('Test Player 1')
    game = greed.Game((player_1,))
    card_1 = greed.Card(greed.card.CardType.HOLDING, 'Test Card 1', 1, needs=greed.card.Icons(keys=1))
    card_2 = greed.Card(greed.card.CardType.HOLDING, 'Test Card 2', 1, costs=[greed.card.Cost(holdings=1)])
    player_1.play_card(game, card_1)
    player_1.play_card(game, card_2)
    assert len(game.discard_deck) == 2
    assert len(player_1.holdings) == 0

@patch('builtins.input', return_value='0')
def test_tableau_player_card_discards_actions(mock_input):
    player_1 = greed.Tableau('Test Player 1')
    game = greed.Game((player_1,))
    card = greed.Card(greed.card.CardType.ACTION, 'Test Card', 1)
    player_1.play_card(game, card)
    assert len(game.discard_deck) == 1

def test_biscuitsomalley_each_turn():
    bom = greed.deck.BiscuitsOMalley()
    player_1 = greed.Tableau('Test Player 1')
    game = greed.Game((player_1,))
    bom.each_turn(game, player_1)
    assert player_1.cash == 10000
    bom.each_turn(game, player_1)
    assert player_1.cash == 10000