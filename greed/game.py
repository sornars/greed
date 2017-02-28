from .deck import create_draw_deck

class Game:
    def __init__(self, players):
        self.players = players
        self.current_round = 0
        self.draw_deck = create_draw_deck()
        self.draft_decks = [[self.draw_deck.pop() for _ in range(0, 12)] for _ in self.players]
        self.discard_deck = []

    def start_round(self):
        self.current_round += 1

        for index, player in enumerate(self.players):
            player.draft_card(self.draft_decks[index])

        played_cards = [(player, player.select_option(player.hand)) for player in self.players]
        played_cards.sort(key=lambda x: x[1].priority)
        for player, card in played_cards:
            player.play_card(self, card)

    def discard_card(self, tableau, card):
        card.on_discard(self, tableau)
        self.discard_deck.append(card)