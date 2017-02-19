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

    def gain_10000_each_turn_with_no_cash(game):
        if game.current_player.tableau.cash == 0:
            game.current_player.tableau.cash += 10000

    thugs.append(Card(
        CardType.THUG,
        '"Biscuits" O\'Malley',
        6,
        'Each turn: If you have no $, gain $10,000.',
        icons=Icons(cars=1),
        each_turn=gain_10000_each_turn_with_no_cash
    ))

    return thugs