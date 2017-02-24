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
        'Gain $20000. At the end of the game lose $25000',
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
        'Gain $10000 for each {Alcohol} you have.',
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

    return thugs
