from .card import Card, CardType, Cost, Icons

class Deck:
    def __init__(self, cards=None):
        self.cards = [] if cards is None else cards

    def __repr__(self):
        return str(len(self.cards))

def generate_standard_deck():
    thugs = generate_thugs()

    return thugs

def generate_thugs():
    thugs = []
    def gain_money_equal_to_opponent_on_left(game):
        current_player = game.current_player
        current_player_index = game.players.index(current_player)
        current_round = game.round
        left_player = game.players[current_player_index % len(game.players) - 1]
        def gain_money_this_round(tableau, property_name, value):
            if (property_name == 'cash' and
                    game.round == current_round and
                    tableau.cash < value):
                current_player.tableau.cash += value - tableau.cash

        left_player.tableau.notify_players.append(gain_money_this_round)

    thugs.append(Card(
        CardType.THUG,
        'Harvey "Brains" Ratcliffe',
        1,
        'This turn, when the player to your left gains $, you also gain that much $.',
        icons=Icons(guns=1),
        this_turn=gain_money_equal_to_opponent_on_left
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

    return thugs