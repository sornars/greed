import random

from .card import Card, CardType
from .deck import Deck
from .tableau import Tableau

class Game:
    def __init__(self, players):
        self.players = players
        self.round = 1
        self.current_player = None
        self.draw_deck = self._create_draw_deck()
        self.draft_decks = [Deck([self.draw_deck.cards.pop() for _ in range(0, 12)]) for _ in self.players]
        self.discard_deck = []

    def _create_draw_deck(self):
        # TODO: Implement generation of actual card deck
        cards = [Card(random.choice(list(CardType)), 'Card {0}'.format(i), i) for i in range(0, 80)]
        return Deck(cards)

    def start_round(self):
        for index, player in enumerate(self.players):
            player.draft_card(self.draft_decks[index])
        if self.round > 2:
            played_cards = []
            for player in self.players:
                played_card = player.select_card()
                played_cards.append((player, played_card))

            played_cards.sort(key=lambda x: x[1].priority)
            for player, played_card in played_cards:
                self.current_player = player
                discard_card = player.tableau.play_card(played_card)
                played_card.this_turn(self)
                if discard_card:
                    self.discard_deck.append(played_card)

        self.end_round()

        if self.round == 12:
            self.end_game()

    def end_game(self):
        # TODO: Implement end of game scoring
        pass

    def end_round(self):
        self.draft_decks = self.draft_decks[1:] + [self.draft_decks[0]]
        self.round += 1

    def __repr__(self):
        return str({
            'players': self.players,
            'round': self.round,
            'draw_deck': self.draw_deck,
            'draft_decks': self.draft_decks
        })


class Player:
    def __init__(self, name):
        self.name = name
        self.tableau = Tableau()

    def draft_card(self, deck):
        # TODO: Implement player selection of card to draft
        self.tableau.hand.cards.append(deck.cards.pop())

    def select_card(self):
        # TODO: Implement card selection
        return self.tableau.hand.cards.pop()

    def __repr__(self):
        return str({
            'name': self.name,
            'tableau': self.tableau
        })