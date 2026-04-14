from playingcard import PlayingCard, CardSuit, _valid_rank_, _convert_to_rank
from collections.abc import Container
import unittest
import random


_full_deck_ = [PlayingCard(s, r) for s in CardSuit for r in range(1, 14)]


class DirtyDeck(Container):

    def __init__(self, *, hide=None):
        self.deck = _full_deck_.copy()
        self.hidden = None
        if hide is not None:
            if not _valid_rank_(hide):
                raise ValueError(f"{hide} is not a card rank")
            self.hidden = _convert_to_rank(hide)

    def __str__(self):
        retstr = ""
        for c in self.deck:
            retstr += f"{str(c)} "
        return retstr

    def __contains__(self, c):
        return c in self.deck

    def __len__(self):
        return len(self.deck)
    
    def __iter__(self):
        return iter(self.deck)
    
    def _swap(self, a, b):
        """ swap two cards """
        return b, a

    def shuffle(self):
        """ Shuffle the deck, and allows to move hidden cards to the end of the deck. """
        self.deck = _full_deck_.copy()  # making a copy of the desk
        # shuffling the deck using the Fisher-Yates algorithm
        deck_size = len(self.deck)
        for i in range(deck_size - 1, 0, -1):
            j = random.randint(0, i)
            self.deck[i], self.deck[j] = self._swap(self.deck[i], self.deck[j])
        # if there is a hidden card, moving it towards the end of the deck
        if self.hidden is not None:
            hidden = []
            visible = []
            # separating the hidden cards from the visible cards
            for card in self.deck:
                if card.rank == self.hidden:
                    hidden.append(card)
                else:
                    visible.append(card)
            self.deck = visible + hidden  # merging the visible and hidden together

    def deal(self):
        """ Remove and return the top card from the deck. """
        low_deck_limit = len(_full_deck_) * 0.25  # declaring a low deck limit
        # if the current deck is less than or equal than the deck limit raise a ResourceWarning
        if len(self.deck) <= low_deck_limit:
            raise ResourceWarning("low deck")
        top_card = self.deck.pop()  # removing and returning the top card from the deck
        return top_card


if __name__ == "__main__":
    # simple test
    d = DirtyDeck()
    print(f"printing deck: {d}")
    d.shuffle()
    print(f"printing deck After Shuffle: {d}")
    print(f"dealing card: {d.deal()}")
    print(len(d))
    d = DirtyDeck(hide='Jack')
    d.shuffle()
    print(f"printing deck with Jack hidden: {d}")
    print(f"dealing card: {d.deal()}")
    d = DirtyDeck(hide=10)
    d.shuffle()
    print(f"printing deck with 10 hidden: {d}")
    try:
        DirtyDeck(hide=17)
    except Exception as e:
        print(f"{e}")
    while True:
        print(d.deal(), end=" ")
