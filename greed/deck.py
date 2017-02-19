class Deck:
    def __init__(self, cards=None):
        self.cards = [] if cards is None else cards

    def draw_card(self):
        return self.cards.pop()

    def add_card(self, card):
        self.cards.append(card)

    def __repr__(self):
        return str(len(self.cards))
