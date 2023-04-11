from enum import Enum


class Suit(str, Enum):
    Club = "♣"
    Diamond = "♦"
    Heart = "♥"
    Spade = "♠"


class Card:

    def __init__(self, rank: str, suit: str) -> None:
        """Initialize a Card with a suit and rank

        Args:
            rank (str): the score rank of the Card
            suit (str): the suit of the card
        """
        self.suit = suit
        self.rank = rank
        self.hard, self.soft = self._points()

    def _points(self) -> Tuple[int, int]:
        """_summary_

        The leading _ in the name is a suggestion to someone reading
        the class that the _points() method is an implementation detail,
        subject to change in a future implementation.

        Returns:
            Tuple[int, int]: _description_
        """
        return int(self.rank), int(self.rank)


class AceCard(Card):
    """Set the special Ace card class.

    The Ace card may return one of two values, either 1 or 11

    Args:
        Card (Tuple): _description_
    """
    def _points(self) -> Tuple[int, int]:
        return 1, 11


class FaceCard(Card):
    """Set the special Face card class.

    The Face card returns a 10

    Args:
        Card (Tuple): _description_
    """
    def _points(self) -> Tuple[int, int]:
        return 10, 10


def card(rank: int, suit: Suit) -> Card:
    """Factory function to define Card subclasses to build a full deck

    Args:
        rank (int): the card rank value
        suit (Suit): the card suit value

    Returns:
        Card: a card with rank and suit
    """
    if rank == 1:
        return AceCard("A", suit)
    elif 2 <= rank < 11:
        return Card(str(rank), suit)
    elif 11 <= rank < 14:
        name = {11: "J",
                12: "Q",
                13: "K"}[rank]
        return FaceCard(name, suit)
    raise Exception("Design Failure")


deck = [card(rank, suit) for rank in range(1, 14) for suit in iter(Suit)]


def card_without_mapping(rank: int, suit: Suit) -> Card:
    if rank == 1:
        return AceCard("A", suit)
    if 2 <= rank < 11:
        return Card(str(rank), suit)
    elif rank == 11:
        return FaceCard("J", suit)
    elif rank == 12:
        return FaceCard("Q", suit)
    elif rank == 13:
        return FaceCard("K", suit)
    else:
        raise Exception("Rank out of range, should be between 1 and 13")


def card_with_only_mapping(rank: int, suit: Suit) -> Card:
    """The fully refactored function associates a rank object with a
    lambda object (which is a function type object). The lambda object
    contains a class, Card, and a string. The lambda object is then applied
    to the suit object to create the Card instance. 

    Args:
        rank (int): _description_
        suit (Suit): _description_

    Returns:
        Card: _description_
    """
    class_rank = {
        1: lambda suit: AceCard("A", suit),
        11: lambda suit: FaceCard("J", suit),
        12: lambda suit: FaceCard("Q", suit),
        13: lambda suit: FaceCard("K", suit)
    }.get(
        rank, lambda suit: Card(str(rank), suit)
    )
    return class_rank(suit)


class CardFactory:

    def rank(self, rank: int) -> "CardFactory":
        """Updates the constructor state

        Args:
            rank (int): _description_

        Returns:
            CardFactory: _description_
        """
        self.class_, self.rank_str = {
            1: (AceCard, "A"),
            11: (FaceCard, "J"),
            12: (FaceCard, "Q"),
            13: (FaceCard, "K")
        }.get(
            rank, (Card, str(rank))
        )
        return self

    def suit(self, suit: Suit) -> Card:
        """creates a Card object

        Args:
            suit (Suit): _description_

        Returns:
            Card: _description_
        """
        return self.class_(self.rank_str, suit)
