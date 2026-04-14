import unittest
from enum import Enum


class CardSuit(Enum):
    CLUBS = 1
    DIAMONDS = 2
    HEARTS = 3
    SPADES = 4


CLUBBASE = 0x1F0D1
DIABASE = 0x1F0C1
HEARTBASE = 0x1F0B2
SPADEBASE = 0x1F0A1


# ******** str methods *********
_card_unicode_ = False


def _card_from_rank(rank, firstcard):
    unival = firstcard + rank
    return str(chr(unival))


def _card_uni_(card):  # unicode cards
    if card.rank == 0:
        return "\u1f0cF"  # just black joker...
    match card.suit:
        case CardSuit.CLUBS:
            return _card_from_rank(card.rank, CLUBBASE)
        case CardSuit.DIAMONDS:
            return _card_from_rank(card.rank, DIABASE)
        case CardSuit.HEARTS:
            return _card_from_rank(card.rank, HEARTBASE)
        case CardSuit.SPADES:
            return _card_from_rank(card.rank, SPADEBASE)
    assert False  # should never get here


def _rank_str_(rank):
    if rank == 0:
        return "Joker"

    match rank:
        case 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10:
            return str(rank)
        case 1:
            return "A"
        case 11:
            return "J"
        case 12:
            return "Q"
        case 13:
            return "K"


def _card_str_(card):  # text version
    if card.rank == 0:
        return "Joker"
    match card.suit:
        case CardSuit.CLUBS:
            return f"{_rank_str_(card.rank)}\u2663"
        case CardSuit.DIAMONDS:
            return f"{_rank_str_(card.rank)}\u2666"
        case CardSuit.HEARTS:
            return f"{_rank_str_(card.rank)}\u2665"
        case CardSuit.SPADES:
            return f"{_rank_str_(card.rank)}\u2660"
    assert False  # should never get here


def _convert_to_rank(rankname):
    match rankname:
        case 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10:
            return rankname
        case "Ace":
            return 1
        case "Jack" | 11:
            return 11
        case "Queen" | 12:
            return 12
        case "King" | 13:
            return 13
        case "Joker" | 0:
            return 0
    raise ValueError("bad rank")


def _valid_rank_(rank):
    try:
        r = _convert_to_rank(rank)
    except Exception:
        return False
    return True


class PlayingCard:

    def __init__(self, suit, rank):  # if rank==0 get joker
        if suit not in CardSuit:
            raise ValueError(f"{suit} is not a card suit")
        if not _valid_rank_(rank):
            raise ValueError(f"{rank} is not a card rank")
        self.suit = CardSuit(suit)
        self.rank = _convert_to_rank(rank)

    def __str__(self):
        if _card_unicode_:
            return _card_uni_(self)
        return _card_str_(self)

    def __eq__(self, c):
        if c.rank != self.rank:
            return False
        if not c.rank:  # Joker
            return True
        return c.suit == self.suit

    @staticmethod
    def cardUnicode(b):
        _card_unicode_ = bool(b)


if __name__ == "__main__":

    class CardTest(unittest.TestCase):

        def test_create_cards(self):
            for s in CardSuit:
                for r in range(0, 14):
                    trialcard = PlayingCard(s, r)
            for s in CardSuit:
                trialcard = PlayingCard(s, "Jack")
                trialcard = PlayingCard(s, "Queen")
                trialcard = PlayingCard(s, "King")
                trialcard = PlayingCard(s, "Ace")

        def test_eq(self):
            trialcard0 = PlayingCard(CardSuit.CLUBS, 1)
            trialcard1 = PlayingCard(CardSuit.CLUBS, "Ace")
            self.assertEqual(trialcard0, trialcard1)
            trialcard2 = PlayingCard(CardSuit.HEARTS, "Ace")
            self.assertNotEqual(trialcard0, trialcard2)
            trialcard3 = PlayingCard(CardSuit.CLUBS, "Jack")
            self.assertNotEqual(trialcard0, trialcard3)

        def test_str(self):
            pass

        def test_unicode(self):
            pass

    unittest.main()
