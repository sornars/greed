import copy
import types

from .card import Card, CardType, Cost, Icons

def generate_standard_deck():
    thugs = generate_thugs()

    return thugs

def generate_thugs():
    thugs = []

    def gain_money_equal_to_opponent_on_left(game):
        current_player = game.current_player
        current_player_index = game.players.index(current_player)
        current_round = game.round
        left_player = game.players[current_player_index - 1]

        def orig_cash_setter(tableau, value):
            return value

        if 'cash' in left_player.tableau.patched_setters:
            orig_cash_setter = left_player.tableau.patched_setters['cash']

        def patched_cash_setter(tableau, value):
            delta = value - tableau.cash
            if game.round == current_round and delta > 0:
                current_player.tableau.cash += delta
            return orig_cash_setter(tableau, value)

        left_player.tableau.patched_setters['cash'] = patched_cash_setter


    thugs.append(Card(
        CardType.THUG,
        'Harvey "Brains" Ratcliffe',
        1,
        'This turn, when the player to your left gains $, you also gain that much $.',
        icons=Icons(guns=1),
        when_played=gain_money_equal_to_opponent_on_left
    ))

    def gain_10000_if_0_cash(game):
        if game.current_player.tableau.cash == 0:
            game.current_player.tableau.cash += 10000

    thugs.append(Card(
        CardType.THUG,
        '"Biscuits" O\'Malley',
        6,
        'Each turn: If you have no $, gain $10,000.',
        icons=Icons(cars=1),
        each_turn=gain_10000_if_0_cash
    ))

    thugs.append(Card(
        CardType.THUG,
        '"King" Richard the Third',
        21,
        icons=Icons(guns=1, cars=1, keys=1)
    ))

    def gain_10000(game):
        game.current_player.tableau.cash += 10000

    thugs.append(Card(
        CardType.THUG,
        'Dickie "Flush" Diamond',
        22,
        icons=Icons(guns=1),
        when_played=gain_10000
    ))

    def gain_5000_per_gun(game):
        game.current_player.tableau.cash += (
            5000 * (game.current_player.tableau.calculate_icons().guns + 1)
        )

    thugs.append(Card(
        CardType.THUG,
        'Ed "Cheesecloth" McGinty',
        23,
        icons=Icons(guns=1, keys=1),
        when_played=gain_5000_per_gun
    ))

    def gain_20000(game):
        game.current_player.tableau.cash += 20000

    def lose_25000(game):
        game.current_player.tableau.cash -= 25000

    thugs.append(Card(
        CardType.THUG,
        '"Generous" Jenny Jones',
        24,
        'Gain $20,000. At the end of the game lose $25,000',
        when_played=gain_20000,
        end_of_game=lose_25000,
        icons=Icons(guns=1)
    ))

    def gain_10000_per_alcohol(game):
        game.current_player.tableau.cash += (
            10000 * game.current_player.tableau.calculate_icons().alcohol
        )

    thugs.append(Card(
        CardType.THUG,
        'Mickey Istari',
        25,
        'Gain $10,000 for each {Alcohol} you have.',
        when_played=gain_10000_per_alcohol,
        icons=Icons(cars=1)
    ))

    def place_an_extra_marker_on_holding(game):
        current_player = game.current_player
        orig_place_markers = current_player.tableau.place_markers

        def place_extra_marker(tableau, card):
            card.markers += 1
            return orig_place_markers(card)

        current_player.tableau.place_markers = types.MethodType(place_extra_marker, current_player.tableau)

    def disable_place_an_extra_marker_on_holding(game):
        current_player = game.current_player
        orig_place_markers = current_player.tableau.place_markers

        def disable_place_extra_marker(tableau, card):
            card.markers -= 1
            return orig_place_markers(card)

        current_player.tableau.place_markers = types.MethodType(disable_place_extra_marker, current_player.tableau)

    thugs.append(Card(
        CardType.THUG,
        'Wolfgang Buttercup',
        42,
        'When you play a HOLDING, place an extra counter on it.',
        when_played=place_an_extra_marker_on_holding,
        on_discard=disable_place_an_extra_marker_on_holding,
        needs=Icons(thugs=2),
        icons=Icons(cars=2)
    ))

    def reveal_a_new_thug(game):
        new_thug = game.draw_deck.pop()
        while new_thug.card_type is not CardType.THUG and game.draw_deck:
            game.discard_deck.append(new_thug)
            new_thug = game.draw_deck.pop()

        game.current_player.tableau.play_card(new_thug, ignore_costs=True, ignore_needs=True)

    thugs.append(Card(
        CardType.THUG,
        '"Polycephalus" Patricia Jones',
        53,
        'Turn over cards from the deck until you find a THUG. '
        'Play it, ignoring COSTS and NEEDS. '
        'Discard all other cards that you revealed from the deck.',
        when_played=reveal_a_new_thug
    ))

    def copy_a_thug(game):
        chosen_thug = game.current_player.tableau.select_thug()
        thug_copy = copy.deepcopy(chosen_thug)
        game.current_player.tableau.play_card(thug_copy, ignore_costs=True, ignore_needs=True)
        thug_copy.when_played(game)

    thugs.append(Card(
        CardType.THUG,
        'Ed "Rubberface" Teach',
        54,
        'This THUG becomes a copy of one of your other THUGS; do its rules.',
        needs=Icons(thugs=1),
        when_played=copy_a_thug
    ))

    def gain_5000_per_marker_on_holding_with_the_most(game):
        most_markers = 0
        for player in game.players:
            for holding in player.tableau.holdings:
                if holding.markers > most_markers:
                    most_markers = holding.markers

        game.current_player.tableau.cash += (5000 * most_markers)

    thugs.append(Card(
        CardType.THUG,
        '"Peeping" Tom "Thumb"',
        56,
        'Gain $5,000 for each counter the HOLDING with the most has.',
        costs=Cost(holdings=1),
        when_played=gain_5000_per_marker_on_holding_with_the_most
    ))

    def gain_15000_per_thug_played(game):
        current_player = game.current_player
        orig_play_card = current_player.tableau.play_card

        def gain_15000_per_thug(tableau, card, discarded_cards=None, ignore_costs=False, ignore_needs=False):
            discard_card = orig_play_card(card, discarded_cards=None, ignore_costs=False, ignore_needs=False)
            if card.card_type is CardType.THUG:
                tableau.cash += 15000
            return discard_card

        current_player.tableau.play_card = types.MethodType(gain_15000_per_thug, current_player.tableau)

    def disable_gain_15000_per_thug_played(game):
        current_player = game.current_player
        orig_play_card = current_player.tableau.play_card

        def disable_gain_15000_per_thug(tableau, card, discarded_cards=None, ignore_costs=False, ignore_needs=False):
            discard_card = orig_play_card(card, discarded_cards=None, ignore_costs=False, ignore_needs=False)
            if card.card_type is CardType.THUG:
                tableau.cash -= 15000
            return discard_card

        current_player.tableau.play_card = types.MethodType(disable_gain_15000_per_thug, current_player.tableau)


    thugs.append(Card(
        CardType.THUG,
        '"Friendly" Gus Caspar',
        61,
        'When you play another THUG, gain $15,000.',
        needs=Icons(thugs=2),
        icons=Icons(keys=2),
        when_played=gain_15000_per_thug_played,
        on_discard=disable_gain_15000_per_thug_played
    ))

    def gain_20000_when_lost(game):
        game.current_player.tableau.cash += 20000

    thugs.append(Card(
        CardType.THUG,
        '"Halloween" Jack Paris',
        62,
        'When you lose this THUG, gain $20,000.',
        icons=Icons(keys=1),
        on_discard=gain_20000_when_lost
    ))

    return thugs
