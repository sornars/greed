import random
import types

from .card import Card, CardType, Cost, Icons
from .tableau import Tableau

def create_draw_deck():
    # TODO: Implement actual list of cards
    draw_deck = [Card(random.choice(list(CardType)), i, 'Test Card {0}'.format(i)) for i in range(55)] + generate_thugs()
    random.shuffle(draw_deck)
    return draw_deck

def generate_thugs():
    return [
        HarveyBrainsRatcliffe(),
        BiscuitsOMalley(),
        KingRichardTheThird(),
        DickieFlushDiamond(),
        EdCheeseclothMcGuinty(),
        GenerousJennieJones(),
        MickeyIstari(),
        WolfgangButtercup(),
        PolycephalusPatriciaJones(),
        EdRubberfaceTeach(),
        PeepingTomThumb(),
        FriendlyGusCaspar(),
        HalloweenJackParis(),
        ViciousSydVarney(),
        RottenJohnnySimmons(),
        RandomScrubPatterson(),
        StingyStanMcDowell(),
        LouieSavoirOFarrell(),
        PeteRepeatFell(),
        NataschaTheSquirrelRubin(),
        NothingbeatsRockBenson(),
        EugeneTheButcherMidge(),
        TedNapoleonBonham(),
        BobbyCourduroyBrown(),
        JackCrackerThompson()
    ]

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

class RandomScrubPatterson(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=65,
            name='"Random" Scrub Patterson',
            rules_text='Draw a card from the deck for each KEY you have,'
                       ' putting them in your hand.',
            icons=Icons(keys=1)
        )

    def when_played(self, game, tableau):
        keys = tableau.calculate_icons().keys + self.icons.keys
        for card in range(keys):
            drawn_card = game.draw_deck.pop()
            tableau.hand.append(drawn_card)

class StingyStanMcDowell(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=66,
            name='"Stingy" Stan McDowell',
            rules_text='All COSTS for you are reduced by $5,000.',
            icons=Icons(cars=1)
        )

    def when_played(self, game, tableau):
        orig_pay_cost = tableau.pay_cost
        def reduce_costs_by_5000(tableau, game, costs):
            reduced_costs = [Cost(cost.cash, cost.thugs, cost.holdings) for cost in costs]
            for cost in reduced_costs:
                if cost.cash >= 5000:
                    cost.cash -= 5000
            return orig_pay_cost(game, reduced_costs)

        tableau.pay_cost = types.MethodType(reduce_costs_by_5000, tableau)

    def on_discard(self, game, tableau):
        orig_pay_cost = tableau.pay_cost
        def disable_reduce_costs_by_5000(tableau, game, costs):
            increased_costs = [Cost(cost.cash, cost.thugs, cost.holdings) for cost in costs]
            for cost in increased_costs:
                if cost.cash >= 5000:
                    cost.cash += 5000
            return orig_pay_cost(game, increased_costs)

        tableau.pay_cost = types.MethodType(disable_reduce_costs_by_5000, tableau)

class LouieSavoirOFarrell(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=67,
            name='Louie "Savoir" O\'Farrell',
            rules_text='Next turn, after all played cards resolve, play n extra card.',
            icons=Icons(cars=1, keys=1)
        )

    def when_played(self, game, tableau):
        orig_end_round = game.end_round
        next_round = game.current_round + 1
        def play_extra_card_next_turn(game):
            if game.current_round == next_round:
                tableau.play_card(game, tableau.select_option(tableau.hand))
            return orig_end_round()

        game.end_round = types.MethodType(play_extra_card_next_turn, game)

class PeteRepeatFell(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=68,
            name='Pete "Repeat" Fell',
            rules_text='Next turn, when you play an ACTION, return it to your hand afterwards.',
            icons=Icons(keys=1)
        )

    def when_played(self, game, tableau):
        orig_discard_card = game.discard_card
        next_round = game.current_round + 1
        current_player = tableau
        def return_action_to_hand_next_turn(game, tableau, card):
            orig_discard_card_results = orig_discard_card(tableau, card)
            if (game.current_round == next_round and
                    tableau == current_player and
                    card.card_type is CardType.ACTION):
                tableau.hand.append(game.discard_deck.pop())
            return orig_discard_card_results

        game.discard_card = types.MethodType(return_action_to_hand_next_turn, game)

class NataschaTheSquirrelRubin(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=69,
            name='Natascha "The Squirrel" Rubin',
            rules_text='Each Turn: Gain $5,000.',
            needs=Icons(holdings=2)
        )

    def each_turn(self, game, tableau):
        tableau.cash += 5000

class NothingbeatsRockBenson(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=70,
            name='"Nothing beats" Rock Benson',
            rules_text='When you play an ACTION, gain $5,000 afterwards.',
            icons=Icons(guns=1)
        )

    def when_played(self, game, tableau):
        orig_play_card = tableau.play_card
        def gain_5000_when_action_played(tableau, game, card, ignore_costs=False, ignore_needs=False):
            card_played = orig_play_card(game, card, ignore_costs=False, ignore_needs=False)
            if card.card_type is CardType.ACTION and card_played:
                tableau.cash += 5000
            return card_played

        tableau.play_card = types.MethodType(gain_5000_when_action_played, tableau)

    def on_discard(self, game, tableau):
        orig_play_card = tableau.play_card
        def disable_gain_5000_when_action_played(tableau, game, card, ignore_costs=False, ignore_needs=False):
            card_played = orig_play_card(game, card, ignore_costs=False, ignore_needs=False)
            if card.card_type is CardType.ACTION and card_played:
                tableau.cash -= 5000
            return card_played

        tableau.play_card = types.MethodType(disable_gain_5000_when_action_played, tableau)

class EugeneTheButcherMidge(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=71,
            name='Eugene "The Butcher" Midge',
            rules_text='When you play an ACTION, gain $5,000 per GUN you have afterwards.',
            costs=[Cost(thugs=1)],
            icons=Icons(guns=1, cars=1)
        )

    def when_played(self, game, tableau):
        orig_play_card = tableau.play_card
        def gain_5000_per_gun_when_action_played(tableau, game, card, ignore_costs=False, ignore_needs=False):
            card_played = orig_play_card(game, card, ignore_costs=False, ignore_needs=False)
            if card.card_type is CardType.ACTION and card_played:
                tableau.cash += 5000 * tableau.calculate_icons().guns
            return card_played

        tableau.play_card = types.MethodType(gain_5000_per_gun_when_action_played, tableau)

    def on_discard(self, game, tableau):
        orig_play_card = tableau.play_card
        def disable_gain_5000_per_gun_when_action_played(tableau, game, card, ignore_costs=False, ignore_needs=False):
            card_played = orig_play_card(game, card, ignore_costs=False, ignore_needs=False)
            if card.card_type is CardType.ACTION and card_played:
                tableau.cash -= 5000 * tableau.calculate_icons().guns
            return card_played

        tableau.play_card = types.MethodType(disable_gain_5000_per_gun_when_action_played, tableau)

class TedNapoleonBonham(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=72,
            name='Ted "Napoleon" Bonham',
            rules_text='Next turn only, this THUG also has GUN and KEY.',
            icons=Icons(cars=1)
        )

    def when_played(self, game, tableau):
        orig_start_round = game.start_round
        current_round = game.current_round
        def gain_gun_and_key_icons_next_turn(game):
            # Round incremented in start_round
            if game.current_round == current_round:
                self.icons = Icons(guns=1, cars=1, keys=1)
            else:
                self.icons = Icons(cars=1)
            return orig_start_round()

        game.start_round = types.MethodType(gain_gun_and_key_icons_next_turn, game)

class BobbyCourduroyBrown(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=76,
            name='Bobby "Courduroy" Brown',
            rules_text='Each opponent lose $10,000.',
            icons=Icons(guns=1)
        )

    def when_played(self, game, tableau):
        for player in game.players:
            if player != tableau:
                new_value = player.cash - 10000
                if new_value > 0:
                    player.cash = new_value
                else:
                    player.cash = 0

class JackCrackerThompson(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=76,
            name='Jack "Cracker" Thompson',
            rules_text='Each other player loses $5,000 for each HOLDING that player has.',
            icons=Icons(keys=1)
        )

    def when_played(self, game, tableau):
        for player in game.players:
            if player != tableau:
                new_value = player.cash - (5000 * len(player.holdings))
                if new_value > 0:
                    player.cash = new_value
                else:
                    player.cash = 0

class DollsOnCall(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=10,
            name='Dolls On Call',
            rules_text='Each Turn: If one player has the most HOLDINGS, that player gain $5,000.',
            costs=[Cost(cash=15000)],
            icons=Icons(hearts=1)
        )

    def each_turn(self, game, tableau):
        max_holdings_count = max([len(player.holdings) for player in game.players])
        max_holdings = [player for player in game.players if len(player.holdings) == max_holdings_count]
        if len(max_holdings) == 1:
            max_holdings[0].cash += 5000

class TommysCashNAmmo(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=58,
            name='Tommy\'s Cash \'N\' Ammo',
            rules_text='Each opponent removes a marker from each of their HOLDINGS.',
            costs=[Cost(holdings=1)],
            icons=Icons(wrenches=1)
        )

    def when_played(self, game, tableau):
        for player in game.players:
            if player != tableau:
                for holding in player.holdings:
                    if holding.markers >= 1:
                        holding.markers -= 1

class Hideout(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=55,
            name='Hideout',
            rules_text='Do all of the rules of all of your THUGS played in previous turns.',
        )

    def when_played(self, game, tableau):
        for thug in tableau.thugs:
            thug.when_played(game, tableau)

class TrotskysBurlesque(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=19,
            name='Trotsky\'s Burlesque',
            rules_text='Each Turn: If one player has the most HEARTS, that player gains $5,000.',
            costs=[Cost(cash=15000)],
            icons=Icons(hearts=1)
        )

    def each_turn(self, game, tableau):
        max_hearts_count = max([player.calculate_icons().hearts for player in game.players])
        max_hearts = [player for player in game.players if player.calculate_icons().hearts == max_hearts_count]
        if len(max_hearts) == 1:
            max_hearts[0].cash += 5000

class JoesGinJoint(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=11,
            name='Joe\'s Gin Joint',
            rules_text='Place 2 extra markers on this.',
            costs=[Cost(cash=15000)],
            icons=Icons(alcohol=1)
        )

    def when_played(self, game, tableau):
        self.markers += 2

class TheRitz(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=18,
            name='The Ritz',
            rules_text='Place 5 extra markers on this.',
            costs=[Cost(cash=30000)],
            icons=Icons(alcohol=1)
        )

    def when_played(self, game, tableau):
        self.markers += 5