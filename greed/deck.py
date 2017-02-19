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

    thug_1 = Card(
        CardType.THUG,
        'Harvey "Brains" Ratcliffe',
        1,
        'This turn, when the player to your left gains $, you also gain that much $',
        this_turn=gain_money_equal_to_opponent_on_left)

    return [thug_1]