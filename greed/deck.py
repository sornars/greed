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
        def gain_equal_money(tableau, property_name, value):
            if (game.round == current_round and
                    property_name == 'cash' and
                    tableau.cash < value):
                current_player.tableau.cash += value - tableau.cash

        left_player.tableau.notify_players.append(gain_equal_money)

    thugs.append(Card(
        CardType.THUG,
        'Harvey "Brains" Ratcliffe',
        1,
        'This turn, when the player to your left gains $, you also gain that much $.',
        icons=Icons(guns=1),
        passive=gain_money_equal_to_opponent_on_left
    ))

    def gain_10000_if_0_cash_each_turn(game):
        if game.current_player.tableau.cash == 0:
            game.current_player.tableau.cash += 10000

    thugs.append(Card(
        CardType.THUG,
        '"Biscuits" O\'Malley',
        6,
        'Each turn: If you have no $, gain $10,000.',
        icons=Icons(cars=1),
        each_turn=gain_10000_if_0_cash_each_turn
    ))

    thugs.append(Card(
        CardType.THUG,
        '"King" Richard the Third',
        21,
        icons=Icons(guns=1, cars=1, keys=1)
    ))

    def gain_10000_when_played(game):
        game.current_player.tableau.cash += 10000

    thugs.append(Card(
        CardType.THUG,
        'Dickie "Flush" Diamond',
        22,
        icons=Icons(guns=1),
        when_played=gain_10000_when_played
    ))

    def gain_5000_per_gun_when_played(game):
        game.current_player.tableau.cash += (
            5000 * game.current_player.tableau.calculate_icons().guns
        )

    thugs.append(Card(
        CardType.THUG,
        'Ed "Cheesecloth" McGinty',
        23,
        icons=Icons(guns=1, keys=1),
        when_played=gain_5000_per_gun_when_played
    ))

    def gain_20000_when_played(game):
        game.current_player.tableau.cash += 20000

    def lose_25000_end_of_game(game):
        game.current_player.tableau.cash -= 25000

    thugs.append(Card(
        CardType.THUG,
        '"Generous" Jenny Jones',
        24,
        'Gain $20000. At the end of the game lose $25000',
        when_played=gain_20000_when_played,
        end_of_game=lose_25000_end_of_game,
        icons=Icons(guns=1)
    ))

    def gain_10000_for_each_alcohol_when_played(game):
        game.current_player.tableau.cash += (
            10000 * game.current_player.tableau.calculate_icons().alcohol
        )

    thugs.append(Card(
        CardType.THUG,
        'Mickey Istari',
        25,
        'Gain $10000 for each {Alcohol} you have.',
        when_played=gain_10000_for_each_alcohol_when_played,
        icons=Icons(cars=1)
    ))

    def place_an_extra_marker_on_holding(game):
        current_player = game.current_player
        def place_extra_marker(tableau, property_name, value):
            if property_name == 'holdings':
                value[-1].markers += 0.5 # TODO: 0.5 markers as assignment to holdings happens twice in Tableau.start_round

        current_player.tableau.notify_players.append(place_extra_marker)


    thugs.append(Card(
        CardType.THUG,
        'Wolfgang Buttercup',
        42,
        'When you play a HOLDING, place an extra counter on it.',
        passive=place_an_extra_marker_on_holding,
        needs=Icons(thugs=2),
        icons=Icons(cars=2)
    ))

    return thugs