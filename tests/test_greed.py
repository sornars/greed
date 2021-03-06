from unittest.mock import patch

import pytest

import greed

def test_deck_create_draw_deck_returns_80_cards():
    assert len(greed.deck.create_draw_deck()) == 80

@patch('builtins.input', return_value='0')
def test_game_start_round_increments_round(mock_input):
    player_1 = greed.ConsoleTableau('Test Player 1')
    player_2 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1, player_2))
    game.start_round()
    assert game.current_round == 1

@patch('builtins.input', return_value='0')
def test_tableau_draft_card_adds_card_to_hand(mock_input):
    player_1 = greed.ConsoleTableau('Test Player 1')
    draft_deck = list(range(12))
    player_1.draft_card(draft_deck)
    assert len(player_1.hand) == 1

@patch('builtins.input', return_value='0')
def test_tableau_select_option_removes_card(mock_input):
    player_1 = greed.ConsoleTableau('Test Player 1')
    draft_deck = list(range(12))
    _, draft_deck = player_1.select_option(draft_deck)
    assert len(draft_deck) == 11
    _, draft_deck = player_1.select_option(draft_deck, remove_option=False)
    assert len(draft_deck) == 11


@patch('builtins.input', side_effect=['a', '0'])
def test_tableau_select_option_asks_for_correct_input(mock_input):
    player_1 = greed.ConsoleTableau('Test Player 1')
    draft_deck = list(range(12))
    _, draft_deck = player_1.select_option(draft_deck)
    assert len(draft_deck) == 11

def test_icons_le():
    icons_1 = greed.card.Icons(0, 0, 0, 0, 0, 0, 0, 0)
    icons_2 = greed.card.Icons(1, 1, 1, 1, 1, 1, 1, 1)
    icons_3 = greed.card.Icons(1, 1, 1)
    assert icons_1 <= icons_2
    assert not icons_2 <= icons_1
    assert not icons_3 <= icons_1

def test_icons_add():
    icons_1 = greed.card.Icons(0, 1, 0, 1, 0, 1, 0, 1, 0)
    icons_2 = greed.card.Icons(1, 1, 1, 1, 1, 1, 1, 1, 1)
    icons_3 = icons_1 + icons_2
    assert icons_3.guns == 1
    assert icons_3.cars == 2
    assert icons_3.keys == 1
    assert icons_3.alcohol == 2
    assert icons_3.hearts == 1
    assert icons_3.wrenches == 2
    assert icons_3.cash == 1
    assert icons_3.thugs == 2
    assert icons_3.holdings == 1

def test_card_invalid_card_type_raises_valueerror():
    with pytest.raises(ValueError):
        greed.Card(1, 2, 'Test Card')

def test_harveybrainsratcliffe_when_played():
    hbr = greed.deck.HarveyBrainsRatcliffe()
    player_1 = greed.ConsoleTableau('Test Player 1')
    player_2 = greed.ConsoleTableau('Test Player 2')
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
    player_1 = greed.ConsoleTableau('Test Player 1', 10000)
    game = greed.Game((player_1,))
    card = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1', costs=[greed.card.Cost(5000)])
    player_1.pay_cost(game, card)
    assert player_1.cash == 5000

def test_tableau_check_needs_returns_true_or_false():
    icons = greed.card.Icons(1, 1, 1, 1, 1, 1)
    player_1 = greed.ConsoleTableau('Test Player 1', 5000)
    assert player_1.check_needs(icons) is False
    card_1 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1', icons=greed.card.Icons(1, 1, 1))
    player_1.thugs.append(card_1)
    assert player_1.check_needs(icons) is False
    card_2 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1', icons=greed.card.Icons(0, 0, 0, 1, 1, 1))
    player_1.holdings.append(card_2)
    assert player_1.check_needs(icons) is True

@patch('builtins.input', return_value='0')
def test_tableau_play_card_extends_thugs(mock_input):
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    card = greed.Card(greed.card.CardType.THUG, 'Test Card', 1)
    player_1.play_card(game, card)
    assert len(player_1.thugs) == 1

@patch('builtins.input', return_value='0')
def test_tableau_play_card_extends_holdings(mock_input):
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    card = greed.Card(greed.card.CardType.HOLDING, 'Test Card', 1)
    player_1.play_card(game, card)
    assert len(player_1.holdings) == 1

@patch('builtins.input', return_value='0')
def test_tableau_pay_cost_removes_thugs(mock_input):
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    card_1 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1')
    player_1.thugs.append(card_1)
    card_2 = greed.Card(greed.card.CardType.THUG, 2, 'Test Card 2', costs=[greed.card.Cost(thugs=1)])
    player_1.pay_cost(game, card_2)
    assert len(player_1.thugs) == 0

@patch('builtins.input', return_value='0')
def test_tableau_pay_cost_removes_holdings(mock_input):
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    player_1.holdings.append(card_1)
    card_2 = greed.Card(greed.card.CardType.THUG, 2, 'Test Card 2', costs=[greed.card.Cost(holdings=1)])
    player_1.pay_cost(game, card_2)
    assert len(player_1.holdings) == 0

@patch('builtins.input', return_value='0')
def test_tableau_pay_cost_removes_cards(mock_input):
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    player_1.hand.append(card_1)
    card_2 = greed.Card(greed.card.CardType.THUG, 2, 'Test Card 2', costs=[greed.card.Cost(cards=1)])
    player_1.pay_cost(game, card_2)
    assert len(player_1.hand) == 0

@patch('builtins.input', return_value='0')
def test_tableau_play_card_discards_costs(mock_input):
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card')
    player_1.holdings.append(card_1)
    cost = greed.card.Cost(holdings=1)
    card_2 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card', costs=[cost])
    player_1.play_card(game, card_2)
    assert len(game.discard_deck) == 1

def test_game_end_round_rotates_draft_decks():
    player_1 = greed.ConsoleTableau('Test Player 1')
    player_2 = greed.ConsoleTableau('Test Player 2')
    game = greed.Game((player_1, player_2))
    game.draft_decks = [1, 2]
    game.end_round()
    assert game.draft_decks == [2,1]

@patch('builtins.input', return_value='0')
def test_tableau_play_card_discards_card_if_needs_or_cost_not_met(mock_input):
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    card_1 = greed.Card(greed.card.CardType.HOLDING, 'Test Card 1', 1, needs=greed.card.Icons(keys=1))
    card_2 = greed.Card(greed.card.CardType.HOLDING, 'Test Card 2', 1, costs=[greed.card.Cost(holdings=1)])
    player_1.play_card(game, card_1)
    player_1.play_card(game, card_2)
    assert len(game.discard_deck) == 2
    assert len(player_1.holdings) == 0

@patch('builtins.input', return_value='0')
def test_tableau_player_card_discards_actions(mock_input):
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    card = greed.Card(greed.card.CardType.ACTION, 'Test Card', 1)
    player_1.play_card(game, card)
    assert len(game.discard_deck) == 1

def test_biscuitsomalley_each_turn():
    bom = greed.deck.BiscuitsOMalley()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    bom.each_turn(game, player_1)
    assert player_1.cash == 10000
    bom.each_turn(game, player_1)
    assert player_1.cash == 10000

def test_dickieflushdiamond_when_played():
    dfd = greed.deck.DickieFlushDiamond()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    dfd.when_played(game, player_1)
    assert player_1.cash == 10000

@patch.object(greed.card.Card, 'each_turn')
@patch('builtins.input', return_value='0')
def test_game_start_round_calls_each_turn(mock_input, mock_each_turn):
    player_1 = greed.ConsoleTableau('Test Player 1')
    card = greed.Card(greed.card.CardType.THUG, 1, 'Test Card')
    player_1.thugs.append(card)
    game = greed.Game((player_1,))
    game.current_round = 3
    game.start_round()
    mock_each_turn.assert_called()

def test_edcheeseclothmcguinty_when_played():
    ecm = greed.deck.EdCheeseclothMcGuinty()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    ecm.when_played(game, player_1)
    assert player_1.cash == 5000
    card = greed.Card(greed.card.CardType.THUG, 1, 'Test Card', icons=greed.card.Icons(guns=3))
    player_1.thugs.append(card)
    ecm.when_played(game, player_1)
    assert player_1.cash == 25000

def test_generousjenniejones_when_played():
    gjj = greed.deck.GenerousJennieJones()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    gjj.when_played(game, player_1)
    assert player_1.cash == 20000

def test_generousjenniejones_end_of_game():
    gjj = greed.deck.GenerousJennieJones()
    player_1 = greed.ConsoleTableau('Test Player 1')
    player_1.cash = 25000
    game = greed.Game((player_1,))
    gjj.end_of_game(game, player_1)
    assert player_1.cash == 0

@patch.object(greed.card.Card, 'end_of_game')
@patch('builtins.input', return_value='0')
def test_game_end_round_calls_end_of_game(mock_input, mock_end_of_game):
    player_1 = greed.ConsoleTableau('Test Player 1')
    card = greed.Card(greed.card.CardType.THUG, 1, 'Test Card')
    player_1.thugs.append(card)
    game = greed.Game((player_1,))
    game.current_round = 12
    game.end_round()
    mock_end_of_game.assert_called()

def test_mickeyistari_when_played():
    mi = greed.deck.MickeyIstari()
    player_1 = greed.ConsoleTableau('Test Player 1')
    card = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card', icons=greed.card.Icons(alcohol=3))
    player_1.holdings.append(card)
    game = greed.Game((player_1,))
    mi.when_played(game, player_1)
    assert player_1.cash == 30000

def test_wolfgangbuttercup_when_played_and_on_discard():
    wb = greed.deck.WolfgangButtercup()
    player_1 = greed.ConsoleTableau('Test Player 1')
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card', icons=greed.card.Icons(alcohol=3))
    game = greed.Game((player_1,))
    wb.when_played(game, player_1)
    player_1.play_holding(game, card_1)
    assert card_1.markers == 4
    card_2 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card', icons=greed.card.Icons(alcohol=3))
    wb.on_discard(game, player_1)
    player_1.play_holding(game, card_2)
    assert card_2.markers == 6

def test_tableau_calculate_markers():
    player_1 = greed.ConsoleTableau('Test Player 1')
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card', icons=greed.card.Icons(alcohol=3))
    player_1.holdings.append(card_1)
    assert player_1.calculate_markers(card_1) == 3
    card_2 = greed.Card(greed.card.CardType.HOLDING, 2, 'Test Card', icons=greed.card.Icons(wrenches=2))
    player_1.holdings.append(card_2)
    assert player_1.calculate_markers(card_2) == 2
    player_1.holdings.append(card_1)
    assert player_1.calculate_markers(card_1) == 6

def test_tableau_place_markers():
    player_1 = greed.ConsoleTableau('Test Player 1')
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card', icons=greed.card.Icons(alcohol=3))
    player_1.holdings.append(card_1)
    player_1.place_markers(card_1)
    assert card_1.markers == 3
    card_2 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card', icons=greed.card.Icons(alcohol=3))
    player_1.holdings.append(card_2)
    player_1.place_markers(card_2)
    assert card_2.markers == 6

def test_polycephaluspatriciajones_when_played():
    ppj = greed.deck.PolycephalusPatriciaJones()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card')
    card_2 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card')
    card_3 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card')
    game.draw_deck = [card_3, card_2, card_1]
    ppj.when_played(game, player_1)
    assert len(player_1.thugs) == 1
    assert len(game.discard_deck) == 2

@patch('builtins.input', return_value='0')
def test_edrubberfaceteach_when_played(mock_input):
    ert = greed.deck.EdRubberfaceTeach()
    dfd = greed.deck.DickieFlushDiamond()
    player_1 = greed.ConsoleTableau('Test Player 1')
    player_1.thugs.append(dfd)
    game = greed.Game((player_1,))
    ert.when_played(game, player_1)
    assert len(player_1.thugs) == 1
    assert player_1.cash == 10000

def test_peepingtomthumb_when_played():
    ptt = greed.deck.PeepingTomThumb()
    player_1 = greed.ConsoleTableau('Test Player 1')
    player_2 = greed.ConsoleTableau('Test Player 2')
    game = greed.Game((player_1, player_2))
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card')
    card_1.markers = 3
    card_2 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card')
    card_2.markers = 5
    player_1.holdings.append(card_1)
    player_2.holdings.append(card_2)
    ptt.when_played(game, player_1)
    assert player_1.cash == 25000

@patch('builtins.input', return_value='0')
def test_friendlyguscaspar_when_played_and_on_discard(mock_input):
    fgc = greed.deck.FriendlyGusCaspar()
    player_1 = greed.ConsoleTableau('Test Player 1')
    card_1 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1')
    game = greed.Game((player_1,))
    fgc.when_played(game, player_1)
    player_1.play_card(game, card_1)
    assert player_1.cash == 15000
    card_2 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 2')
    fgc.on_discard(game, player_1)
    player_1.play_card(game, card_2)
    assert player_1.cash == 15000

def test_halloweenjackparis_on_discard():
    hjp = greed.deck.HalloweenJackParis()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    hjp.on_discard(game, player_1)
    assert player_1.cash == 20000

@patch('builtins.input', return_value='0')
def test_vicioussydvarney_when_played(mock_input):
    vsv = greed.deck.ViciousSydVarney()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    vsv.when_played(game, player_1)
    player_1.cash += 10000
    game.current_round += 1
    card_1 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1', costs=[greed.card.Cost(cash=5000)])
    player_1.play_card(game, card_1)
    assert player_1.cash == 10000
    game.current_round += 1
    card_2 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1', costs=[greed.card.Cost(cash=5000)])
    player_1.play_card(game, card_2)
    assert player_1.cash == 5000

@patch('builtins.input', return_value='0')
def test_rottenjohnnysimmons_when_played(mock_input):
    rjs = greed.deck.RottenJohnnySimmons()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    rjs.when_played(game, player_1)
    game.current_round += 1
    card_1 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1', needs=greed.card.Icons(thugs=1))
    player_1.play_card(game, card_1)
    assert len(player_1.thugs) == 1
    game.current_round += 1
    card_2 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1', needs=greed.card.Icons(thugs=2))
    player_1.play_card(game, card_2)
    assert len(player_1.thugs) == 1

def test_randomscrubpatterson_when_played():
    rsp = greed.deck.RandomScrubPatterson()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    card = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1', icons=greed.card.Icons(keys=3))
    player_1.thugs.append(card)
    rsp.when_played(game, player_1)
    assert len(player_1.hand) == 4

@patch('builtins.input', return_value='0')
def test_stingystanmcdowell_when_played(mock_input):
    ssm = greed.deck.StingyStanMcDowell()
    player_1 = greed.ConsoleTableau('Test Player 1')
    player_1.cash = 15000
    game = greed.Game((player_1,))
    ssm.when_played(game, player_1)
    card = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1', costs=[greed.card.Cost(cash=10000)])
    player_1.pay_cost(game, card)
    assert player_1.cash == 10000
    ssm.on_discard(game, player_1)
    player_1.pay_cost(game, card)
    assert player_1.cash == 0

@patch('builtins.input', return_value='0')
def test_louiesavoirofarrell_when_played(mock_input):
    lso = greed.deck.LouieSavoirOFarrell()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    lso.when_played(game, player_1)
    card = greed.Card(greed.card.CardType.THUG, 1, 'Test Card')
    player_1.hand.append(card)
    game.current_round += 1
    game.end_round()
    assert len(player_1.thugs) == 1
    game.current_round += 1
    game.end_round()

def test_tableau_select_options_raise_valueerror_with_no_options():
    player_1 = greed.ConsoleTableau('Test Player 1')
    with pytest.raises(ValueError):
        player_1.select_option([])

@patch('builtins.input', return_value='0')
def test_peterepeatfell_when_played(mock_input):
    prf = greed.deck.PeteRepeatFell()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    prf.when_played(game, player_1)
    game.current_round += 1
    card_1 = greed.Card(greed.card.CardType.ACTION, 1, 'Test Card 1')
    player_1.play_card(game, card_1)
    assert len(game.discard_deck) == 0
    assert card_1 in player_1.hand
    game.current_round += 1
    card_2 = greed.Card(greed.card.CardType.ACTION, 1, 'Test Card 2')
    player_1.play_card(game, card_2)
    assert len(game.discard_deck) == 1

def test_nataschathesquirrelrubin_each_turn():
    ntsr = greed.deck.NataschaTheSquirrelRubin()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    ntsr.each_turn(game, player_1)
    assert player_1.cash == 5000

@patch('builtins.input', return_value='0')
def test_nothingbeatsrockbenson_when_played_and_on_discard(mock_input):
    nbrb = greed.deck.NothingbeatsRockBenson()
    player_1 = greed.ConsoleTableau('Test Player 1')
    card_1 = greed.Card(greed.card.CardType.ACTION, 1, 'Test Card 1')
    game = greed.Game((player_1,))
    nbrb.when_played(game, player_1)
    player_1.play_card(game, card_1)
    assert player_1.cash == 5000
    card_2 = greed.Card(greed.card.CardType.ACTION, 1, 'Test Card 2')
    nbrb.on_discard(game, player_1)
    player_1.play_card(game, card_2)
    assert player_1.cash == 5000

@patch('builtins.input', return_value='0')
def test_eugenethebutchermidge_when_played_and_on_discard(mock_input):
    etbm = greed.deck.EugeneTheButcherMidge()
    player_1 = greed.ConsoleTableau('Test Player 1')
    card_1 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1', icons=greed.card.Icons(guns=3))
    card_2 = greed.Card(greed.card.CardType.ACTION, 2, 'Test Card 2')
    player_1.thugs.append(card_1)
    game = greed.Game((player_1,))
    etbm.when_played(game, player_1)
    player_1.play_card(game, card_2)
    assert player_1.cash == 15000
    card_3 = greed.Card(greed.card.CardType.ACTION, 3, 'Test Card 3')
    etbm.on_discard(game, player_1)
    player_1.play_card(game, card_3)
    assert player_1.cash == 15000

@patch('builtins.input', return_value='0')
def test_tednapoleonbonham_when_played(mock_input):
    tnb = greed.deck.TedNapoleonBonham()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    tnb.when_played(game, player_1)
    game.start_round()
    assert tnb.icons == greed.card.Icons(guns=1, cars=1, keys=1)
    game.start_round()
    assert tnb.icons == greed.card.Icons(cars=1)

def test_bobbycourduroybrown_when_played():
    bcb = greed.deck.BobbyCourduroyBrown()
    player_1 = greed.ConsoleTableau('Test Player 1')
    player_1.cash = 15000
    player_2 = greed.ConsoleTableau('Test Player 2')
    player_2.cash = 15000
    player_3 = greed.ConsoleTableau('Test Player 3')
    player_3.cash = 5000
    game = greed.Game((player_1, player_2, player_3))
    bcb.when_played(game, player_1)
    assert player_1.cash == 15000
    assert player_2.cash == 5000
    assert player_3.cash == 0

def test_jackcrackerjohnson_when_played():
    jct = greed.deck.JackCrackerThompson()
    player_1 = greed.ConsoleTableau('Test Player 1')
    player_1.cash = 15000
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    player_1.holdings.append(card_1)
    player_2 = greed.ConsoleTableau('Test Player 2')
    player_2.cash = 15000
    card_2 = greed.Card(greed.card.CardType.HOLDING, 2, 'Test Card 2')
    player_2.holdings.append(card_2)
    player_3 = greed.ConsoleTableau('Test Player 3')
    player_3.cash = 5000
    card_3 = greed.Card(greed.card.CardType.HOLDING, 3, 'Test Card 3')
    card_4 = greed.Card(greed.card.CardType.HOLDING, 4, 'Test Card 4')
    player_3.holdings.append(card_3)
    player_3.holdings.append(card_4)
    game = greed.Game((player_1, player_2, player_3))
    jct.when_played(game, player_1)
    assert player_1.cash == 15000
    assert player_2.cash == 10000
    assert player_3.cash == 0

def test_dollsoncall_each_turn():
    doc = greed.deck.DollsOnCall()
    player_1 = greed.ConsoleTableau('Test Player 1')
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    player_1.holdings.append(card_1)
    player_2 = greed.ConsoleTableau('Test Player 2')
    card_2 = greed.Card(greed.card.CardType.HOLDING, 2, 'Test Card 2')
    card_3 = greed.Card(greed.card.CardType.HOLDING, 3, 'Test Card 3')
    player_2.holdings.append(card_2)
    game = greed.Game((player_1, player_2))
    doc.each_turn(game, player_1)
    assert player_1.cash == 0
    assert player_2.cash == 0
    player_2.holdings.append(card_3)
    doc.each_turn(game, player_1)
    assert player_1.cash == 0
    assert player_2.cash == 5000

def test_tommyscashnammo_when_played():
    tcna = greed.deck.TommysCashNAmmo()
    player_1 = greed.ConsoleTableau('Test Player 1')
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    card_1.markers = 3
    player_2 = greed.ConsoleTableau('Test Player 2')
    card_2 = greed.Card(greed.card.CardType.HOLDING, 2, 'Test Card 2')
    card_2.markers = 3
    card_3 = greed.Card(greed.card.CardType.HOLDING, 3, 'Test Card 3')
    card_3.markers = 0
    player_2.holdings.append(card_2)
    player_2.holdings.append(card_3)
    game = greed.Game((player_1, player_2))
    tcna.when_played(game, player_1)
    assert card_1.markers == 3
    assert card_2.markers == 2
    assert card_3.markers == 0

@patch.object(greed.card.Card, 'when_played')
def test_hideout_when_played(mock_when_played):
    h = greed.deck.Hideout()
    player_1 = greed.ConsoleTableau('Test Player 1')
    card_1 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1')
    player_1.thugs.append(card_1)
    game = greed.Game((player_1,))
    h.when_played(game, player_1)
    mock_when_played.assert_called_once()

def test_trotskysburlesque_each_turn():
    tb = greed.deck.TrotskysBurlesque()
    player_1 = greed.ConsoleTableau('Test Player 1')
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1', icons=greed.card.Icons(hearts=3))
    player_1.holdings.append(card_1)
    player_2 = greed.ConsoleTableau('Test Player 2')
    card_2 = greed.Card(greed.card.CardType.HOLDING, 2, 'Test Card 2', icons=greed.card.Icons(hearts=2))
    player_2.holdings.append(card_2)
    game = greed.Game((player_1, player_2))
    tb.each_turn(game, player_1)
    assert player_1.cash == 5000

def test_joesginjoint_when_played():
    jgj = greed.deck.JoesGinJoint()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    jgj.when_played(game, player_1)
    assert jgj.markers == 2

def test_theritz_when_played():
    tr = greed.deck.TheRitz()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    tr.when_played(game, player_1)
    assert tr.markers == 5

def test_junkyard_when_played_and_end_of_game():
    j = greed.deck.Junkyard()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    j.when_played(game, player_1)
    player_1.holdings.append(j)
    player_1.place_markers(j)
    assert j.markers == 0
    j.end_of_game(game, player_1)
    assert j.markers == 1

@patch('builtins.input', return_value='0')
def test_zoningoffice_when_played_and_on_discard(mock_input):
    zo = greed.deck.ZoningOffice()
    player_1 = greed.ConsoleTableau('Test Player 1')
    player_1.cash += 10000
    game = greed.Game((player_1,))
    zo.when_played(game, player_1)
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1', costs=[greed.card.Cost(cash=10000)])
    player_1.play_card(game, card_1)
    assert len(player_1.holdings) == 1
    assert player_1.cash == 10000
    zo.on_discard(game, player_1)
    card_2 = greed.Card(greed.card.CardType.HOLDING, 2, 'Test Card 2', costs=[greed.card.Cost(cash=10000)])
    player_1.play_card(game, card_2)
    assert len(player_1.holdings) == 2
    assert player_1.cash == 0

def test_bookiejoint_end_of_game():
    bj = greed.deck.BookieJoint()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    bj.markers = 3
    bj.end_of_game(game, player_1)
    assert player_1.cash == 15000

def test_headquarters_when_played():
    hq = greed.deck.Headquarters()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    card = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    player_1.holdings.append(card)
    player_1.holdings.append(card)
    hq.when_played(game, player_1)
    assert hq.markers == 3

def test_paddyspub_when_played():
    pp = greed.deck.PaddysPub()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    card = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1', icons=greed.card.Icons(cars=3))
    player_1.thugs.append(card)
    pp.when_played(game, player_1)
    assert pp.markers == 3

def test_sexysadies_each_turn():
    ss = greed.deck.SexySadies()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    ss.each_turn(game, player_1)
    assert player_1.cash == 0
    ss.markers = 3
    ss.each_turn(game, player_1)
    assert player_1.cash == 5000

def test_loanshark_when_played():
    ls = greed.deck.Loanshark()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    ls.when_played(game, player_1)
    assert player_1.cash == 20000
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1', icons=greed.card.Icons(hearts=1))
    player_1.play_holding(game, card_1)
    assert card_1.markers == 0
    card_2 = greed.Card(greed.card.CardType.HOLDING, 2, 'Test Card 2', icons=greed.card.Icons(hearts=1))
    ls.on_discard(game, player_1)
    player_1.play_holding(game, card_2)
    assert card_2.markers == 2

def test_poorhouse_each_turn():
    ph = greed.deck.PoorHouse()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    ph.each_turn(game, player_1)
    assert player_1.cash == 5000
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    card_2 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1')
    player_1.holdings.append(card_1)
    player_1.holdings.append(card_1)
    player_1.thugs.append(card_2)
    player_1.thugs.append(card_2)
    ph.each_turn(game, player_1)
    assert player_1.cash == 10000
    player_1.holdings.append(card_1)
    ph.each_turn(game, player_1)
    assert player_1.cash == 10000

def test_jennyswaterfrontdive_each_turn():
    jwd = greed.deck.JennysWaterfrontDive()
    player_1 = greed.ConsoleTableau('Test Player 1')
    player_2 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1, player_2))
    jwd.each_turn(game, player_1)
    assert player_1.cash == 10000
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1', icons=greed.card.Icons(wrenches=1))
    player_2.holdings.append(card_1)
    jwd.each_turn(game, player_1)
    assert player_1.cash == 20000
    card_2 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1', icons=greed.card.Icons(hearts=1))
    player_2.holdings.append(card_2)
    jwd.each_turn(game, player_1)
    assert player_1.cash == 20000
    player_2.holdings.pop()
    card_3 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1', icons=greed.card.Icons(alcohol=1))
    player_1.holdings.append(card_3)
    jwd.each_turn(game, player_1)
    assert player_1.cash == 20000

@patch('builtins.input', return_value='0')
def test_sandyssnookernschnapps_when_played_and_on_discard(mock_input):
    ssns = greed.deck.SandysSnookerNSchanpps()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    ssns.when_played(game, player_1)
    card = greed.Card(greed.card.CardType.ACTION, 1, 'Test Card 1')
    player_1.play_card(game, card)
    assert ssns.markers == 1
    ssns.on_discard(game, player_1)
    player_1.play_card(game, card)
    assert ssns.markers == 1

def test_six_corners_when_played():
    sc = greed.deck.SixCorners()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    card = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    player_1.holdings.append(card)
    sc.when_played(game, player_1)
    assert card.markers == 1
    assert sc.markers == 1

def test_lamontesescortservice_end_of_game():
    les = greed.deck.LamontesEscortService()
    player_1 = greed.ConsoleTableau('Test Player 1')
    player_2 = greed.ConsoleTableau('Test Player 2')
    game = greed.Game((player_1, player_2))
    card = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1')
    player_1.thugs.append(card)
    player_2.thugs.append(card)
    les.end_of_game(game, player_1)
    assert player_1.cash == 0
    assert player_2.cash == 0
    player_1.thugs.append(card)
    les.end_of_game(game, player_1)
    assert player_1.cash == 20000
    assert player_2.cash == 0

@patch('builtins.input', return_value='0')
def test_insuranceoffice_when_played(mock_input):
    io = greed.deck.InsuranceOffice()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    card_1 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1')
    card_2 = greed.Card(greed.card.CardType.HOLDING, 2, 'Test Card 2')
    player_1.thugs.append(card_1)
    player_1.holdings.append(card_2)
    io.when_played(game, player_1)
    player_1.discard_thug(game)
    assert io.markers == 2
    player_1.discard_holding(game)
    assert io.markers == 4
    io.markers -= 1
    assert io.markers == 4
    io.markers += 1
    assert io.markers == 5

def test_shakedown_when_played():
    s = greed.deck.Shakedown()
    player_1 = greed.ConsoleTableau('Test Player 1')
    player_2 = greed.ConsoleTableau('Test Player 2')
    player_3 = greed.ConsoleTableau('Test Player 3')
    player_4 = greed.ConsoleTableau('Test Player 4')
    game = greed.Game((player_1, player_2, player_3, player_4))
    s.when_played(game, player_1)
    assert player_1.cash == 10000
    card_1 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1')
    player_2.play_thug(game, card_1)
    assert player_1.cash == 20000
    player_3.play_thug(game, card_1)
    assert player_1.cash == 20000
    player_4.play_thug(game, card_1)
    assert player_1.cash == 30000

def test_tableau_cash_cannot_be_negative():
    player_1 = greed.ConsoleTableau('Test Player 1')
    player_1.cash = -1
    assert player_1.cash == 0

def test_arson_when_played():
    a = greed.deck.Arson()
    player_1 = greed.ConsoleTableau('Test Player 1')
    player_1.cash = 25000
    player_2 = greed.ConsoleTableau('Test Player 2')
    player_2.cash = 25000
    game = greed.Game((player_1, player_2))
    card_1 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1')
    player_1.thugs.append(card_1)
    player_1.thugs.append(card_1)
    a.when_played(game, player_1)
    assert player_1.cash == 25000
    assert player_2.cash == 5000

def test_sting_when_played():
    s = greed.deck.Sting()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    card_1 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1', icons=greed.card.Icons(cars=3))
    card_2 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1', icons=greed.card.Icons(hearts=3))
    player_1.thugs.append(card_1)
    player_1.holdings.append(card_2)
    s.when_played(game, player_1)
    assert player_1.cash == 60000

def test_museumheist_when_played():
    mh = greed.deck.MuseumHeist()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    mh.when_played(game, player_1)
    assert player_1.cash == 25000

def test_streetwalkers_when_played():
    sw = greed.deck.StreetWalkers()
    player_1 = greed.ConsoleTableau('Test Player 1')
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    card_2= greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 2')
    player_1.holdings.append(card_1)
    player_1.holdings.append(card_2)
    game = greed.Game((player_1,))
    sw.when_played(game, player_1)
    assert card_1.markers == 1
    assert card_2.markers == 1

def test_card_markers_cannot_be_negative():
    card = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    card.markers = -1
    assert card.markers == 0

def test_raid_when_played():
    r = greed.deck.Raid()
    player_1 = greed.ConsoleTableau('Test Player 1')
    player_2 = greed.ConsoleTableau('Test Player 2')
    card = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    card.markers = 5
    player_2.holdings.append(card)
    game = greed.Game((player_1, player_2))
    r.when_played(game, player_1)
    assert card.markers == 4

def test_masterplan_when_played():
    mp = greed.deck.MasterPlan()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    mp.when_played(game, player_1)
    game.current_round += 1
    player_1.cash += 5000
    assert player_1.cash == 10000
    game.current_round += 1
    player_1.cash += 5000
    assert player_1.cash == 15000

def test_protectionracket_when_played():
    pr = greed.deck.ProtectionRacket()
    player_1 = greed.ConsoleTableau('Test Player 1')
    player_2 = greed.ConsoleTableau('Test Player 2')
    game = greed.Game((player_1, player_2))
    card = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    pr.when_played(game, player_1)
    assert player_1.cash == 0
    player_1.holdings.append(card)
    player_2.holdings.append(card)
    pr.when_played(game, player_1)
    assert player_1.cash == 0
    player_1.holdings.append(card)
    pr.when_played(game, player_1)
    assert player_1.cash == 10000

@patch('builtins.input', return_value='0')
def test_insurancescam_when_played(mock_input):
    iscam = greed.deck.InsuranceScam()
    player_1 = greed.ConsoleTableau('Test Player 1')
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    card_1.markers = 3
    player_1.holdings.append(card_1)
    player_2 = greed.ConsoleTableau('Test Player 2')
    card_2 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    player_2.holdings.append(card_2)
    game = greed.Game((player_1, player_2))
    iscam.when_played(game, player_1)
    assert player_1.cash == 15000
    game.current_round += 1
    game.end_round()
    assert len(player_1.holdings) == 0
    assert len(player_2.holdings) == 0

@patch('builtins.input', return_value='0')
def test_suicide_mission_when_played(mock_input):
    sm = greed.deck.SuicideMission()
    player_1 = greed.ConsoleTableau('Test Player 1')
    card = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1')
    player_1.thugs.append(card)
    game = greed.Game((player_1,))
    sm.when_played(game, player_1)
    assert len(player_1.thugs) == 0
    assert player_1.cash == 25000

@patch('builtins.input', return_value='0')
def test_vandalism_when_played(mock_input):
    v = greed.deck.Vandalism()
    player_1 = greed.ConsoleTableau('Test Player 1')
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    player_1.holdings.append(card_1)
    player_2 = greed.ConsoleTableau('Test Player 2')
    card_2 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    player_2.holdings.append(card_2)
    game = greed.Game((player_1, player_2))
    v.when_played(game, player_1)
    game.current_round += 1
    game.end_round()
    assert len(player_1.holdings) == 1
    assert len(player_2.holdings) == 0

@patch('builtins.input', return_value='0')
def test_onelastheist_when_played(mock_input):
    olh = greed.deck.OneLastHeist()
    player_1 = greed.ConsoleTableau('Test Player 1')
    card_1 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1')
    player_1.thugs.append(card_1)
    player_1.thugs.append(card_1)
    player_2 = greed.ConsoleTableau('Test Player 2')
    card_2 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1')
    player_2.thugs.append(card_2)
    game = greed.Game((player_1, player_2))
    olh.when_played(game, player_1)
    assert player_1.cash == 10000
    game.current_round += 1
    game.end_round()
    assert len(player_1.holdings) == 0
    assert len(player_2.holdings) == 0

@patch('builtins.input', return_value='0')
def test_stealideas_when_played(mock_input):
    si = greed.deck.StealIdeas()
    player_1 = greed.ConsoleTableau('Test Player 1')
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    player_1.holdings.append(card_1)
    player_2 = greed.ConsoleTableau('Test Player 2')
    card_2 = greed.Card(greed.card.CardType.HOLDING, 2, 'Test Card 2')
    card_2.markers = 3
    player_2.holdings.append(card_2)
    card_3 = greed.Card(greed.card.CardType.HOLDING, 3, 'Test Card 3')
    card_3.markers = 3
    player_2.holdings.append(card_3)
    game = greed.Game((player_1, player_2))
    si.when_played(game, player_1)
    assert card_1.markers == 0
    card_3.markers = 5
    si.when_played(game, player_1)
    assert card_1.markers == 5

def test_insidertrading_when_played():
    it = greed.deck.InsiderTrading()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    it.when_played(game, player_1)
    assert player_1.cash == 45000

def test_pickpocketnetwork_when_played():
    pn = greed.deck.PickpocketNetwork()
    player_1 = greed.ConsoleTableau('Test Player 1')
    card_1 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1', icons=greed.deck.Icons(keys=3))
    player_1.thugs.append(card_1)
    card_2 = greed.Card(greed.card.CardType.HOLDING, 2, 'Test Card 2', icons=greed.deck.Icons(wrenches=3))
    player_1.holdings.append(card_2)
    game = greed.Game((player_1,))
    pn.when_played(game, player_1)
    assert player_1.cash == 60000

@patch('builtins.input', return_value='0')
def test_liquidate_when_played(mock_input):
    l = greed.deck.Liquidate()
    player_1 = greed.ConsoleTableau('Test Player 1')
    card = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    card.markers = 5
    player_1.holdings.append(card)
    game = greed.Game((player_1,))
    player_1.play_card(game, l)
    assert player_1.cash == 75000
    assert len(player_1.holdings) == 0

@patch('builtins.input', return_value='0')
def test_renovate_when_played(mock_input):
    r = greed.deck.Renovate()
    player_1 = greed.ConsoleTableau('Test Player 1')
    card = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    player_1.holdings.append(card)
    game = greed.Game((player_1,))
    r.when_played(game, player_1)
    assert card.markers == 2

def test_scouting_when_played():
    s = greed.deck.Scouting()
    player_1 = greed.ConsoleTableau('Test Player 1')
    player_2 = greed.ConsoleTableau('Test Player 2')
    player_2.cash = 20000
    game = greed.Game((player_1, player_2))
    card_1 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1', icons=greed.card.Icons(cars=1))
    player_1.thugs.append(card_1)
    s.when_played(game, player_1)
    assert player_1.cash == 10000
    card_2 = greed.Card(greed.card.CardType.THUG, 2, 'Test Card 2', icons=greed.card.Icons(guns=1))
    player_1.thugs.append(card_2)
    s.when_played(game, player_1)
    assert player_1.cash == 20000
    assert player_2.cash == 10000
    card_3 = greed.Card(greed.card.CardType.THUG, 3, 'Test Card 3', icons=greed.card.Icons(keys=1))
    player_1.thugs.append(card_3)
    s.when_played(game, player_1)
    assert player_1.cash == 30000
    assert player_2.cash == 0
    assert len(player_1.hand) == 1

def test_smuggling_when_played():
    s = greed.deck.Smuggling()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    s.when_played(game, player_1)
    assert player_1.cash == 25000

def test_estateheist_when_played():
    eh = greed.deck.EstateHeist()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    card_1 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1', icons=greed.card.Icons(guns=1))
    player_1.thugs.append(card_1)
    eh.when_played(game, player_1)
    assert player_1.cash == 10000
    card_2 = greed.Card(greed.card.CardType.THUG, 2, 'Test Card 2', icons=greed.card.Icons(cars=1))
    player_1.thugs.append(card_2)
    eh.when_played(game, player_1)
    assert player_1.cash == 30000
    card_3 = greed.Card(greed.card.CardType.THUG, 3, 'Test Card 3', icons=greed.card.Icons(keys=1))
    player_1.thugs.append(card_3)
    eh.when_played(game, player_1)
    assert player_1.cash == 60000

def test_discard_holding_succeeds_with_no_holdings():
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    player_1.discard_holding(game)

def test_discard_thug_succeeds_with_no_thugs():
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    player_1.discard_thug(game)

@patch('builtins.input', return_value='0')
def test_takecareofbusiness_when_played(mock_input):
    tcob = greed.deck.TakeCareOfBusiness()
    player_1 = greed.ConsoleTableau('Test Player 1')
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    card_1.markers = 3
    card_2 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    card_2.markers = 1
    player_1.holdings.append(card_2)
    player_2 = greed.ConsoleTableau('Test Player 2')
    card_3 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1')
    player_2.thugs.append(card_3)
    game = greed.Game((player_1, player_2))
    tcob.when_played(game, player_1)
    assert card_1.markers == 3
    assert card_2.markers == 2
    game.current_round += 1
    game.end_round()
    assert len(player_2.thugs) == 0

@patch('builtins.input', return_value='0')
def test_gambit_when_played(mock_input):
    g = greed.deck.Gambit()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    g.when_played(game, player_1)
    assert player_1.cash == 30000

def test_suckerconvention_when_played():
    sc = greed.deck.SuckerConvention()
    player_1 = greed.ConsoleTableau('Test Player 1')
    player_2 = greed.ConsoleTableau('Test Player 2')
    game = greed.Game((player_1, player_2))
    sc.when_played(game, player_1)
    assert player_1.cash == 30000
    assert player_2.cash == 10000

def test_circusofcrime_when_played():
    coc = greed.deck.CircusOfCrime()
    player_1 = greed.ConsoleTableau('Test Player 1')
    card_1 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1')
    card_2 = greed.Card(greed.card.CardType.THUG, 2, 'Test Card 2')
    card_3 = greed.Card(greed.card.CardType.THUG, 3, 'Test Card 3')
    player_1.thugs.append(card_1)
    player_1.thugs.append(card_2)
    player_1.thugs.append(card_3)
    game = greed.Game((player_1,))
    coc.when_played(game, player_1)
    assert player_1.cash == 30000

def test_complexscheme_when_played():
    cs = greed.deck.ComplexScheme()
    player_1 = greed.ConsoleTableau('Test Player 1')
    game = greed.Game((player_1,))
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    cs.when_played(game, player_1)
    game.current_round += 1
    player_1.play_holding(game, card_1)
    assert card_1.markers == 3

def test_beggarsbanquet_when_played():
    bb = greed.deck.BeggarsBanquet()
    player_1 = greed.ConsoleTableau('Test Player 1')
    player_2 = greed.ConsoleTableau('Test Player 2')
    game = greed.Game((player_1, player_2))
    bb.when_played(game, player_1)
    assert player_1.cash == 0
    card_1 = greed.Card(greed.card.CardType.THUG, 1, 'Test Card 1')
    player_2.thugs.append(card_1)
    bb.when_played(game, player_1)
    assert player_1.cash == 25000

def test_inform_when_played():
    i = greed.deck.Inform()
    player_1 = greed.ConsoleTableau('Test Player 1')
    player_2 = greed.ConsoleTableau('Test Player 2')
    player_3 = greed.ConsoleTableau('Test Player 3')
    player_4 = greed.ConsoleTableau('Test Player 4')
    game = greed.Game((player_1, player_2, player_3, player_4))
    i.when_played(game, player_1)
    assert player_1.cash == 10000
    card_1 = greed.Card(greed.card.CardType.ACTION, 1, 'Test Card 1')
    player_2.play_action(game, card_1)
    assert player_1.cash == 20000
    player_3.play_action(game, card_1)
    assert player_1.cash == 20000
    player_4.play_action(game, card_1)
    assert player_1.cash == 30000

def test_honestwork_when_played():
    hw = greed.deck.HonestWork()
    player_1 = greed.ConsoleTableau('Test Player 1')
    player_1.cash = 20000
    game = greed.Game((player_1,))
    hw.when_played(game, player_1)
    assert player_1.cash == 35000
    game.discard_card(player_1, hw)
    assert len(player_1.hand) == 1
    hw.when_played(game, player_1)
    assert player_1.cash == 50000

@patch('builtins.input', return_value='0')
def test_seance_when_played(mock_input):
    s = greed.deck.Seance()
    player_1 = greed.ConsoleTableau('Test Player 1')
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    player_1.holdings.append(card_1)
    card_2 = greed.Card(greed.card.CardType.THUG, 2, 'Test Card 2')
    player_1.hand.append(card_2)
    game = greed.Game((player_1,))
    s.when_played(game, player_1)
    assert player_1.cash == 10000
    assert card_1.markers == 1
    assert len(player_1.thugs) == 1

@patch('builtins.input', return_value='0')
def test_relocate_when_played(mock_input):
    r = greed.deck.Relocate()
    player_1 = greed.ConsoleTableau('Test Player 1')
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    card_1.markers = 3
    player_1.holdings.append(card_1)
    game = greed.Game((player_1,))
    r.costs_paid.append(card_1)
    r.when_played(game, player_1)
    assert player_1.hand[0] == card_1
    game.current_round += 1
    player_1.play_holding(game, card_1)
    assert card_1.markers == 5

@patch('builtins.input', return_value='0')
def test_tableau_pay_cost_records_cost_paid(mock_input):
    player_1 = greed.ConsoleTableau('Test Player 1')
    card_1 = greed.Card(greed.card.CardType.HOLDING, 1, 'Test Card 1')
    player_1.holdings.append(card_1)
    card_2 = greed.Card(greed.card.CardType.HOLDING, 2, 'Test Card 1', costs=[greed.card.Cost(holdings=1)])
    game = greed.Game((player_1,))
    player_1.pay_cost(game, card_2)
    assert len(player_1.holdings) == 0
    assert len(card_2.costs_paid) == 1
    assert card_2.costs_paid[0] == card_1

