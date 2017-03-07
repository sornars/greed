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

        each_turn_cards = [(player, card) for player in self.players for card in player.thugs + player.holdings]
        each_turn_cards.sort(key=lambda x: x[1].priority)
        for player, card in each_turn_cards:
            card.each_turn(self, player)

    def end_round(self):
        self.draft_decks = self.draft_decks[-1:] + self.draft_decks[:-1]
        if self.current_round == 12:
            end_of_game_cards = [(player, card) for player in self.players for card in player.thugs + player.holdings]
            end_of_game_cards.sort(key=lambda x: x[1].priority)
            for player, card in end_of_game_cards:
                card.end_of_game(self, player)

    def discard_card(self, tableau, card, on_discard=True):
        if on_discard:
            card.on_discard(self, tableau)
        self.discard_deck.append(card)