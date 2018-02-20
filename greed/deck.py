import random
import types

from .card import Card, CardType, Cost, Icons
from .tableau import ConsoleTableau

def create_draw_deck():
    draw_deck = generate_thugs() + generate_holdings() + generate_actions()
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

def generate_holdings():
    return [
        DollsOnCall(),
        TommysCashNAmmo(),
        Hideout(),
        TrotskysBurlesque(),
        JoesGinJoint(),
        TheRitz(),
        Junkyard(),
        ZoningOffice(),
        BookieJoint(),
        MassageParlor(),
        Headquarters(),
        PaddysPub(),
        MorticiasAbsintheParlor(),
        Chinatown(),
        SexySadies(),
        ThievesHouse(),
        Loanshark(),
        DaisysCookies(),
        PoorHouse(),
        JennysWaterfrontDive(),
        SandysSnookerNSchanpps(),
        KrazyKatClub(),
        SixCorners(),
        LamontesEscortService(),
        InsuranceOffice()
    ]

def generate_actions():
    return [
        Shakedown(),
        Arson(),
        Sting(),
        MuseumHeist(),
        StreetWalkers(),
        Raid(),
        MasterPlan(),
        ProtectionRacket(),
        InsuranceScam(),
        SuicideMission(),
        Vandalism(),
        OneLastHeist(),
        StealIdeas(),
        InsiderTrading(),
        PickpocketNetwork(),
        Liquidate(),
        Renovate(),
        Scouting(),
        Smuggling(),
        EstateHeist(),
        TakeCareOfBusiness(),
        Gambit(),
        SuckerConvention(),
        CircusOfCrime(),
        ComplexScheme(),
        BeggarsBanquet(),
        Inform(),
        HonestWork(),
        Seance(),
        Relocate()
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
        orig_set_cash = left_player._set_cash

        def gain_cash_equal_to_left_player(left_player, cash):
            if game.current_round == current_round and cash > left_player.cash:
                delta = cash - tableau.cash
                tableau.cash += delta
            orig_set_cash(cash)

        left_player._set_cash = types.MethodType(gain_cash_equal_to_left_player, left_player)


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
        orig_play_holding = tableau.play_holding
        def place_extra_marker(tableau, game, card):
            card.markers += 1
            orig_play_holding(game, card)

        tableau.play_holding = types.MethodType(place_extra_marker, tableau)

    def on_discard(self, game, tableau):
        orig_play_holding = tableau.play_holding
        def disable_place_extra_marker(tableau, game, card):
            orig_play_holding(game, card)
            card.markers -= 1

        tableau.play_holding = types.MethodType(disable_place_extra_marker, tableau)

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
            game.discard_card(tableau, drawn_card, on_discard=False)
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
        selected_thug, tableau.thugs = tableau.select_option(tableau.thugs, remove_option=False)
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
        orig_play_thug = tableau.play_thug
        def gain_15000_when_thug_played(tableau, game, card):
            tableau.cash += 15000
            return orig_play_thug(game, card)

        tableau.play_thug = types.MethodType(gain_15000_when_thug_played, tableau)

    def on_discard(self, game, tableau):
        orig_play_thug = tableau.play_thug
        def disable_gain_15000_when_thug_played(tableau, game, card):
            tableau.cash -= 15000
            return orig_play_thug(game, card)

        tableau.play_thug = types.MethodType(disable_gain_15000_when_thug_played, tableau)

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
        def reduce_costs_by_5000(tableau, game, card):
            reduced_costs = [Cost(cost.cash, cost.thugs, cost.holdings) for cost in card.costs]
            for cost in reduced_costs:
                if cost.cash >= 5000:
                    cost.cash -= 5000
            new_card = Card(card.card_type, card.priority, card.name, costs=reduced_costs)
            return orig_pay_cost(game, new_card)

        tableau.pay_cost = types.MethodType(reduce_costs_by_5000, tableau)

    def on_discard(self, game, tableau):
        orig_pay_cost = tableau.pay_cost
        def disable_reduce_costs_by_5000(tableau, game, card):
            increased_costs = [Cost(cost.cash, cost.thugs, cost.holdings) for cost in card.costs]
            for cost in increased_costs:
                if cost.cash >= 5000:
                    cost.cash += 5000
            new_card = Card(card.card_type, card.priority, card.name, costs=increased_costs)
            return orig_pay_cost(game, new_card)

        tableau.pay_cost = types.MethodType(disable_reduce_costs_by_5000, tableau)

class LouieSavoirOFarrell(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.THUG,
            priority=67,
            name='Louie "Savoir" O\'Farrell',
            rules_text='Next turn, after all played cards resolve, play an extra card.',
            icons=Icons(cars=1, keys=1)
        )

    def when_played(self, game, tableau):
        orig_end_round = game.end_round
        next_round = game.current_round + 1
        def play_extra_card_next_turn(game):
            if game.current_round == next_round:
                played_card, tableau.hand = tableau.select_option(tableau.hand)
                tableau.play_card(game, played_card)
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
        def return_action_to_hand_next_turn(game, tableau, card, on_discard=True):
            orig_discard_card_results = orig_discard_card(tableau, card, on_discard)
            if (game.current_round == next_round and
                    tableau == current_player and
                    card.card_type is CardType.ACTION):
                tableau.hand.append(card)
                game.discard_deck = [discarded_card for discarded_card in game.discard_deck
                                     if discarded_card != card]
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
        orig_play_action = tableau.play_action
        def gain_5000_when_action_played(tableau, game, card):
            tableau.cash += 5000
            return orig_play_action(game, card)

        tableau.play_action = types.MethodType(gain_5000_when_action_played, tableau)

    def on_discard(self, game, tableau):
        orig_play_action = tableau.play_action
        def disable_gain_5000_when_action_played(tableau, game, card):
            tableau.cash -= 5000
            return orig_play_action(game, card)

        tableau.play_action = types.MethodType(disable_gain_5000_when_action_played, tableau)

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
        orig_play_action = tableau.play_action
        def gain_5000_per_gun_when_action_played(tableau, game, card):
            tableau.cash += 5000 * tableau.calculate_icons().guns
            return orig_play_action(game, card)

        tableau.play_action = types.MethodType(gain_5000_per_gun_when_action_played, tableau)

    def on_discard(self, game, tableau):
        orig_play_action = tableau.play_action
        def disable_gain_5000_per_gun_when_action_played(tableau, game, card):
            tableau.cash -= 5000 * tableau.calculate_icons().guns
            return orig_play_action(game, card)

        tableau.play_action = types.MethodType(disable_gain_5000_per_gun_when_action_played, tableau)

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
                new_value = player.cash - (5000 * player.calculate_icons().holdings)
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
        max_holdings_count = max([player.calculate_icons().holdings for player in game.players])
        max_holdings = [player for player in game.players if player.calculate_icons().holdings == max_holdings_count]
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

class Junkyard(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=12,
            name='Junkyard',
            rules_text='This gets its normal markers at the end of the game '
                       'rather than when played.',
            costs=[Cost(cash=10000)],
            icons=Icons(wrenches=1)
        )

    def when_played(self, game, tableau):
        # Plus 1 to account for its own icon
        normal_markers = tableau.calculate_markers(self) + 1
        orig_place_markers = tableau.place_markers
        def remove_normal_markers(tableau, card):
            orig_place_markers(card)
            if card == self:
                card.markers -= normal_markers

        tableau.place_markers = types.MethodType(remove_normal_markers, tableau)

    def end_of_game(self, game, tableau):
        normal_markers = tableau.calculate_markers(self)
        self.markers += normal_markers

class ZoningOffice(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=52,
            name='Zoning Office',
            rules_text='When you play another HOLDING, gain $5,000.'
                       'HOLDINGS cost you $5,000 less.'
        )

    def when_played(self, game, tableau):
        orig_pay_cost = tableau.pay_cost
        def reduce_holding_costs_by_5000_and_gain_5000_per_holding(tableau, game, card):
            new_card = card
            if card.card_type is CardType.HOLDING:
                reduced_costs = [Cost(cost.cash, cost.thugs, cost.holdings) for cost in card.costs]
                for cost in reduced_costs:
                    if cost.cash >= 5000:
                        cost.cash -= 5000
                tableau.cash += 5000
                new_card = Card(card.card_type, card.priority, card.name, costs=reduced_costs)

            return orig_pay_cost(game, new_card)

        tableau.pay_cost = types.MethodType(reduce_holding_costs_by_5000_and_gain_5000_per_holding, tableau)

    def on_discard(self, game, tableau):
        orig_pay_cost = tableau.pay_cost
        def disable_reduce_holding_costs_by_5000_and_gain_5000_per_holding(tableau, game, card):
            new_card = card
            if card.card_type is CardType.HOLDING:
                increased_costs = [Cost(cost.cash, cost.thugs, cost.holdings) for cost in card.costs]
                for cost in increased_costs:
                    if cost.cash >= 5000:
                        cost.cash += 5000
                tableau.cash -= 5000
                new_card = Card(card.card_type, card.priority, card.name, costs=increased_costs)
            return orig_pay_cost(game, new_card)

        tableau.pay_cost = types.MethodType(disable_reduce_holding_costs_by_5000_and_gain_5000_per_holding, tableau)

class BookieJoint(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=7,
            name='Bookie Joint',
            rules_text='At the end of the game, gain an extra $5,000 for each marker on this.',
            costs=[Cost(cash=10000)],
            icons=Icons(wrenches=1)
        )

    def end_of_game(self, game, tableau):
        tableau.cash += 5000 * self.markers

class MassageParlor(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=48,
            name='Massage Parlor',
            needs=Icons(cars=2),
            icons=Icons(hearts=1, wrenches=1)
        )

class Headquarters(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=37,
            name='Headquarters',
            rules_text='Place a marker on this for each HOLDING you have.',
            needs=Icons(guns=1, keys=1)
        )

    def when_played(self, game, tableau):
        self.markers += tableau.calculate_icons().holdings + 1

class PaddysPub(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=15,
            name='Paddy\'s Pub',
            rules_text='Place an extra marker on this for each CAR you have.',
            needs=Icons(alcohol=1)
        )

    def when_played(self, game, tableau):
        self.markers += tableau.calculate_icons().cars

class MorticiasAbsintheParlor(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=14,
            name='Morticia\'s Absinthe Parlor',
            costs=[Cost(cash=10000)],
            icons=Icons(alcohol=1, hearts=1)
        )

class Chinatown(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=8,
            name='Chinatown',
            costs=[Cost(cash=10000)],
            icons=Icons(wrenches=1, alcohol=1)
        )

class SexySadies(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=49,
            name='Sexy Sadie\'s',
            rules_text='Each turn: If this HOLDING has at least 3 markers on it, gain $5,000.',
            needs=Icons(cars=1),
            icons=Icons(hearts=1)
        )

    def each_turn(self, game, tableau):
        if self.markers >= 3:
            tableau.cash += 5000

class ThievesHouse(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=51,
            name='Thieves\' House',
            needs=Icons(keys=2),
            icons=Icons(wrenches=1, alcohol=1)
        )

class Loanshark(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=44,
            name='Loanshark',
            rules_text='Gain $20,000. When you play a HOLDING, remove a marker from it.'
        )

    def when_played(self, game, tableau):
        tableau.cash += 20000
        orig_play_holding = tableau.play_holding
        def remove_marker(tableau, game, card):
            orig_play_holding(game, card)
            card.markers -= 1

        tableau.play_holding = types.MethodType(remove_marker, tableau)

    def on_discard(self, game, tableau):
        orig_play_holding = tableau.play_holding
        def disable_remove_marker(tableau, game, card):
            card.markers += 1
            orig_play_holding(game, card)

        tableau.play_holding = types.MethodType(disable_remove_marker, tableau)

class DaisysCookies(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=9,
            name='Daisy\'s Cookies',
            costs=[Cost(cash=10000)],
            icons=Icons(wrenches=1, hearts=1)
        )

class PoorHouse(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=16,
            name='Poor House',
            rules_text='Each turn: If you have at most 2 HOLDINGS and '
                       'at most 2 THUGS, gain $5,000.',
            costs=[Cost(cash=10000)],
            icons=Icons(wrenches=1)
        )

    def each_turn(self, game, tableau):
        if tableau.calculate_icons().holdings <= 2 and tableau.calculate_icons().thugs <= 2:
            tableau.cash += 5000

class JennysWaterfrontDive(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=46,
            name='Jenny\'s Waterfront Dive',
            rules_text='Each turn: If there are no ALCOHOL or HEART HOLDINGS in play, gain $10,000.'
        )

    def each_turn(self, game, tableau):
        active = True
        for player in game.players:
            icons = player.calculate_icons()
            if icons.alcohol > 0 or icons.hearts > 0:
                active = False

        if active:
            tableau.cash += 10000

class SandysSnookerNSchanpps(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=17,
            name='Sandy\'s Snooker \'N\' Schnapps',
            rules_text='When you plan an ACTION, place a marker on this afterwards.',
            costs=[Cost(cash=20000)],
            icons=Icons(alcohol=1)
        )

    def when_played(self, game, tableau):
        orig_play_action = tableau.play_action
        def gain_marker_when_action_played(tableau, game, card):
            self.markers += 1
            return orig_play_action(game, card)

        tableau.play_action = types.MethodType(gain_marker_when_action_played, tableau)

    def on_discard(self, game, tableau):
        orig_play_action = tableau.play_action
        def disable_gain_marker_when_action_played(tableau, game, card):
            self.markers -= 1
            return orig_play_action(game, card)

        tableau.play_action = types.MethodType(disable_gain_marker_when_action_played, tableau)

class KrazyKatClub(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=47,
            name='Krazy Kat Club',
            needs=[Icons(guns=2)],
            icons=Icons(alcohol=1, hearts=1)
        )

class SixCorners(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=50,
            name='Six Corners',
            rules_text='Place a marker on each of your HOLDINGS with no icons'
                       ' (ALCOHOL, HEART, WRENCH).',
        )

    def when_played(self, game, tableau):
        for holding in tableau.holdings:
            if holding.icons == Icons():
                holding.markers += 1
        self.markers += 1

class LamontesEscortService(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=13,
            name='Lamonte\'s Escort Service',
            rules_text='At the end of the game, '
                       'if you are the one player with the most THUGS, '
                       'gain $20,000.',
            costs=[Cost(cash=5000)],
            icons=Icons(hearts=1)
        )

    def end_of_game(self, game, tableau):
        max_thugs_count = max([player.calculate_icons().thugs for player in game.players])
        max_thugs = [player for player in game.players if player.calculate_icons().thugs == max_thugs_count]
        if len(max_thugs) == 1 and max_thugs[0] == tableau:
            tableau.cash += 20000

class InsuranceOffice(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.HOLDING,
            priority=45,
            name='Insurance Office',
            rules_text='When you lose a THUG or another HOLDING, '
                       'place 2 markers on this. '
                       'You can\'t lose markers from this HOLDING.'
        )

    @Card.markers.setter
    def markers(self, value):
        if self._markers < value:
            self._markers = value

    def when_played(self, game, tableau):
        orig_discard_thug = tableau.discard_thug
        def add_2_markers_when_thug_discarded(tableau, game):
            self.markers += 2
            return orig_discard_thug(game)

        tableau.discard_thug = types.MethodType(add_2_markers_when_thug_discarded, tableau)

        orig_discard_holding = tableau.discard_holding
        def add_2_markers_when_holding_discarded(tableau, game):
            self.markers += 2
            return orig_discard_holding(game)

        tableau.discard_holding = types.MethodType(add_2_markers_when_holding_discarded, tableau)

class Shakedown(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=3,
            name='Shakedown!',
            rules_text='Gain $10,000. When an adjactent player plays a THUG this turn, gain $10,000.'
        )

    def when_played(self, game, tableau):
        tableau.cash += 10000
        current_player = tableau
        current_round = game.current_round
        current_player_index = game.players.index(tableau)
        left_player = [game.players[current_player_index - 1]] if len(game.players) >= 2 else []
        right_player = [game.players[current_player_index + 1]] if len(game.players) > 2 else []
        adjacent_players = left_player + right_player
        for player in adjacent_players:
            orig_play_thug = player.play_thug
            def gain_10000_when_thug_played_this_turn(tableau, game, card):
                if game.current_round == current_round:
                    current_player.cash += 10000
                return orig_play_thug(game, card)

            player.play_thug = types.MethodType(gain_10000_when_thug_played_this_turn, player)

class Arson(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=75,
            name='Arson!',
            rules_text='Each opponent loses $10,000 for each THUG you have.'
        )

    def when_played(self, game, tableau):
        for player in game.players:
            if player != tableau:
                player.cash -= 10000 * tableau.calculate_icons().thugs

class Sting(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=33,
            name='Sting!',
            rules_text='Gain $10,000 for each CAR you have and $10,000 for each HEART you have.'
        )

    def when_played(self, game, tableau):
        total_icons = tableau.calculate_icons()
        tableau.cash += 10000 * (total_icons.cars + total_icons.hearts)

class MuseumHeist(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=30,
            name='Museum heist!',
            rules_text='Gain $25,000.',
            needs=Icons(guns=1, cars=1, keys=1)
        )

    def when_played(self, game, tableau):
        tableau.cash += 25000

class StreetWalkers(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=39,
            name='Street walkers!',
            rules_text='Place a marker on each of your HOLDINGS.',
            needs=Icons(hearts=1)
        )

    def when_played(self, game, tableau):
        for holding in tableau.holdings:
            holding.markers += 1

class Raid(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=59,
            name='Raid!',
            rules_text='Each opponent removes a marker from each of their HOLDINGS.',
            needs=Icons(guns=1)
        )

    def when_played(self, game, tableau):
        for player in game.players:
            if player != tableau:
                for holding in player.holdings:
                    holding.markers -= 1

class MasterPlan(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=78,
            name='Master Plan!',
            rules_text='Next turn, double all $ you gain.'
        )

    def when_played(self, game, tableau):
        next_turn = game.current_round + 1
        orig_set_cash = tableau._set_cash

        def double_cash_gained_next_turn(tableau, cash):
            if game.current_round == next_turn and cash > tableau.cash:
                delta = cash - tableau.cash
                cash = tableau.cash + (2 * delta)
            orig_set_cash(cash)

        tableau._set_cash = types.MethodType(double_cash_gained_next_turn, tableau)

class ProtectionRacket(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=60,
            name='Protection Racket!',
            rules_text='Gain $5,000 for each HOLDING the player with the most HOLDINGS has.'
        )

    def when_played(self, game, tableau):
        max_holdings_count = max([player.calculate_icons().holdings for player in game.players])
        max_holdings = [player for player in game.players if player.calculate_icons().holdings == max_holdings_count]
        if len(max_holdings) == 1:
            tableau.cash += 5000 * max_holdings_count

class InsuranceScam(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=5,
            name='Insurance Scam!',
            rules_text='Gain $5,000 for each marker on the HOLDING of yours with the most markers. '
                       'At the end of next turn, each player (including you) '
                       'loses a HOLDING they choose.',
            needs=Icons(keys=1)
        )

    def when_played(self, game, tableau):
        tableau.cash += 5000 * max([holding.markers for holding in tableau.holdings] or [0])
        next_round = game.current_round + 1
        orig_end_round = game.end_round
        def lose_holding_end_of_next_turn(game):
            if game.current_round == next_round:
                for player in game.players:
                    player.discard_holding(game)
            orig_end_round()

        game.end_round = types.MethodType(lose_holding_end_of_next_turn, game)

class SuicideMission(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=35,
            name='Suicide Mission!',
            rules_text='Gain $25,000.',
            costs=[Cost(thugs=1)]
        )

    def when_played(self, game, tableau):
        tableau.discard_thug(game)
        tableau.cash += 25000

class Vandalism(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=79,
            name='Vandalism!',
            rules_text='At the end of next turn, each opponent loses a HOLDING they choose.',
            needs=Icons(cars=1)
        )

    def when_played(self, game, tableau):
        next_round = game.current_round + 1
        orig_end_round = game.end_round
        def each_opponent_lose_holding_end_of_next_turn(game):
            if game.current_round == next_round:
                for player in game.players:
                    if player != tableau:
                        player.discard_holding(game)
            orig_end_round()

        game.end_round = types.MethodType(each_opponent_lose_holding_end_of_next_turn, game)

class OneLastHeist(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=73,
            name='One last heist!',
            rules_text='Gain $5,000 for each THUGH the player with the most THUGS has. '
                       'At the end of next turn, each player (including you) '
                       'loses a THUG they choose.',
            needs=Icons(guns=1)
        )

    def when_played(self, game, tableau):
        max_thugs_count = max([player.calculate_icons().thugs for player in game.players] or [0])
        max_thugs = [player for player in game.players if player.calculate_icons().thugs == max_thugs_count]
        if len(max_thugs) == 1:
            tableau.cash += 5000 * max_thugs_count
        next_round = game.current_round + 1
        orig_end_round = game.end_round
        def lose_thug_end_of_next_turn(game):
            if game.current_round == next_round:
                for player in game.players:
                    player.discard_thug(game)
            orig_end_round()

        game.end_round = types.MethodType(lose_thug_end_of_next_turn, game)

class StealIdeas(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=56,
            name='Steal Ideas!',
            rules_text='Place as many markers onto one of your HOLDINGS '
                       'as are on the HOLDING an opponent has with the most markers.',
            needs=Icons(wrenches=1)
        )

    def when_played(self, game, tableau):
        selected_holding, tableau.holdings = tableau.select_option(tableau.holdings, remove_option=False)
        max_markers_count = max([holding.markers for player in game.players for holding in player.holdings if player != tableau])
        max_markers = [holding for player in game.players for holding in player.holdings if player != tableau and holding.markers == max_markers_count]
        if len(max_markers) == 1:
            selected_holding.markers += max_markers_count

class InsiderTrading(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=29,
            name='Insider Trading!',
            rules_text='Gain $45,000.',
            needs=Icons(cash=90000)
        )

    def when_played(self, game, tableau):
        tableau.cash += 45000

class PickpocketNetwork(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=31,
            name='Pickpocket network!',
            rules_text='Gain $10,000 for each KEY you have and $10,000 for each WRENCH you have.'
        )

    def when_played(self, game, tableau):
        total_icons = tableau.calculate_icons()
        tableau.cash += 10000 * (total_icons.keys + total_icons.wrenches)

class Liquidate(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=4,
            name='Liquidate!',
            rules_text='Gain $15,000 for each marker that was on the HOLDING you paid.',
            costs=[Cost(holdings=1)]
        )

    def when_played(self, game, tableau):
        discarded_holding = game.discard_deck[-1]
        tableau.cash += 15000 * discarded_holding.markers

class Renovate(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=38,
            name='Renovate!',
            rules_text='Place two markers on one of your HOLDINGS.'
        )

    def when_played(self, game, tableau):
        selected_holding, tableau.holdings = tableau.select_option(tableau.holdings, remove_option=False)
        selected_holding.markers += 2

class Scouting(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=74,
            name='Scouting!',
            rules_text='If you have a CAR, gain $10,000. '
                       'If you have a GUN, each opponent loses $10,000. '
                       'If you have a KEY, draw a card from the deck, taking it to your hand.'
        )

    def when_played(self, game, tableau):
        total_icons = tableau.calculate_icons()
        if total_icons.cars > 0:
            tableau.cash += 10000

        if total_icons.guns > 0:
            for player in game.players:
                if player != tableau:
                    player.cash -= 10000

        if total_icons.keys > 0:
            tableau.hand.append(game.draw_deck.pop())

class Smuggling(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=32,
            name='Smuggling!',
            rules_text='Gain $25,000.',
            needs=Icons(cars=1, alcohol=1)
        )

    def when_played(self, game, tableau):
        tableau.cash += 25000

class EstateHeist(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=74,
            name='Estate heist!',
            rules_text='Gain $10,000 if you have a GUN. '
                       'Gain $10,000 if you have a CAR. '
                       'Gain $10,000 if you have a KEYß.'
        )

    def when_played(self, game, tableau):
        total_icons = tableau.calculate_icons()
        if total_icons.cars > 0:
            tableau.cash += 10000

        if total_icons.guns > 0:
            tableau.cash += 10000

        if total_icons.keys > 0:
            tableau.cash += 10000

class TakeCareOfBusiness(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=40,
            name='Take care of business!',
            rules_text='Place a marker on each of your HOLDIGNS with no more than one marker. '
                       'At the end of next turn each opponent loses a THUG they choose.'
        )

    def when_played(self, game, tableau):
        for holding in tableau.holdings:
            if holding.markers <= 1:
                holding.markers += 1

        next_round = game.current_round + 1
        orig_end_round = game.end_round
        def lose_thug_end_of_next_turn(game):
            if game.current_round == next_round:
                for player in game.players:
                    if player != tableau:
                        player.discard_thug(game)
            orig_end_round()

        game.end_round = types.MethodType(lose_thug_end_of_next_turn, game)

class Gambit(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=26,
            name='Gambit!',
            rules_text='Gain $30,000.',
            costs=[Cost(cards=1)]
        )

    def when_played(self, game, tableau):
        tableau.cash += 30000

class SuckerConvention(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=34,
            name='Sucker convention!',
            rules_text='Gain $30,000. Each other player gain $10,000.'
        )

    def when_played(self, game, tableau):
        for player in game.players:
            if player == tableau:
                player.cash += 30000
            else:
                player.cash += 10000

class CircusOfCrime(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=26,
            name='Circus of crime!',
            rules_text='Gain $10,000 for each THUG you have.',
            costs=[Cost(holdings=2)]
        )

    def when_played(self, game, tableau):
        tableau.cash = 10000 * len(tableau.thugs)

class ComplexScheme(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=43,
            name='Complex Scheme!',
            rules_text='Next turn, any time you play a HOLDING, place 3 extra markers on it.',
            needs=Icons(keys=1, wrenches=1)
        )

    def when_played(self, game, tableau):
        orig_play_holding = tableau.play_holding
        next_turn = game.current_round + 1
        def place_3_extra_markers(tableau, game, card):
            if game.current_round == next_turn:
                card.markers += 3
            orig_play_holding(game, card)

        tableau.play_holding = types.MethodType(place_3_extra_markers, tableau)

class BeggarsBanquet(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=20,
            name='Beggars Banquet!',
            rules_text='Gain $25,000.'
        )

    def when_played(self, game, tableau):
        min_thugs_count = min([player.calculate_icons().thugs for player in game.players])
        min_thugs = [player for player in game.players if player.calculate_icons().thugs == min_thugs_count]
        if len(min_thugs) == 1 and min_thugs[0] == tableau:
            tableau.cash += 25000

class Inform(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=2,
            name='Inform!',
            rules_text='Gain $10,000. When an adjactent player plays an ACTION this turn, gain $10,000.'
        )

    def when_played(self, game, tableau):
        tableau.cash += 10000
        current_player = tableau
        current_round = game.current_round
        current_player_index = game.players.index(tableau)
        left_player = [game.players[current_player_index - 1]] if len(game.players) >= 2 else []
        right_player = [game.players[current_player_index + 1]] if len(game.players) > 2 else []
        adjacent_players = left_player + right_player
        for player in adjacent_players:
            orig_play_action = player.play_action
            def gain_10000_when_action_played_this_turn(tableau, game, card):
                if game.current_round == current_round:
                    current_player.cash += 10000
                return orig_play_action(game, card)

            player.play_action = types.MethodType(gain_10000_when_action_played_this_turn, player)

class HonestWork(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=36,
            name='Honest work!',
            rules_text='Gain $15,000. Then, if you have less than $50,000, return this card to your hand.'
        )

    def when_played(self, game, tableau):
        tableau.cash += 15000
        current_round = game.current_round
        current_player = tableau
        orig_discard_card = game.discard_card
        def return_card_to_hand_if_less_than_5000(game, tableau, card, on_discard=True):
            orig_discard_card(tableau, card, on_discard)
            if (game.current_round == current_round and
                    tableau == current_player and
                    card == self and
                    tableau.cash < 50000):
                tableau.hand.append(card)
                game.discard_deck = [discarded_card for discarded_card in game.discard_deck
                                     if discarded_card != card]

        game.discard_card = types.MethodType(return_card_to_hand_if_less_than_5000, game)

class Seance(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=80,
            name='Seance!',
            rules_text='Gain $10,000. Place a marker on one of your HOLDINGS. '
                       'You may play another card.'
        )

    def when_played(self, game, tableau):
        tableau.cash += 10000
        selected_holding, tableau.holdings = tableau.select_option(tableau.holdings, remove_option=False)
        selected_holding.markers += 1
        selected_card, tableau.hand = tableau.select_option(tableau.hand)
        tableau.play_card(game, selected_card)

class Relocate(Card):
    def __init__(self):
        super().__init__(
            card_type=CardType.ACTION,
            priority=41,
            name='Relocate!',
            costs=[Cost(holdings=1)],
            rules_text='Next turn, any time you play a HOLDING, '
                       'place as many extra markers on it as were on the '
                       'HOLDING you paid, plus two.'
        )

    def when_played(self, game, tableau):
        cost_paid = self.costs_paid.pop()
        extra_markers = cost_paid.markers
        cost_paid.markers = 0
        tableau.hand.append(cost_paid)
        orig_play_holding = tableau.play_holding
        next_turn = game.current_round + 1
        def place_extra_markers_plus_2(tableau, game, card):
            if game.current_round == next_turn:
                card.markers += extra_markers + 2
            orig_play_holding(game, card)

        tableau.play_holding = types.MethodType(place_extra_markers_plus_2, tableau)
