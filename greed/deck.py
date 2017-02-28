import random

from .card import Card, CardType, Cost, Icons

def create_draw_deck():
    # TODO: Implement actual list of cards
    return [Card(random.choice(list(CardType)), i, 'Test Card {0}'.format(i)) for i in range(80)]

class HarveyBrainsRatcliffe(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=1,
            name='Harvey "Brains" Ratcliffe',
            rules_text='This turn, when the player to your left gains $,'
                       ' you also gain that much $.',
            icons=Icons(keys=1)
        )

    def when_played(self, game, tableau):
        current_round = game.current_round
        left_player = game.players[game.players.index(tableau) - 1]

        def orig_cash_setter(orig, value):
            pass

        if 'cash' in left_player.patched_setters:
            orig_cash_setter = left_player.patched_setters['cash']

        def patched_cash_setter(orig, value):
            delta = value - orig
            if game.current_round == current_round and delta > 0:
                tableau.cash += delta
            orig_cash_setter(orig, value)

        left_player.patched_setters['cash'] = patched_cash_setter

class BiscuitsOMalley(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=6,
            name='"Biscuits" O\'Malley',
            rules_text='Each Turn: If you have no $, gain $10,000.',
            icons=Icons(cars=1)
        )

    def each_turn(self, game, tableau):
        if tableau.cash == 0:
            tableau.cash += 10000

class KingRichardTheThird(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=21,
            name='"King" Richard the Third',
            costs=[Cost(thugs=1), Cost(holdings=1), Cost(cash=10000)],
            icons=Icons(guns=1, cars=1, keys=1)
        )




