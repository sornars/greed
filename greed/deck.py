import random
import types

from .card import Card, CardType, Cost, Icons
from .tableau import Tableau

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

class DickieFlushDiamond(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=22,
            name='Dickie "Flush" Diamond',
            rules_text='Gain $10,000.',
            icons=Icons(guns=1)
        )

    def when_played(self, game, tableau):
        tableau.cash += 10000

class EdCheeseclothMcGuinty(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=23,
            name='Ed "CheeseCloth" McGuinty',
            rules_text='Gain $5,000 per GUN you have.',
            icons=Icons(guns=1, keys=1)
        )

    def when_played(self, game, tableau):
        guns = tableau.calculate_icons().guns + self.icons.guns
        tableau.cash += 5000 * guns

class GenerousJennieJones(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=24,
            name='"Generous" Jennie Jones',
            rules_text='Gain $20,000. At the end of the game lose $25,000.',
            icons=Icons(guns=1)
        )

    def when_played(self, game, tableau):
        tableau.cash += 20000

    def end_of_game(self, game, tableau):
        tableau.cash -= 25000

class MickeyIstari(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=25,
            name='Mickey Istari',
            rules_text='Gain $10,000 for each ALOCHOL you have.',
            icons=Icons(cars=1)
        )

    def when_played(self, game, tableau):
        alcohol = tableau.calculate_icons().alcohol
        tableau.cash += 10000 * alcohol

class WolfgangButtercup(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=42,
            name='Wolfgang Buttercup',
            rules_text='When you play a HOLDING, place an extra counter on it.',
            icons=Icons(cars=2)
        )

    def when_played(self, game, tableau):
        orig_place_markers = tableau.place_markers

        def place_extra_marker(tableau, card):
            card.markers += 1
            return orig_place_markers(card)

        tableau.place_markers = types.MethodType(place_extra_marker, tableau)

    def on_discard(self, game, tableau):
        orig_place_markers = tableau.place_markers

        def disable_place_extra_marker(tableau, card):
            card.markers -= 1
            return orig_place_markers(card)

        tableau.place_markers = types.MethodType(disable_place_extra_marker, tableau)