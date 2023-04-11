from enum import Enum
from typing import cast, Any
import abc
from abc import abstractmethod
import random
import sys


class Suit(str, Enum):
    Club = "\N{BLACK CLUB SUIT}"
    Diamond = "\N{BLACK DIAMOND SUIT}"
    Heart = "\N{BLACK HEART SUIT}"
    Spade = "\N{BLACK SPADE SUIT}"


class Card:
    insure = False

    def __init__(self,
                 rank: str,
                 suit: Suit,
                 hard: int,
                 soft: int) -> None:
        """Initialize a Card with a suit and rank"""

        self.suit = suit
        self.rank = rank
        self.hard = hard
        self.soft = soft

    # override the built-in __repr__ and __str__ methods 
    # to report more meaningful information
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(rank={self.suit!r}, suit={self.suit!r}, "
            f"hard={self.hard!r}, soft={self.soft!r})"
        )

    def __str__(self) -> str:
        return f"{self.rank}{self.suit}"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return (
            self.suit == other.suit
            and self.rank == other.rank
        )

    def __ne__(self, other: Any) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return (
            self.rank != other.rank
            or self.suit != other.suit
        )

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank < other.rank

    def __le__(self, other: Any) -> bool:
        try:
            return self.rank <= cast(Card, other).rank
        except AttributeError:
            return NotImplemented

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.rank > other.rank

    def __ge__(self, other: Any) -> bool:
        try:
            return self.rank >= cast(Card, other).rank
        except AttributeError:
            return NotImplemented

    def __hash__(self) -> int:
        return (
            hash(self.suit) + 4*hash(self.rank)
        ) % sys.hash_info.modulus

    # def __format__(self, format_spec: str) -> str:
    #     if format_spec == "":
    #         return str(self)
        # rs = (
        #     format_spec.replace("%r", self.rank)
        #     .replace("%s", self.suit)
        #     .replace("%%", "%s")
        # )
        # return rs


class NumberCard(Card):

    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__(rank, suit, rank, rank)


class AceCard(Card):
    insure = True

    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__("A", suit, 1, 11)

    def __str__(self) -> str:
        return f"A{self.suit}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(rank={self.rank!r},\
            suit={self.suit!r}, hard={self.hard!r}, soft={self.soft!r})"


class FaceCard(Card):
    facemap = {
            11: "J",
            12: "Q",
            13: "K"
        }

    def __init__(self, rank: int, suit: Suit) -> None:
        super().__init__(rank, suit, 10, 10)

    def __str__(self) -> str:
        return f"{self.facemap[self.rank]}{self.suit}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(rank={self.rank!r},\
            suit={self.suit!r}, hard={self.hard!r}, soft={self.soft!r})"


def card(rank: int, suit: Suit) -> Card:
    if rank == 1:
        return AceCard(rank, suit)
    elif 2 <= rank < 11:
        return NumberCard(rank, suit)
    elif 11 <= rank < 14:
        return FaceCard(rank, suit)
    else:
        raise TypeError


class Deck(list):

    def __init__(self, decks: int = 1) -> None:
        super().__init__(
            card(r + 1, s) 
            for r in range(13) 
            for s in iter(Suit)
            for d in range(decks)
            )
        random.shuffle(self)
        burn = random.randint(1, 52)
        for i in range(burn):
            self.pop()


class Hand:

    def __init__(self, dealer_card: Card, *cards: Card) -> None:
        self.dealer_card = dealer_card
        self.cards = list(cards)

    def __str__(self) -> str:
        return ", ".join(map(str, self.cards))

    def __repr__(self) -> str:
        cards_text = ", ".join(map(repr, self.cards))
        return f"{self.__class__.__name__}({self.dealer_card!r}, {cards_text})"

    def __format__(self, spec: str) -> str:
        if spec == "":
            return str(self)
        return ", ".join(f"{c:{spec}}" for c in self.cards)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.total() == other
        try:
            return (
                self.cards == cast(Hand, other).cards
                and self.dealer_card == cast(Hand, other).dealer_card
            )
        except AttributeError:
            # fall back to reverse operator
            return NotImplemented

    def __ne__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.total() == other
        try:
            return (
                self.cards != cast(Hand, other).cards
                or self.dealer_card != cast(Hand, other).dealer_card
            )
        except AttributeError:
            # fall back to reverse operator
            return NotImplemented


    def __lt__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.total() < cast(int, other)
        try:
            return self.total() < cast(Hand, other).total()
        except AttributeError:
            return NotImplemented
    
    def __gt__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.total() > cast(int, other)
        try:
            return self.total() > cast(Hand, other).total()
        except AttributeError:
            return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.total() <= cast(int, other)
        try:
            return self.total() <= cast(Hand, other).total()
        except AttributeError:
            return NotImplemented

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, int):
            return self.total() >= cast(int, other)
        try:
            return self.total() >= cast(Hand, other).total()
        except AttributeError:
            return NotImplemented

    def total(self) -> int:
        delta_soft = max(c.soft - c.hard for c in self.cards)
        hard = sum(c.hard for c in self.cards)
        if hard + delta_soft <= 21:
            return hard + delta_soft
        return hard


class FrozenHand(Hand):

    def __init__(self, *args, **kwargs) -> None:
        if len(args) == 1 and isinstance(args[0], Hand):
            # Clone a hand
            other = cast(Hand, args[0])
            self.dealer_card = other.dealer_card
            self.cards = other.cards
        else:
            # Build a fresh Hand from Card instances
            super().__init__(*args, **kwargs)

    def __hash__(self) -> int:
        return sum(hash(c) for c in self.cards) % sys.hash_info.modulus


# test the implementation
# d = Deck()
# h = Hand(d.pop(), d.pop(), d.pop())
# s1 = Hand(h, d.pop(), split=0)
# s2 = Hand(h, d.pop(), split=1)

class GameStrategy:
    """Each method requires the current Hand object as an argument value.
    The decisions are based on the available information;
    that is, on the dealer's cards and the player's cards.
    The result of each decision is shown in the type hints as a Boolean value.
    Each method returns True if the player elects to perform the action.
    """
    def insurance(self, hand: Hand) -> bool:
        return False

    def split(self, hand: Hand) -> bool:
        return False

    def double(self, hand: Hand) -> bool:
        return False

    def hit(self, hand: Hand) -> bool:
        return sum(c.hard for c in hand.cards) <= 17


# The player must place an initial, or ante, bet based on the betting strategy.
# The player will then receive a hand of cards.
# If the hand is splittable, the player must decide whether to split it or not
# based on their game strategy. 
# This can create additional Hand instances. In some casinos, 
# the additional hands are also splittable.
# For each Hand instance, the player must decide to hit, double, or stand 
# based on their game strategy.
# The player will then receive payouts, and they must update 
# their betting strategy based on their wins and losses.


class Table:

    def __init__(self) -> None:
        self.deck = Deck()

    def place_bet(self, amount: int) -> None:
        print("Bet", amount)

    def get_hand(self) -> Hand:
        try:
            self.hand = Hand(
                self.deck.pop(),
                self.deck.pop(),
                self.deck.pop()
            )
            self.hole_card = self.deck.pop()
        except IndexError:
            # Out of cards: need to shuffle and try again
            self.deck = Deck()
            return self.get_hand()
        print("Deal", self.hand)
        return self.hand

    def can_insure(self, hand: Hand) -> bool:
        return hand.dealer_card.insure


class BettingStrategy(metaclass=abc.ABCMeta):

    @abstractmethod
    def bet(self) -> int:
        return 1

    def record_win(self) -> None:
        pass

    def record_loss(self) -> None:
        pass


class Player:

    def __init__(
        self,
        table: Table,
        bet_strategy: BettingStrategy,
        game_strategy: GameStrategy,
        **extras,
    ) -> None:
        self.table = table
        self.bet_strategy = bet_strategy
        self.game_strategy = game_strategy
        if extras:
            raise TypeError(f"Extra arguments: {extras!r}")

    def game(self):
        self.table.place_bet(self.bet_strategy.bet())
        self.hand = self.table.get_hand()
