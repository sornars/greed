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
            needs=Icons(thugs=2),
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

class PolycephalusPatriciaJones(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=53,
            name='"Polycephalus" Patricia Jones',
            rules_text='Turn over cards from the deck until you find a THUG. '
                       'Play it, ignoring COSTS and NEEDS. '
                       'Discard all other cards that you revealed from the deck.',
            icons=Icons(cars=2)
        )

    def when_played(self, game, tableau):
        drawn_card = game.draw_deck.pop()
        while drawn_card.card_type is not CardType.THUG:
            game.discard_deck.append(drawn_card)
            drawn_card = game.draw_deck.pop()

        tableau.play_card(game, drawn_card, ignore_costs=True, ignore_needs=True)

class EdRubberfaceTeach(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=54,
            name='Ed "Rubberface" Teach',
            rules_text='This THUG becomes a copy of one of your other THUGS; do its rules.',
            needs=Icons(thugs=1)
        )

    def when_played(self, game, tableau):
        # pylint: disable=E0202
        selected_thug = tableau.select_option(tableau.thugs)
        tableau.thugs.append(selected_thug)
        copied_card = type(selected_thug)()
        self.rules_text = copied_card.rules_text
        self.icons = copied_card.icons
        self.when_played = copied_card.when_played
        self.each_turn = copied_card.each_turn
        self.on_discard = copied_card.on_discard
        self.end_of_game = copied_card.end_of_game
        self.when_played(game, tableau)

class PeepingTomThumb(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=56,
            name='"Peeping" Tom "Thumb"',
            rules_text='Gain $5,000 for each counter the HOLDING with the most has.',
            costs=[Cost(holdings=1)],
            icons=Icons(guns=2)
        )

    def when_played(self, game, tableau):
        most_markers = 0
        for player in game.players:
            for holding in player.holdings:
                if holding.markers > most_markers:
                    most_markers = holding.markers
        tableau.cash += 5000 * most_markers

class FriendlyGusCaspar(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=61,
            name='"Friendly" Gus Caspar',
            rules_text='When you play another THUG, gain $15,000.',
            needs=Icons(guns=1, cars=1),
            icons=Icons(keys=2)
        )

    def when_played(self, game, tableau):
        orig_play_card = tableau.play_card
        def gain_15000_when_thug_played(tableau, game, card, ignore_costs=False, ignore_needs=False):
            card_played = orig_play_card(game, card, ignore_costs=False, ignore_needs=False)
            if card.card_type is CardType.THUG and card_played:
                tableau.cash += 15000
            return card_played

        tableau.play_card = types.MethodType(gain_15000_when_thug_played, tableau)

    def on_discard(self, game, tableau):
        orig_play_card = tableau.play_card
        def disable_gain_15000_when_thug_played(tableau, game, card, ignore_costs=False, ignore_needs=False):
            card_played = orig_play_card(game, card, ignore_costs=False, ignore_needs=False)
            if card.card_type is CardType.THUG and card_played:
                tableau.cash -= 15000
            return card_played

        tableau.play_card = types.MethodType(disable_gain_15000_when_thug_played, tableau)

class HalloweenJackParis(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=62,
            name='"Halloween" Jack Paris',
            rules_text='When you lose this THUG, gain $20,000.',
            icons=Icons(keys=1)
        )

    def on_discard(self, game, tableau):
        tableau.cash += 20000

class ViciousSydVarney(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=63,
            name='"Vicious" Syd Varney',
            rules_text='Next turn, you ignore COSTS.',
            icons=Icons(guns=1)
        )

    def when_played(self, game, tableau):
        orig_play_card = tableau.play_card
        next_round = game.current_round + 1
        def ignore_costs_next_turn(tableau, game, card, ignore_costs=False, ignore_needs=False):
            ignore_costs = ignore_costs
            if game.current_round == next_round:
                ignore_costs = True
            orig_play_card(game, card, ignore_costs, ignore_needs)

        tableau.play_card = types.MethodType(ignore_costs_next_turn, tableau)

class RottenJohnnySimmons(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=64,
            name='"Rotten" Johnny Simmons',
            rules_text='Next turn, you ignore NEEDS.',
            icons=Icons(cars=1)
        )

    def when_played(self, game, tableau):
        orig_play_card = tableau.play_card
        next_round = game.current_round + 1
        def ignore_needs_next_turn(tableau, game, card, ignore_costs=False, ignore_needs=False):
            ignore_needs = ignore_needs
            if game.current_round == next_round:
                ignore_needs = True
            orig_play_card(game, card, ignore_costs, ignore_needs)

        tableau.play_card = types.MethodType(ignore_needs_next_turn, tableau)